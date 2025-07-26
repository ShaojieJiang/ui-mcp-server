"""Tests for server functions."""

from ui_mcp_server.models import Choice, NumberInput, TableOutput
from ui_mcp_server.server import choice, number_input, table_output


def test_number_input():
    """Test number_input function returns input unchanged."""
    params = NumberInput(
        type="number_input", label="Test Input", min_value=0, max_value=100, step=1
    )

    result = number_input(params)

    assert result == params
    assert result.type == "number_input"
    assert result.label == "Test Input"
    assert result.min_value == 0
    assert result.max_value == 100
    assert result.step == 1


def test_choice():
    """Test choice function returns input unchanged."""
    params = Choice(
        type="radio", label="Test Choice", options=["Option A", "Option B", "Option C"]
    )

    result = choice(params)

    assert result == params
    assert result.type == "radio"
    assert result.label == "Test Choice"
    assert result.options == ["Option A", "Option B", "Option C"]


def test_table_output():
    """Test table_output function returns input unchanged."""
    params = TableOutput(
        data=[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    )

    result = table_output(params)

    assert result == params
    assert result.type == "dataframe"
    assert result.data == [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
