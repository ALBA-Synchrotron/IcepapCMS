#
# Copyright (c) 2006, 2007 Canonical
#
# Written by Gustavo Niemeyer <gustavo@niemeyer.net>
#
# This file is part of Storm Object Relational Mapper.
#
# Storm is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# Storm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Basic database interfacing mechanisms for Storm.

This is the common code for database support; specific databases are
supported in modules in L{storm.databases}.
"""

from storm.expr import Expr, State, compile
from storm.variables import Variable
from storm.exceptions import ClosedError
from storm.uri import URI
import storm


__all__ = ["Database", "Connection", "Result",
           "convert_param_marks", "create_database", "register_scheme"]


DEBUG = False


class Result(object):
    """A representation of the results from a single SQL statement."""

    _closed = False

    def __init__(self, connection, raw_cursor):
        self._connection = connection # Ensures deallocation order.
        self._raw_cursor = raw_cursor
        if raw_cursor.arraysize == 1:
            # Default of 1 is silly.
            self._raw_cursor.arraysize = 10

    def __del__(self):
        """Close the cursor."""
        try:
            self.close()
        except:
            pass

    def close(self):
        """Close the underlying raw cursor, if it hasn't already been closed.
        """
        if not self._closed:
            self._closed = True
            self._raw_cursor.close()
            self._raw_cursor = None

    def get_one(self):
        """Fetch one result from the cursor.

        The result will be converted to an appropriate format via
        L{from_database}.

        @return: A converted row or None, if no data is left.
        """
        row = self._raw_cursor.fetchone()
        if row is not None:
            return tuple(self.from_database(row))
        return None

    def get_all(self):
        """Fetch all results from the cursor.

        The results will be converted to an appropriate format via
        L{from_database}.
        """
        result = self._raw_cursor.fetchall()
        if result:
            return [tuple(self.from_database(row)) for row in result]
        return result

    def __iter__(self):
        """Yield all results, one at a time.

        The results will be converted to an appropriate format via
        L{from_database}.
        """
        while True:
            results = self._raw_cursor.fetchmany()
            if not results:
                break
            for result in results:
                yield tuple(self.from_database(result))

    def get_insert_identity(self, primary_columns, primary_variables):
        """Get a query which will return the row that was just inserted.

        This must be overridden in database-specific subclasses.

        @rtype: L{storm.expr.Expr}
        """
        raise NotImplementedError

    @staticmethod
    def set_variable(variable, value):
        """Set the given variable's value from the database."""
        variable.set(value, from_db=True)

    @staticmethod
    def from_database(row):
        """Convert a row fetched from the database to an agnostic format.

        This method is intended to be overridden in subclasses, but
        not called externally.

        If there are any peculiarities in the datatypes returned from
        a database backend, this method should be overridden in the
        backend subclass to convert them.
        """
        return row


class Connection(object):
    """A connection to a database.

    @cvar result_factory: A callable which takes this L{Connection}
        and the backend cursor and returns an instance of L{Result}.
    @type param_mark: C{str}
    @cvar param_mark: The dbapi paramstyle that the database backend expects.
    @type compile: L{storm.expr.Compile}
    @cvar compile: The compiler to use for connections of this type.
    """

    result_factory = Result
    param_mark = "?"
    compile = compile

    _closed = False

    def __init__(self, database, raw_connection):
        self._database = database # Ensures deallocation order.
        self._raw_connection = raw_connection

    def __del__(self):
        """Close the connection."""
        try:
            self.close()
        except:
            pass

    def execute(self, statement, params=None, noresult=False):
        """Execute a statement with the given parameters.

        @type statement: L{Expr} or C{str}
        @param statement: The statement to execute. It will be
            compiled if necessary.
        @param noresult: If True, no result will be returned.

        @return: The result of C{self.result_factory}, or None if
            C{noresult} is True.
        """
        if self._closed:
            raise ClosedError("Connection is closed")
        if isinstance(statement, Expr):
            if params is not None:
                raise ValueError("Can't pass parameters with expressions")
            state = State()
            statement = self.compile(statement, state)
            params = state.parameters
        statement = convert_param_marks(statement, "?", self.param_mark)
        raw_cursor = self.raw_execute(statement, params)
        if noresult:
            raw_cursor.close()
            return None
        return self.result_factory(self, raw_cursor)

    def close(self):
        """Close the connection if it is not already closed."""
        if not self._closed:
            self._closed = True
            self._raw_connection.close()
            self._raw_connection = None

    def commit(self):
        """Commit the connection."""
        self._raw_connection.commit()

    def rollback(self):
        """Rollback the connection."""
        self._raw_connection.rollback()

    @staticmethod
    def to_database(params):
        """Convert some parameters into values acceptable to a database backend.

        It is acceptable to override this method in subclasses, but it
        is not intended to be used externally.

        This delegates conversion to any L{Variable}s in the parameter
        list, and passes through all other values untouched.
        """
        for param in params:
            if isinstance(param, Variable):
                yield param.get(to_db=True)
            else:
                yield param

    def build_raw_cursor(self):
        """Get a new dbapi cursor object.

        It is acceptable to override this method in subclasses, but it
        is not intended to be called externally.
        """
        return self._raw_connection.cursor()

    def raw_execute(self, statement, params=None):
        """Execute a raw statement with the given parameters.

        It's acceptable to override this method in subclasses, but it
        is not intended to be called externally.

        If the global C{DEBUG} is True, the statement will be printed
        to standard out.

        @return: The dbapi cursor object, as fetched from L{build_raw_cursor}.
        """
        raw_cursor = self.build_raw_cursor()
        if not params:
            if DEBUG:
                print statement, ()
            raw_cursor.execute(statement)
        else:
            params = tuple(self.to_database(params))
            if DEBUG:
                print statement, params
            raw_cursor.execute(statement, params)
        return raw_cursor

    def preset_primary_key(self, primary_columns, primary_variables):
        """Process primary variables before an insert happens.

        This method may be overwritten by backends to implement custom
        changes in primary variables before an insert happens.
        """


class Database(object):
    """A database that can be connected to.

    This should be subclassed for individual database backends.

    @cvar connection_factory: A callable which will take this database
        and a raw connection and should return an instance of
        L{Connection}.
    """

    connection_factory = Connection

    def connect(self):
        """Create a connection to the database.

        This should be overriden in subclasses to do any
        database-specific connection setup. It should call
        C{self.connection_factory} to allow for ease of customization.

        @return: An instance of L{Connection}.
        """
        raise NotImplementedError


def convert_param_marks(statement, from_param_mark, to_param_mark):
    # TODO: Add support for $foo$bar$foo$ literals.
    if from_param_mark == to_param_mark or from_param_mark not in statement:
        return statement
    tokens = statement.split("'")
    for i in range(0, len(tokens), 2):
        tokens[i] = tokens[i].replace(from_param_mark, to_param_mark)
    return "'".join(tokens)


_database_schemes = {}

def register_scheme(scheme, factory):
    """Register a handler for a new database URI scheme.

    @param scheme: the database URI scheme
    @param factory: a function taking a URI instance and returning a database.
    """
    _database_schemes[scheme] = factory


def create_database(uri):
    """Create a database instance.

    @param uri: An URI instance, or a string describing the URI. Some examples:
        - "sqlite:" An in memory sqlite database.
        - "sqlite:example.db" A SQLite database called example.db
        - "postgres:test" The database 'test' from the local postgres server.
        - "postgres://user:password@host/test" The database test on machine host
          with supplied user credentials, using postgres.
        - "anything:..." Where 'anything' has previously been registered
          with L{register_scheme}.
    """
    if isinstance(uri, basestring):
        uri = URI(uri)
    if uri.scheme in _database_schemes:
        factory = _database_schemes[uri.scheme]
    else:
        module = __import__("%s.databases.%s" % (storm.__name__, uri.scheme),
                            None, None, [""])
        factory = module.create_from_uri
    return factory(uri)
