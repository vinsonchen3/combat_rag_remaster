from pathlib import Path

from src.ingestion.chunker import chunk_document


def test_chunk_document_transforms_sections_into_chunks(
    mocker,
    sample_sections,
):
    mocker.patch(
        "src.ingestion.chunker.docx_to_sections",
        return_value=sample_sections,
    )

    path = Path("/documents/test.docx")

    chunks = chunk_document(path)

    assert chunks == [
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


def test_chunk_document_skips_empty_sections(mocker):
    sections = [
        {
            "heading": "Empty Section",
            "content": [],
        },
        {
            "heading": "Motor Mounting",
            "content": ["Mount the motors."],
        },
    ]

    mocker.patch(
        "src.ingestion.chunker.docx_to_sections",
        return_value=sections,
    )

    chunks = chunk_document(Path("/documents/test.docx"))

    assert chunks == [
        {
            "id": "test.docx:1",
            "source": "test.docx",
            "heading": "Motor Mounting",
            "text": "Mount the motors.",
        }
    ]


def test_chunk_document_calls_parser_with_given_path(mocker):
    mock_parser = mocker.patch(
        "src.ingestion.chunker.docx_to_sections",
        return_value=[],
    )

    path = Path("/documents/test.docx")

    chunk_document(path)

    mock_parser.assert_called_once_with(path)