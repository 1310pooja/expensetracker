# config.py

import os

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER', 'etdb')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Lkjhg098')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'etdb.mysql.database.azure.com')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'etdb')
    MYSQL_SSL_CA = os.getenv('MYSQL_SSL_CA', 'DigiCertGlobalRootG2.crt.pem')
    MYSQL_SSL_DISABLED = bool(os.getenv('MYSQL_SSL_DISABLED', False))
