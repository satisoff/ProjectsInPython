from __future__ import annotations

import mysql.connector
from mysql.connector import MySQLConnection

from .config import Settings


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS fee_det (
    adm_no INT PRIMARY KEY,
    st_name VARCHAR(50) NOT NULL,
    class INT NOT NULL,
    sec CHAR(1) NOT NULL,
    cont_no BIGINT NOT NULL,
    subm_month VARCHAR(20) DEFAULT 'None',
    amt_submited INT DEFAULT 0,
    date_paymnt DATE NULL
);
"""

ACTIVITY_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(20) NOT NULL,
    adm_no INT NOT NULL,
    st_name VARCHAR(50) NULL,
    amount INT NULL,
    detail VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection(settings: Settings, *, with_database: bool = True) -> MySQLConnection:
    connect_args = {
        "host": settings.mysql_host,
        "port": settings.mysql_port,
        "user": settings.mysql_user,
        "password": settings.mysql_password,
    }
    if with_database:
        connect_args["database"] = settings.mysql_database

    if not settings.mysql_ssl_disabled:
        connect_args["ssl_disabled"] = False

    return mysql.connector.connect(**connect_args)


def init_database(settings: Settings) -> None:
    conn = get_connection(settings, with_database=False)
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.mysql_database}")
        cursor.execute(f"USE {settings.mysql_database}")
        cursor.execute(SCHEMA_SQL)
        cursor.execute(ACTIVITY_SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()
