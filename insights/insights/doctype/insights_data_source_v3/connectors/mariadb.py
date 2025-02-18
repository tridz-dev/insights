# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe


def get_mariadb_connection_string(data_source):
    password = data_source.get_password(raise_exception=False)
    connection_string = (
        f"mysql://{data_source.username}:{password}"
        f"@{data_source.host}:{data_source.port}/{data_source.database_name}"
    )
    extra_args = frappe._dict(
        ssl=data_source.use_ssl,
        ssl_verify_cert=data_source.use_ssl,
        charset="utf8mb4",
        use_unicode=True,
    )
    return connection_string, extra_args
