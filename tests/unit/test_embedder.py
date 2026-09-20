import numpy as np

from src.ingestion import embedder


def test_embed_text(mocker):
    mock_model = mocker.Mock()
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])

    mocker.patch.object(embedder, "model", mock_model)

    result = embedder.embed_text("hello world")

    assert result == [0.1, 0.2, 0.3]

    mock_model.encode.assert_called_once_with("hello world")


def test_embed_chunks(mocker, sample_chunks):
    mock_model = mocker.Mock()
    mock_model.encode.return_value = np.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]
    )

    mocker.patch.object(embedder, "model", mock_model)

    result = embedder.embed_chunks(sample_chunks)

    mock_model.encode.assert_called_once_with(
        [
            (
                "Motor Mounting\n"
                "Mount the motors using four M3 screws.\n"
                "Secure the motor before attaching the gearbox."
            ),
            (
                "Battery Selection\n"
                "Use a 4S LiPo battery for the competition robot."
            ),
        ]
    )

    assert result[0]["embedding"] == [0.1, 0.2, 0.3]
    assert result[1]["embedding"] == [0.4, 0.5, 0.6]


def test_embed_chunks_adds_embeddings_without_removing_chunk_data(
    mocker,
    sample_chunks,
):
    mock_model = mocker.Mock()
    mock_model.encode.return_value = np.array(
        [
            [0.1, 0.2],
            [0.3, 0.4],
        ]
    )

    mocker.patch.object(embedder, "model", mock_model)

    result = embedder.embed_chunks(sample_chunks)

    assert result[0]["id"] == "test.docx:0"
    assert result[0]["source"] == "test.docx"
    assert result[0]["heading"] == "Motor Mounting"
    assert result[0]["text"] == (
        "Mount the motors using four M3 screws.\n"
        "Secure the motor before attaching the gearbox."
    )

    assert result[1]["id"] == "test.docx:1"
    assert result[1]["source"] == "test.docx"
    assert result[1]["heading"] == "Battery Selection"