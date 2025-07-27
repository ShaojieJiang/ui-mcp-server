"""Models for UI components."""

import uuid
from typing import Any, Literal
from pydantic import BaseModel, Field


class BaseComponent(BaseModel, use_attribute_docstrings=True):
    """Base configuration for UI components."""

    type: str
    """Type identifier for the UI component."""
    key: str = Field(default_factory=lambda: str(uuid.uuid4()), init=False)
    """Unique identifier for the component."""


class InputComponent(BaseComponent):
    """Configuration for user input components."""

    label: str
    """Label of the component for the user to see."""
    help: str | None = None
    """Optional help text for the component."""
    value: Any | None = None
    """Initial of the component."""


class OutputComponent(BaseComponent):
    """Configuration for output components. Reserved for future implementation."""

    pass


class NumberInput(InputComponent):
    """Parameters for number input components."""

    type: Literal["number_input", "slider"]
    """UI component type."""
    min_value: float | None = None
    """Minimum value for the component."""
    max_value: float | None = None
    """Maximum value for the component."""
    step: float | None = None
    """Step for the component."""
    value: float | None = None
    """Initial value of the component."""


class Choice(InputComponent):
    """Configuration for selection-based input components."""

    type: Literal["radio", "multiselect"]
    """UI component type."""
    options: list[str]
    """Available selection options."""
    value: int | str | list[str] | None = None
    """Initial value(s) from the options."""


class Chart(OutputComponent):
    """Parameters for chart components."""

    type: Literal["line", "bar", "scatter"]
    """UI component type."""
    data: list[int | float]
    """List of values for the component."""
    x_label: str
    """Label of the x-axis."""
    y_label: str
    """Label of the y-axis."""
