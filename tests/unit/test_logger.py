from framework.utils.logger import logger


def test_logger_exposes_expected_methods():
    for method_name in ["debug", "info", "warning", "error", "critical"]:
        assert hasattr(logger, method_name)


def test_logger_can_bind_context():
    bound_logger = logger.bind(request_id="abc-123")

    assert bound_logger is not None
