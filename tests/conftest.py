import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_attendance_repo():
    return MagicMock()


@pytest.fixture
def mock_device_repo():
    return MagicMock()


@pytest.fixture
def mock_student_repo():
    return MagicMock()


@pytest.fixture
def mock_notification_repo():
    return MagicMock()
