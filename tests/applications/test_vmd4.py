"""Test Axis VMD4 API.

pytest --cov-report term-missing --cov=axis.vmd4 tests/test_vmd4.py
"""

from asynctest import Mock
import pytest

from axis.applications.vmd4 import Vmd4


@pytest.fixture
def vmd4() -> Vmd4:
    """Returns the vmd4 mock object."""
    mock_request = Mock()
    mock_request.return_value = ""
    return Vmd4(mock_request)


def test_get_empty_configuration(vmd4):
    """Test empty get_configuration"""
    vmd4._request.return_value = response_get_configuration_empty
    vmd4.update()
    vmd4._request.assert_called_with(
        "post",
        "/local/vmd/control.cgi",
        json={
            "method": "getConfiguration",
            "apiVersion": "1.2",
            "context": "Axis library",
        },
    )

    assert len(vmd4.values()) == 0


def test_get_configuration(vmd4):
    """Test get_supported_versions"""
    vmd4._request.return_value = response_get_configuration
    vmd4.update()
    vmd4._request.assert_called_with(
        "post",
        "/local/vmd/control.cgi",
        json={
            "method": "getConfiguration",
            "apiVersion": "1.2",
            "context": "Axis library",
        },
    )

    assert len(vmd4.values()) == 1

    vmd4 = vmd4["Camera1Profile1"]
    assert vmd4.id == "Camera1Profile1"
    assert vmd4.name == "Profile 1"
    assert vmd4.camera == 1
    assert vmd4.uid == 1
    assert vmd4.triggers == [
        {
            "type": "includeArea",
            "data": [[-0.97, -0.97], [-0.97, 0.97], [0.97, 0.97], [0.97, -0.97],],
        }
    ]
    assert vmd4.filters == [
        {"data": 1, "active": True, "type": "timeShortLivedLimit"},
        {"data": 5, "active": True, "type": "distanceSwayingObject"},
        {"data": [5, 5], "active": True, "type": "sizePercentage"},
    ]


def test_get_configuration_error(vmd4):
    """Test empty get_configuration.

    _request returns an empty dict on error.
    """
    vmd4._request.return_value = {}
    vmd4.update()
    vmd4._request.assert_called_with(
        "post",
        "/local/vmd/control.cgi",
        json={
            "method": "getConfiguration",
            "apiVersion": "1.2",
            "context": "Axis library",
        },
    )

    assert len(vmd4.values()) == 0


response_get_configuration_empty = {
    "apiVersion": "1.4",
    "method": "getConfiguration",
    "context": "Axis library",
    "data": {
        "cameras": [{"id": 1, "rotation": 0, "active": True}],
        "configurationStatus": 26,
        "profiles": [],
    },
}


response_get_configuration = {
    "apiVersion": "1.4",
    "method": "getConfiguration",
    "context": "Axis library",
    "data": {
        "cameras": [{"id": 1, "rotation": 0, "active": True}],
        "configurationStatus": 2,
        "profiles": [
            {
                "filters": [
                    {"data": 1, "active": True, "type": "timeShortLivedLimit"},
                    {"data": 5, "active": True, "type": "distanceSwayingObject"},
                    {"data": [5, 5], "active": True, "type": "sizePercentage"},
                ],
                "camera": 1,
                "triggers": [
                    {
                        "type": "includeArea",
                        "data": [
                            [-0.97, -0.97],
                            [-0.97, 0.97],
                            [0.97, 0.97],
                            [0.97, -0.97],
                        ],
                    }
                ],
                "name": "Profile 1",
                "uid": 1,
            }
        ],
    },
}

response_get_configuration_error = {
    "apiVersion": "1.1",
    "method": "getConfiguration",
    "context": "Axis library",
    "error": {
        "code": "2000",
        "message": "The requested version of the application is not supported.",
    },
}

