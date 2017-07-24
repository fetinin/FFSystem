from datetime import date
import re

from database.enums import Roles, Statuses

SUCCESS_VALIDATION_MSG = "Everything's fine."


class ValidatorMixin:
    validators = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

    def __setattr__(self, key, value):
        validator = self.validators.get(key, None)
        if validator:
            is_valid, msg = validator(value)
            if not is_valid:
                raise AttributeError(msg)
        super().__setattr__(key, value)

    @classmethod
    def _attr_is_nullable(cls, attr_name) -> bool:
        return getattr(cls, attr_name).property.columns[0].nullable

    def validate(self) -> (bool, str):
        is_valid, msg = True, SUCCESS_VALIDATION_MSG

        for attr_name, validator in self.validators.items():
            value = getattr(self, attr_name)
            if not value and not self._attr_is_nullable(attr_name):
                    is_valid, msg = False, f"{attr_name.title()} is required."
                    break
            elif value:
                is_valid, msg = validator(value)
                if not is_valid:
                    break
            else:
                continue

        if not is_valid:
            raise AttributeError(msg)


def is_name(value: str) -> (bool, str):
    if re.compile(r"^[a-zA-Z0-9_-]{3,40}$").match(value):
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Name should contain only letters, numbers or _."


def is_email(value: str) -> (bool, str):
    if re.compile(r'^[\S]+@[\S]+\.[\S]+$').match(value):
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Invalid email address."


def is_password(value: str) -> (bool, str):
    if len(value) >= 3:
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Password should be at least 3 characters long."


def is_role(value: str) -> (bool, str):
    possible_roles = [role.value for role in Roles]
    if value in possible_roles:
        return True, SUCCESS_VALIDATION_MSG
    else:
        roll_choices = ", ".join(possible_roles)
        return False, f"Role should be one of these: {roll_choices}"


def is_credit_card(value: str) -> (bool, str):
    def is_luhn_valid(card_number: str) -> bool:
        card_number = [int(i) for i in str(card_number)]

        card_len = len(card_number)
        start = 0 if card_len % 2 == 0 else 1

        for index in range(start, card_len, 2):
            card_number[index] *= 2
            if card_number[index] > 9:
                card_number[index] -= 9

        return sum(card_number) % 10 == 0

    all_digits = all(l.isdigit() for l in value)
    if all_digits and len(value) >= 16 and is_luhn_valid(value):
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Credit card number should be at least 16 digits " \
                      "long and be valid."


def is_link(value: str) -> (bool, str):
    if value.startswith(("http", "/")):
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Invalid link. Should start with http or '/'."


def is_description(value: str) -> (bool, str):
    if len(value) >= 10:
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Description"


def is_not_empty(value: str) -> (bool, str):
    if value:
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Value shouldn't be empty."


def are_all_digits(value: str) -> (bool, str):
    if all(s.isdigit() for s in value):
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "Price should contain only numbers."


def date_is_not_past(value: date) -> (bool, str):
    if value >= date.today():
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, "You can't be from the past, so are dates."


def is_project_status(value: str) -> (bool, str):
    possible_statuses = [role.value for role in Statuses]
    if value in possible_statuses:
        return True, SUCCESS_VALIDATION_MSG
    else:
        roll_choices = ", ".join(possible_statuses)
        return False, f"Status can be one of these: {roll_choices}"


def is_archive(value: str) -> (bool, str):
    supported_formats = ".zip", ".tar", ".rar"
    if value.endswith(supported_formats):
        return True, SUCCESS_VALIDATION_MSG
    else:
        return False, f"Invalid format. Please upload one of these: " \
                      f"{', '.join(supported_formats)}."
