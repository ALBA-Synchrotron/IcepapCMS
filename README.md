# IcepapCMS

![Pypi version][pypi]

Python module to configure, control and monitor IcePAP based systems.


## Installation
### Pypi 
From within your favourite python environment:

NOTE: PyQT5 5.15.2 has a bug: https://bugreports.qt.io/browse/QTBUG-88688
```console
pip install PyQT5==5.15.1 icepapcms
```

To use MySQL Databases you should install [mysqlclient](https://pypi.org/project/mysqlclient/)

To use PostgreSQL Databeses you should install [psycopg2](https://pypi.org/project/psycopg2/)


## Contribute

You can find how to contribute to this project on CONTRIBUTING.md file.


# Ldap configuration:
The LDAP configuration is located on the icepapcms configuration file: 

`<user home>/.icepapcms/icepapcms.conf`


The section "ldap" should have the next configuration:
```
[ldap]
    use = True
    not_allowed = root, operator, xxxxx
    servers = 'ldap://ldap01.test.com','ldap://ldap02.test.es'
    user_template = 'uid={},ou=Users,dc=Company,dc=XX'

```
# All networks configuration

The all networks flag is allowed: icepapcms --all-networks 

To avoid launching icepapcms with the flag all the time, it is possible to
configure it on the icepapcms configuration file: 

`<user home>/.icepapcms/icepapcms.conf`


The section "all_networks" should have the next configuration:
```
[all_networks]
use = True
```

[pypi]: https://img.shields.io/pypi/pyversions/icepap.svg