import types
import pytest
from unittest.mock import Mock
from control.auth_controller import AuthController

class DummyUser(types.SimpleNamespace):
    pass

@pytest.fixture
def repo():
    return Mock(spec_set=["get_user_by_credentials"])

@pytest.fixture
def controller(repo):
    return AuthController(repo)

def test_authenticate_success(controller, repo):
    user = DummyUser(id=1, username="alice", role="Admin")
    repo.get_user_by_credentials.return_value = user
    result = controller.authenticate("alice", "secret", "Admin")
    assert result is user
    repo.get_user_by_credentials.assert_called_once_with("alice", "secret", "Admin")

def test_authenticate_failure_returns_none(controller, repo):
    repo.get_user_by_credentials.return_value = None
    result = controller.authenticate("bob", "badpass", "Csr_Rep")
    assert result is None
    repo.get_user_by_credentials.assert_called_once_with("bob", "badpass", "Csr_Rep")
