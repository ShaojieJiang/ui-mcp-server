"""Models for UI components."""

import uuid
from datetime import date, time
from pathlib import Path
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


class ColorPicker(InputComponent):
    """Configuration for color picker components."""

    type: Literal["color_picker"]
    """UI component type."""
    value: str | None = None
    """Initial hex value of the component."""


class DateInput(InputComponent):
    """Configuration for date input components."""

    type: Literal["date_input"]
    """UI component type."""
    min_value: date | None = None
    """Minimum date for the component."""
    max_value: date | None = None
    """Maximum date for the component."""
    format: Literal["YYYY/MM/DD", "DD/MM/YYYY", "MM/DD/YYYY"]
    """Format of the date."""
    value: date | None = None
    """Initial date of the component."""


class TimeInput(InputComponent):
    """Configuration for time input components."""

    type: Literal["time_input"]
    """UI component type."""
    value: time | None = None
    """Initial time of the component."""
    step: int = 15 * 60
    """Step for the component in seconds."""


class AudioInput(InputComponent):
    """Configuration for audio input components."""

    type: Literal["audio_input"]
    """UI component type."""


class CameraInput(InputComponent):
    """Configuration for camera input components."""

    type: str = "camera_input"
    """UI component type."""


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


class AudioOutput(OutputComponent):
    """Configuration for audio output components."""

    type: Literal["audio"]
    """UI component type."""
    url: str | Path
    """URL or path of the media."""
    format: Literal["audio/mp3", "audio/wav", "audio/ogg"]
    """Format of the audio."""
    sample_rate: int | None = None
    """Sample rate of the audio."""
    loop: bool = False
    """Whether to loop the audio."""
    autoplay: bool = False
    """Whether to auto play the audio."""


class VideoOutput(OutputComponent):
    """Configuration for video output components."""

    type: str = "video"
    """UI component type."""
    url: str | Path
    """URL or path of the video."""
    format: Literal["video/mp4", "video/webm", "video/ogg"]
    """Format of the video."""
    subtitles: str | None = None
    """Subtitles of the video."""
    muted: bool = False
    """Whether to mute the video."""
    loop: bool = False
    """Whether to loop the video."""
    autoplay: bool = False
    """Whether to auto play the video."""


class ImageOutput(OutputComponent):
    """Configuration for image output components."""

    type: str = "image"
    """UI component type."""
    url: str | Path
    """URL or path of the image."""
    caption: str | None = None
    """Caption of the image."""
    width: int | None = None
    """Width of the image."""
    clamp: bool | None = None
    """Whether to clamp the image."""
    channels: Literal["RGB", "RGBA"]
    """Channels of the image."""
    output_format: Literal["auto", "JPEG", "PNG", "WEBP"]
    """Output format of the image."""
