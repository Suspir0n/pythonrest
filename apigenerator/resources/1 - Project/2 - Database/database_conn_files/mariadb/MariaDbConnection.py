# PyMysql Imports #
import pymysql

# Infra Imports #
from src.e_Infra.GlobalVariablesManager import *

# Global MySQL Connections #
mariadb_internet_conn = None


# Method returns connection according to given environment variables #
def get_mariadb_connection_schema_internet():
    # Assigning global variable #
    global mariadb_internet_conn

    # Creating connection Singleton Style #
    if not mariadb_internet_conn:
        mariadb_internet_conn = 'mysql+pymysql://' + get_global_variable('mariadb_user') + ':' \
                                                 + get_global_variable('mariadb_password') + '@' \
                                                 + get_global_variable('mariadb_host') + ':' \
                                                 + get_global_variable('mariadb_port') + '/' \
                                                 + get_global_variable('mariadb_schema')
    # Returning connection result #
    return mariadb_internet_conn
