"""Tests for server functions and models."""

from datetime import date, time
from pathlib import Path
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
from ui_mcp_server.server import (
    audio_input,
    audio_output,
    camera_input,
    chart,
    choice,
    color_picker,
    date_input,
    image_output,
    number_input,
    time_input,
    video_output,
)


def test_number_input():
    """Test number_input function returns input unchanged."""
    params = NumberInput(
        type="number_input",
        label="Test Input",
        min_value=0,
        max_value=100,
        step=1,
        value=50,
        help="Test help",
    )

    result = number_input(params)

    assert result == params
    assert result.type == "number_input"
    assert result.label == "Test Input"
    assert result.min_value == 0
    assert result.max_value == 100
    assert result.step == 1
    assert result.value == 50
    assert result.help == "Test help"


def test_number_input_slider():
    """Test number_input with slider type."""
    params = NumberInput(
        type="slider", label="Slider Input", min_value=10, max_value=200
    )

    result = number_input(params)

    assert result == params
    assert result.type == "slider"


def test_choice_radio():
    """Test choice function with radio type."""
    params = Choice(
        type="radio",
        label="Test Choice",
        options=["Option A", "Option B", "Option C"],
        value="Option A",
    )

    result = choice(params)

    assert result == params
    assert result.type == "radio"
    assert result.label == "Test Choice"
    assert result.options == ["Option A", "Option B", "Option C"]
    assert result.value == "Option A"


def test_choice_multiselect():
    """Test choice function with multiselect type."""
    params = Choice(
        type="multiselect",
        label="Multi Choice",
        options=["A", "B", "C", "D"],
        value=["A", "C"],
    )

    result = choice(params)

    assert result == params
    assert result.type == "multiselect"
    assert result.value == ["A", "C"]


def test_chart():
    """Test chart function."""
    params = Chart(
        type="line", data=[1, 2, 3, 4, 5], x_label="X Axis", y_label="Y Axis"
    )

    result = chart(params)

    assert result == params
    assert result.type == "line"
    assert result.data == [1, 2, 3, 4, 5]
    assert result.x_label == "X Axis"
    assert result.y_label == "Y Axis"


def test_chart_bar():
    """Test chart function with bar type."""
    params = Chart(
        type="bar", data=[10.5, 20.3, 15.7], x_label="Categories", y_label="Values"
    )

    result = chart(params)

    assert result == params
    assert result.type == "bar"


def test_chart_scatter():
    """Test chart function with scatter type."""
    params = Chart(type="scatter", data=[1.1, 2.2, 3.3], x_label="X", y_label="Y")

    result = chart(params)

    assert result == params
    assert result.type == "scatter"


def test_color_picker():
    """Test color_picker function."""
    params = ColorPicker(
        type="color_picker", label="Pick Color", value="#FF0000", help="Choose a color"
    )

    result = color_picker(params)

    assert result == params
    assert result.type == "color_picker"
    assert result.label == "Pick Color"
    assert result.value == "#FF0000"
    assert result.help == "Choose a color"


def test_date_input():
    """Test date_input function."""
    test_date = date(2024, 1, 15)
    min_date = date(2024, 1, 1)
    max_date = date(2024, 12, 31)

    params = DateInput(
        type="date_input",
        label="Select Date",
        min_value=min_date,
        max_value=max_date,
        format="YYYY/MM/DD",
        value=test_date,
    )

    result = date_input(params)

    assert result == params
    assert result.type == "date_input"
    assert result.label == "Select Date"
    assert result.min_value == min_date
    assert result.max_value == max_date
    assert result.format == "YYYY/MM/DD"
    assert result.value == test_date


def test_date_input_formats():
    """Test date_input with different formats."""
    formats = ["DD/MM/YYYY", "MM/DD/YYYY"]

    for fmt in formats:
        params = DateInput(type="date_input", label="Date", format=fmt)
        result = date_input(params)
        assert result.format == fmt


def test_time_input():
    """Test time_input function."""
    test_time = time(14, 30, 0)

    params = TimeInput(
        type="time_input",
        label="Select Time",
        value=test_time,
        step=900,  # 15 minutes
    )

    result = time_input(params)

    assert result == params
    assert result.type == "time_input"
    assert result.label == "Select Time"
    assert result.value == test_time
    assert result.step == 900


def test_audio_input():
    """Test audio_input function."""
    params = AudioInput(
        type="audio_input", label="Record Audio", help="Record your voice"
    )

    result = audio_input(params)

    assert result == params
    assert result.type == "audio_input"
    assert result.label == "Record Audio"
    assert result.help == "Record your voice"


def test_camera_input():
    """Test camera_input function."""
    params = CameraInput(type="camera_input", label="Take Photo")

    result = camera_input(params)

    assert result == params
    assert result.type == "camera_input"
    assert result.label == "Take Photo"


def test_audio_output():
    """Test audio_output function."""
    params = AudioOutput(
        type="audio",
        url="https://example.com/audio.mp3",
        format="audio/mp3",
        sample_rate=44100,
        loop=True,
        autoplay=False,
    )

    result = audio_output(params)

    assert result == params
    assert result.type == "audio"
    assert result.url == "https://example.com/audio.mp3"
    assert result.format == "audio/mp3"
    assert result.sample_rate == 44100
    assert result.loop is True
    assert result.autoplay is False


def test_audio_output_path():
    """Test audio_output with Path."""
    path = Path("/path/to/audio.wav")
    params = AudioOutput(type="audio", url=path, format="audio/wav")

    result = audio_output(params)

    assert result == params
    assert result.url == path


def test_video_output():
    """Test video_output function."""
    params = VideoOutput(
        type="video",
        url="https://example.com/video.mp4",
        format="video/mp4",
        subtitles="English subtitles",
        muted=True,
        loop=False,
        autoplay=True,
    )

    result = video_output(params)

    assert result == params
    assert result.type == "video"
    assert result.url == "https://example.com/video.mp4"
    assert result.format == "video/mp4"
    assert result.subtitles == "English subtitles"
    assert result.muted is True
    assert result.loop is False
    assert result.autoplay is True


def test_video_output_formats():
    """Test video_output with different formats."""
    formats = ["video/webm", "video/ogg"]

    for fmt in formats:
        params = VideoOutput(type="video", url="test.video", format=fmt)
        result = video_output(params)
        assert result.format == fmt


def test_image_output():
    """Test image_output function."""
    params = ImageOutput(
        type="image",
        url="https://example.com/image.png",
        caption="Test Image",
        width=800,
        clamp=True,
        channels="RGBA",
        output_format="PNG",
    )

    result = image_output(params)

    assert result == params
    assert result.type == "image"
    assert result.url == "https://example.com/image.png"
    assert result.caption == "Test Image"
    assert result.width == 800
    assert result.clamp is True
    assert result.channels == "RGBA"
    assert result.output_format == "PNG"


def test_image_output_formats():
    """Test image_output with different formats."""
    formats = ["auto", "JPEG", "WEBP"]

    for fmt in formats:
        params = ImageOutput(
            type="image", url="test.jpg", channels="RGB", output_format=fmt
        )
        result = image_output(params)
        assert result.output_format == fmt


def test_image_output_channels():
    """Test image_output with RGB channels."""
    params = ImageOutput(
        type="image",
        url=Path("/path/to/image.jpg"),
        channels="RGB",
        output_format="JPEG",
    )

    result = image_output(params)

    assert result == params
    assert result.channels == "RGB"


def test_base_component_key_generation():
    """Test that BaseComponent generates unique keys."""
    comp1 = NumberInput(type="number_input", label="Test 1")
    comp2 = NumberInput(type="number_input", label="Test 2")

    assert comp1.key != comp2.key
    assert len(comp1.key) > 0
    assert len(comp2.key) > 0
