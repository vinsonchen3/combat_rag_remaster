import pytest


@pytest.fixture
def sample_sections():
    return [
        {
            "id": "section-1",
            "source": "chassis.docx",
            "heading": "Motor Mounting",
            "text": "Mount the motors using four M3 screws.",
        },
        {
            "id": "section-2",
            "source": "battery.docx",
            "heading": "Battery Selection",
            "text": "Use a 4S LiPo battery for the competition robot.",
        },
    ]


@pytest.fixture
def sample_chunks():
    return [
        {
            "id": "section-1",
            "source": "chassis.docx",
            "heading": "Motor Mounting",
            "text": "Mount the motors using four M3 screws.",
        },
        {
            "id": "section-2",
            "source": "battery.docx",
            "heading": "Battery Selection",
            "text": "Use a 4S LiPo battery for the competition robot.",
        },
    ]
