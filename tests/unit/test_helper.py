import pytest

from framework.utils import Helper


def test_random_string_uses_requested_length():
    assert Helper.random_string(5, alphabet="a") == "aaaaa"


def test_random_string_rejects_negative_length():
    with pytest.raises(ValueError, match="length"):
        Helper.random_string(-1)


def test_merge_headers_ignores_none_and_uses_last_value():
    headers = Helper.merge_headers({"Accept": "json"}, None, {"Accept": "xml"})

    assert headers == {"Accept": "xml"}


def test_chunk_list_splits_iterables():
    assert Helper.chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_list_rejects_invalid_size():
    with pytest.raises(ValueError, match="size"):
        Helper.chunk_list([1], 0)


def test_redact_sensitive_masks_nested_values():
    payload = {"token": "abc", "user": {"password": "secret", "name": "Ada"}}

    assert Helper.redact_sensitive(payload) == {
        "token": "***",
        "user": {"password": "***", "name": "Ada"},
    }
