from framework.utils import Helper


def test_required_field_validation_accepts_complete_payload():
    missing = Helper.validate_required_fields({"id": 1, "name": "Ada"}, ["id", "name"])

    assert missing == []


def test_required_field_validation_returns_missing_and_empty_fields():
    missing = Helper.validate_required_fields({"id": 1, "name": ""}, ["id", "name", "email"])

    assert missing == ["name", "email"]


def test_dict_difference_reports_added_removed_and_modified_values():
    diff = Helper.dict_difference({"id": 1, "role": "user"}, {"id": 1, "role": "admin", "active": True})

    assert diff == {
        "added": {"active": True},
        "removed": {},
        "modified": {"role": {"old": "user", "new": "admin"}},
    }
