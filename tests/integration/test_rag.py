from src import rag
from src.llm import openai_client


def test_answer_question_runs_retrieval_and_generation(
    mocker,
    sample_retrieved_chunks,
):
    mock_retriever = mocker.Mock()

    mock_retriever.retrieve.return_value = sample_retrieved_chunks

    fake_response = mocker.Mock()
    fake_response.output_text = (
        "Use a 4S LiPo battery for the competition robot.[2]"
    )

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    result = rag.answer_question(
        question="What battery should we use?",
        retriever=mock_retriever,
    )

    mock_retriever.retrieve.assert_called_once_with(
        "What battery should we use?"
    )

    mock_client.responses.create.assert_called_once()

    assert result == (
        "Use a 4S LiPo battery for the competition robot.[2]\n\n"
        " *Sources:*\n"
        "[2] `battery.docx` — Battery Selection"
    )


def test_answer_question_passes_conversation_context(
    mocker,
    sample_retrieved_chunks,
):
    mock_retriever = mocker.Mock()
    mock_retriever.retrieve.return_value = sample_retrieved_chunks

    fake_response = mocker.Mock()
    fake_response.output_text = "Use a 4S battery.[2]"

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    conversation_context = (
        "We previously discussed using a 4S LiPo battery."
    )

    result = rag.answer_question(
        question="What battery did we discuss?",
        retriever=mock_retriever,
        conversation_context=conversation_context,
    )

    assert result == (
        "Use a 4S battery.[2]\n\n"
        " *Sources:*\n"
        "[2] `battery.docx` — Battery Selection"
    )

    call_kwargs = mock_client.responses.create.call_args.kwargs

    assert conversation_context in call_kwargs["input"]


def test_answer_question_returns_answer_without_sources_when_no_citations(
    mocker,
    sample_retrieved_chunks,
):
    mock_retriever = mocker.Mock()
    mock_retriever.retrieve.return_value = sample_retrieved_chunks

    fake_response = mocker.Mock()
    fake_response.output_text = (
        "The documentation does not specify the exact torque."
    )

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    result = rag.answer_question(
        question="What torque should I use?",
        retriever=mock_retriever,
    )

    assert result == (
        "The documentation does not specify the exact torque."
    )