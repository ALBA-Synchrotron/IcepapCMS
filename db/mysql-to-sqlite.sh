#!/bin/bash
sqlt -f DBI --dsn dbi:mysql:icepapcms --db-user icepapcms --db-password configure -t SQLite > create_sqlite.sql
