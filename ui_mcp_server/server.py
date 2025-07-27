"""Tools for UI components."""

from mcp.server.fastmcp import FastMCP
from ui_mcp_server.models import (
    AudioInput,
    AudioOutput,
    CameraInput,
    Chart,
    Choice,
    ColorPicker,
    DateInput,
    ImageOutput,
    NumberInput,
    TimeInput,
    VideoOutput,
)


server = FastMCP("ui-mcp-server")


@server.prompt()
def ui_component_prompt() -> str:  # pragma: no cover
    """Predefined prompt for UI component generation."""
    return "Use the tools from the ui-mcp-server to generate a UI components, which will be used in a frontend application. When tools are called, the next response should be something very short and concise."  # noqa: E501


@server.tool()
def number_input(params: NumberInput) -> NumberInput:
    """Generate a number input component.

    Args:
        params: Parameters for the number input component.
    """
    return params


@server.tool()
def choice(params: Choice) -> Choice:
    """Generate a choice input component.

    Args:
        params: Parameters for the choice input component.
    """
    return params


@server.tool()
def chart(params: Chart) -> Chart:
    """Generate a chart component.

    Args:
        params: Parameters for the chart component.
    """
    return params


@server.tool()
def color_picker(params: ColorPicker) -> ColorPicker:
    """Generate a color picker component.

    Args:
        params: Parameters for the color picker component.
    """
    return params


@server.tool()
def date_input(params: DateInput) -> DateInput:
    """Generate a date input component.

    Args:
        params: Parameters for the date input component.
    """
    return params


@server.tool()
def time_input(params: TimeInput) -> TimeInput:
    """Generate a time input component.

    Args:
        params: Parameters for the time input component.
    """
    return params


@server.tool()
def audio_input(params: AudioInput) -> AudioInput:
    """Generate an audio input component.

    Args:
        params: Parameters for the audio input component.
    """
    return params


@server.tool()
def camera_input(params: CameraInput) -> CameraInput:
    """Generate a camera input component.

    Args:
        params: Parameters for the camera input component.
    """
    return params


@server.tool()
def audio_output(params: AudioOutput) -> AudioOutput:
    """Generate an audio output component.

    Args:
        params: Parameters for the audio output component.
    """
    return params


@server.tool()
def video_output(params: VideoOutput) -> VideoOutput:
    """Generate a video output component.

    Args:
        params: Parameters for the video output component.
    """
    return params


@server.tool()
def image_output(params: ImageOutput) -> ImageOutput:
    """Generate an image output component.

    Args:
        params: Parameters for the image output component.
    """
    return params


if __name__ == "__main__":
    server.run()
