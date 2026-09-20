import pytest


@pytest.fixture
def sample_sections():
    return [
        {
            "heading": "Motor Mounting",
            "content": [
                "Mount the motors using four M3 screws.",
                "Secure the motor before attaching the gearbox.",
            ],
        },
        {
            "heading": "Battery Selection",
            "content": [
                "Use a 4S LiPo battery for the competition robot.",
            ],
        },
    ]


@pytest.fixture
def sample_chunks():
    return [
        {
            "id": "test.docx:0",
            "source": "test.docx",
            "heading": "Motor Mounting",
            "text": (
                "Mount the motors using four M3 screws.\n"
                "Secure the motor before attaching the gearbox."
            ),
        },
        {
            "id": "test.docx:1",
            "source": "test.docx",
            "heading": "Battery Selection",
            "text": "Use a 4S LiPo battery for the competition robot.",
        },
    ]


@pytest.fixture
def sample_retrieved_chunks():
    return [
        {
            "text": "Mount the motors.",
            "metadata": {
                "source": "chassis.docx",
                "heading": "Motor Mounting",
            },
        },
        {
            "text": "Use a 4S battery.",
            "metadata": {
                "source": "battery.docx",
                "heading": "Battery Selection",
            },
        },
    ]
