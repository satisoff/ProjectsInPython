from __future__ import annotations

from typing import Any

from .config import Settings
from .db import get_connection


class FeeRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _fetchone_dict(self, cursor) -> dict[str, Any] | None:
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "adm_no": row[0],
            "st_name": row[1],
            "class": row[2],
            "sec": row[3],
            "cont_no": row[4],
            "subm_month": row[5],
            "amt_submited": row[6],
            "date_paymnt": str(row[7]) if row[7] else None,
        }

    def create_student(self, payload: dict[str, Any]) -> None:
        conn = get_connection(self.settings)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO fee_det (adm_no, st_name, class, sec, cont_no, subm_month, amt_submited)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    payload["adm_no"],
                    payload["st_name"],
                    payload["class"],
                    payload["sec"],
                    payload["cont_no"],
                    payload.get("subm_month", "None"),
                    payload.get("amt_submited", 0),
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def get_student(self, adm_no: int) -> dict[str, Any] | None:
        conn = get_connection(self.settings)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT adm_no, st_name, class, sec, cont_no, subm_month, amt_submited, date_paymnt
                FROM fee_det WHERE adm_no = %s
                """,
                (adm_no,),
            )
            return self._fetchone_dict(cursor)
        finally:
            conn.close()

    def update_student(self, adm_no: int, updates: dict[str, Any]) -> bool:
        if not updates:
            return False

        allowed_fields = {
            "st_name": "st_name",
            "class": "class",
            "sec": "sec",
            "cont_no": "cont_no",
        }

        set_clauses: list[str] = []
        values: list[Any] = []
        for key, value in updates.items():
            if key in allowed_fields:
                set_clauses.append(f"{allowed_fields[key]} = %s")
                values.append(value)

        if not set_clauses:
            return False

        conn = get_connection(self.settings)
        try:
            cursor = conn.cursor()
            values.append(adm_no)
            cursor.execute(
                f"UPDATE fee_det SET {', '.join(set_clauses)} WHERE adm_no = %s",
                tuple(values),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def update_fee_submission(self, adm_no: int, amount_submitted: int, subm_month: str, payment_date) -> bool:
        conn = get_connection(self.settings)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE fee_det
                SET amt_submited = %s, subm_month = %s, date_paymnt = %s
                WHERE adm_no = %s
                """,
                (amount_submitted, subm_month, payment_date, adm_no),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_student(self, adm_no: int) -> bool:
        conn = get_connection(self.settings)
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fee_det WHERE adm_no = %s", (adm_no,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
