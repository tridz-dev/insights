# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from contextlib import suppress

import frappe
from frappe.model.document import Document


class InsightsTableLinkv3(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        data_source: DF.Link
        left_column: DF.Data
        left_table: DF.Data
        name: DF.Int | None
        right_column: DF.Data
        right_table: DF.Data
    # end: auto-generated types

    def before_insert(self):
        if self.is_duplicate():
            frappe.throw("Link already exists", exc=frappe.DuplicateEntryError)

    def is_duplicate(self):
        # check if there a link with the same tables and columns
        # for eg. if there is a link between Orders and OrderItems with columns order_id and order_id
        # there should not be another link between OrderItems and Orders with columns order_id and order_id

        return frappe.db.exists(
            "Insights Table Link v3",
            {
                "left_table": self.right_table,
                "right_table": self.left_table,
                "left_column": self.right_column,
                "right_column": self.left_column,
            },
        ) or frappe.db.exists(
            "Insights Table Link v3",
            {
                "left_table": self.left_table,
                "right_table": self.right_table,
                "left_column": self.left_column,
                "right_column": self.right_column,
            },
        )

    @staticmethod
    def create(data_source, left_table, right_table, left_column, right_column):
        doc = frappe.new_doc("Insights Table Link v3")
        doc.data_source = data_source
        doc.left_table = left_table
        doc.right_table = right_table
        doc.left_column = left_column
        doc.right_column = right_column
        with suppress(frappe.DuplicateEntryError):
            doc.save(ignore_permissions=True)

    @staticmethod
    def get_links(data_source, left_table, right_table):
        left_to_right_links = frappe.get_all(
            "Insights Table Link v3",
            filters={
                "data_source": data_source,
                "left_table": left_table,
                "right_table": right_table,
            },
            fields=["left_table", "right_table", "left_column", "right_column"],
        )
        right_to_left_links = frappe.get_all(
            "Insights Table Link v3",
            filters={
                "data_source": data_source,
                "left_table": right_table,
                "right_table": left_table,
            },
            fields=[
                "left_table as right_table",
                "right_table as left_table",
                "left_column as right_column",
                "right_column as left_column",
            ],
        )
        return left_to_right_links + right_to_left_links
