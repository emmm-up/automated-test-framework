# API Documentation

This project provides a pytest-based API automation framework built around
`framework.base.APIClient`, shared configuration, logging, and helper utilities.

## APIClient

```python
from framework.base import APIClient

client = APIClient(
    base_url="https://jsonplaceholder.typicode.com",
    timeout=30,
    headers={"Content-Type": "application/json"},
)
```

| Method | Description |
| --- | --- |
| `get(endpoint, params=None, **kwargs)` | Send a GET request. |
| `post(endpoint, data=None, json=None, **kwargs)` | Send a POST request. |
| `put(endpoint, data=None, json=None, **kwargs)` | Send a PUT request. |
| `patch(endpoint, data=None, json=None, **kwargs)` | Send a PATCH request. |
| `delete(endpoint, **kwargs)` | Send a DELETE request. |
| `close()` | Close the underlying session. |

All request helpers return a `requests.Response` object. Status failures are
raised through `response.raise_for_status()`.

## Configuration

`framework.config.Settings` loads configuration from environment variables or
`.env`.

| Setting | Environment variable | Default |
| --- | --- | --- |
| `BASE_URL` | `BASE_URL` | `https://jsonplaceholder.typicode.com` |
| `API_TIMEOUT` | `API_TIMEOUT` | `30` |
| `REQUEST_RETRIES` | `REQUEST_RETRIES` | `3` |
| `LOG_LEVEL` | `LOG_LEVEL` | `INFO` |
| `LOG_DIR` | `LOG_DIR` | `logs` |
| `REPORT_DIR` | `REPORT_DIR` | `allure-results` |

## Helper Utilities

```python
from framework.utils import Helper
```

| Function | Description |
| --- | --- |
| `json_to_dict(json_str)` | Parse a JSON string into a dictionary. |
| `dict_to_json(data, indent=2)` | Serialize a dictionary to JSON. |
| `get_nested_value(data, keys, separator=".")` | Read dotted paths from nested dictionaries. |
| `set_nested_value(data, keys, value, separator=".")` | Write dotted paths into nested dictionaries. |
| `list_to_dict(data, key)` | Index a list of dictionaries by a field. |
| `dict_difference(dict1, dict2)` | Compare two dictionaries. |
| `random_string(length=8, alphabet=...)` | Generate random test strings. |
| `merge_headers(*headers)` | Merge optional header dictionaries. |
| `chunk_list(items, size)` | Split iterables into fixed-size chunks. |
| `redact_sensitive(data, sensitive_keys=None, replacement="***")` | Mask sensitive fields before logging. |
| `validate_required_fields(data, fields)` | Return missing or empty required fields. |

## CI/CD

The GitHub Actions workflow runs on pushes to `main` and `dev`, pull requests
to `main`, and manual dispatch. It installs dependencies, runs `ruff`, executes
the pytest suite with coverage, and uploads `coverage.xml` as an artifact.
