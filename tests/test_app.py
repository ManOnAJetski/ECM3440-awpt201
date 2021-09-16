import pytest
import sys
sys.path.append("./soil-moisture-sensor")
import app

def test_app():
    pass

def test_connection_string_exists_otherwise_error_raised():
    with pytest.raises(ValueError) as e_info:
        app.initialise("")