from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as backend_app


_BASELINE_ACTIVITIES = deepcopy(backend_app.activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities before and after each test for isolation."""
    backend_app.activities.clear()
    backend_app.activities.update(deepcopy(_BASELINE_ACTIVITIES))

    yield

    backend_app.activities.clear()
    backend_app.activities.update(deepcopy(_BASELINE_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(backend_app.app)
