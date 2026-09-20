from src.llm import openai_client


def test_build_document_context(sample_retrieved_chunks):
    result = openai_client.build_document_context(
        sample_retrieved_chunks
    )

    assert result == (
        "Source: chassis.docx\n"
        "Heading: Motor Mounting\n"
        "Mount the motors.\n\n"
        "Source: battery.docx\n"
        "Heading: Battery Selection\n"
        "Use a 4S battery."
    )


def test_build_document_context_empty_chunks():
    result = openai_client.build_document_context([])

    assert result == ""


def test_build_source_list_returns_only_cited_sources(
    sample_retrieved_chunks,
):
    result = openai_client.build_source_list(
        sample_retrieved_chunks,
        {1},
    )

    assert result == (
        "[1] `chassis.docx` — Motor Mounting"
    )


def test_build_source_list_returns_empty_string_when_nothing_is_cited(
    sample_retrieved_chunks,
):
    result = openai_client.build_source_list(
        sample_retrieved_chunks,
        set(),
    )

    assert result == ""


def test_get_cited_source_numbers():
    answer = (
        "The robot uses a 4S battery.[2] "
        "The motors require M3 screws.[1][3]"
    )

    result = openai_client.get_cited_source_numbers(answer)

    assert result == {1, 2, 3}


def test_get_cited_source_numbers_returns_empty_set_without_citations():
    answer = "The robot uses a 4S battery."

    result = openai_client.get_cited_source_numbers(answer)

    assert result == set()


def test_generate_answer_returns_answer_without_sources_when_no_citations(
    mocker,
    sample_retrieved_chunks,
):
    fake_response = mocker.Mock()
    fake_response.output_text = (
        "The motors should be mounted using M3 screws."
    )

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    result = openai_client.generate_answer(
        question="How should I mount the motors?",
        chunks=sample_retrieved_chunks,
    )

    assert result == (
        "The motors should be mounted using M3 screws."
    )

    mock_client.responses.create.assert_called_once()


def test_generate_answer_appends_cited_sources(
    mocker,
    sample_retrieved_chunks,
):
    fake_response = mocker.Mock()
    fake_response.output_text = (
        "Mount the motors using four M3 screws.[1]"
    )

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    result = openai_client.generate_answer(
        question="How should I mount the motors?",
        chunks=sample_retrieved_chunks,
    )

    assert result == (
        "Mount the motors using four M3 screws.[1]\n\n"
        " *Sources:*\n"
        "[1] `chassis.docx` — Motor Mounting"
    )


def test_generate_answer_passes_question_and_documentation_to_openai(
    mocker,
    sample_retrieved_chunks,
):
    fake_response = mocker.Mock()
    fake_response.output_text = "The answer is [1]."

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    openai_client.generate_answer(
        question="How should I mount the motors?",
        chunks=sample_retrieved_chunks,
    )

    call_kwargs = mock_client.responses.create.call_args.kwargs

    assert call_kwargs["model"] == openai_client.MODEL

    assert (
        "How should I mount the motors?"
        in call_kwargs["input"]
    )

    assert "Motor Mounting" in call_kwargs["input"]
    assert "Mount the motors." in call_kwargs["input"]


def test_generate_answer_includes_conversation_context(
    mocker,
    sample_retrieved_chunks,
):
    fake_response = mocker.Mock()
    fake_response.output_text = "Use the 4S battery.[2]"

    mock_client = mocker.Mock()
    mock_client.responses.create.return_value = fake_response

    mocker.patch.object(
        openai_client,
        "client",
        mock_client,
    )

    conversation_context = (
        "We discussed using a 4S LiPo battery."
    )

    openai_client.generate_answer(
        question="What battery did we discuss?",
        chunks=sample_retrieved_chunks,
        conversation_context=conversation_context,
    )

    call_kwargs = mock_client.responses.create.call_args.kwargs

    assert (
        "Conversation history from the Slack thread:"
        in call_kwargs["input"]
    )

    assert conversation_context in call_kwargs["input"]