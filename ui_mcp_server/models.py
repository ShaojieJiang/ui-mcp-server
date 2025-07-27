"""Models for UI components."""

import uuid
from typing import Any, Literal
from pydantic import BaseModel, Field


class BaseComponent(BaseModel, use_attribute_docstrings=True):
    """Base configuration for UI components."""

    type: str
    """Type identifier for the UI component."""
    key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    """Unique identifier for the component."""


class InputComponent(BaseComponent):
    """Configuration for user input components."""

    label: str
    """Label of the component for the user to see."""
    help: str | None = None
    """Optional help text for the component."""
    user_input: Any | None = None
    """User-provided answer for the component."""


class OutputComponent(BaseComponent):
    """Configuration for output components. Reserved for future implementation."""

    pass


class NumberInput(InputComponent):
    """Parameters for number input components."""

    type: Literal["number_input", "slider"]
    """UI component type."""
    min_value: int | float | None = None
    """Minimum value for the component."""
    max_value: int | float | None = None
    """Maximum value for the component."""
    step: int | float | None = None
    """Step for the component."""
    user_input: int | float | None = None
    """Value input by the user for the component."""


class Choice(InputComponent):
    """Configuration for selection-based input components."""

    type: Literal["radio", "multiselect"]
    """UI component type."""
    options: list[str]
    """Available selection options."""
    user_input: int | str | list[str] | None = None
    """Selected value(s) from the options."""


class TableOutput(OutputComponent):
    """Parameters for table output components. Be sure to generate a list of dictionaries as the `data` field."""  # noqa: E501

    type: Literal["table"]
    """UI component type."""
    data: list[dict]
    """List of JSON objects for the component."""
