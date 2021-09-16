import pytest
import sys
sys.path.append("./soil-moisture-sensor")
import app

def test_app():
    pass

def test_connection_string_exists():
    with pytest.raises(ValueError) as e_info:
        app.initialise("")