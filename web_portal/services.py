from __future__ import annotations

from datetime import date
from typing import Any

from .repository import FeeRepository


class ValidationError(ValueError):
    pass


MONTHS = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
]


def fee_per_month(student_class: int) -> int:
    if 1 <= student_class <= 5:
        return 1000
    if 6 <= student_class <= 8:
        return 1700
    if 9 <= student_class <= 10:
        return 2500
    if 11 <= student_class <= 12:
        return 2970
    raise ValidationError("class must be in range 1-12")


def submitted_month(total_amount: int, monthly_fee: int) -> str:
    month_index = min(max(total_amount // monthly_fee, 1), 12) - 1
    return MONTHS[month_index]


class FeeService:
    def __init__(self, repository: FeeRepository) -> None:
        self.repository = repository

    def validate_student_payload(self, payload: dict[str, Any], *, updating: bool = False) -> dict[str, Any]:
        cleaned: dict[str, Any] = {}

        def _get(name: str):
            return payload.get(name)

        if not updating:
            try:
                cleaned["adm_no"] = int(_get("adm_no"))
            except (TypeError, ValueError):
                raise ValidationError("adm_no must be an integer")

        if "st_name" in payload or not updating:
            st_name = str(_get("st_name") or "").strip()
            if not st_name or any(not (ch.isalpha() or ch.isspace()) for ch in st_name):
                raise ValidationError("st_name must contain letters and spaces only")
            cleaned["st_name"] = st_name

        if "class" in payload or not updating:
            try:
                class_value = int(_get("class"))
            except (TypeError, ValueError):
                raise ValidationError("class must be an integer")
            fee_per_month(class_value)
            cleaned["class"] = class_value

        if "sec" in payload or not updating:
            sec = str(_get("sec") or "").strip().upper()
            if len(sec) != 1 or not sec.isalpha():
                raise ValidationError("sec must be a single alphabetic character")
            cleaned["sec"] = sec

        if "cont_no" in payload or not updating:
            cont = str(_get("cont_no") or "").strip()
            if not cont.isdigit() or len(cont) != 10:
                raise ValidationError("cont_no must be a 10-digit number")
            cleaned["cont_no"] = int(cont)

        return cleaned

    def add_student(self, payload: dict[str, Any]) -> dict[str, Any]:
        cleaned = self.validate_student_payload(payload)
        existing = self.repository.get_student(cleaned["adm_no"])
        if existing:
            raise ValidationError("adm_no already exists")
        self.repository.create_student(cleaned)
        return self.repository.get_student(cleaned["adm_no"])

    def get_student(self, adm_no: int) -> dict[str, Any] | None:
        return self.repository.get_student(adm_no)

    def update_student(self, adm_no: int, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.repository.get_student(adm_no):
            raise ValidationError("student not found")
        cleaned = self.validate_student_payload(payload, updating=True)
        if not cleaned:
            raise ValidationError("no valid fields provided for update")
        self.repository.update_student(adm_no, cleaned)
        return self.repository.get_student(adm_no)

    def delete_student(self, adm_no: int) -> bool:
        return self.repository.delete_student(adm_no)

    def submit_fee(self, adm_no: int, paid_amount: int) -> dict[str, Any]:
        student = self.repository.get_student(adm_no)
        if not student:
            raise ValidationError("student not found")
        if paid_amount <= 0:
            raise ValidationError("paid_amount must be positive")

        monthly_fee = fee_per_month(int(student["class"]))
        if paid_amount < monthly_fee:
            raise ValidationError(f"paid_amount must be at least {monthly_fee}")

        adjusted_paid = (paid_amount // monthly_fee) * monthly_fee
        refund = paid_amount - adjusted_paid

        new_total = int(student["amt_submited"]) + adjusted_paid
        max_amount = monthly_fee * 12
        if new_total > max_amount:
            refund += new_total - max_amount
            new_total = max_amount

        month = submitted_month(new_total, monthly_fee)
        today = date.today()
        updated = self.repository.update_fee_submission(adm_no, new_total, month, today)
        if not updated:
            raise ValidationError("unable to submit fee")

        return {
            "student": self.repository.get_student(adm_no),
            "monthly_fee": monthly_fee,
            "accepted_amount": adjusted_paid,
            "refund_amount": refund,
        }
