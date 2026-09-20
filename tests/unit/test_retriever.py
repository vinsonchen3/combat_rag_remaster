from src.retrieval.retriever import Retriever


def test_retrieve_encodes_query_and_queries_collection(mocker):
    model = mocker.Mock()
    collection = mocker.Mock()

    model.encode.return_value.tolist.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    collection.query.return_value = {
        "documents": [
            [
                "Mount the motors using four M3 screws.",
                "Use a 4S LiPo battery.",
            ]
        ],
        "metadatas": [
            [
                {
                    "source": "chassis.docx",
                    "heading": "Motor Mounting",
                },
                {
                    "source": "battery.docx",
                    "heading": "Battery Selection",
                },
            ]
        ],
    }

    retriever = Retriever(
        collection=collection,
        model=model,
        top_k=2,
    )

    result = retriever.retrieve("How do I mount the motors?")

    model.encode.assert_called_once_with(
        "How do I mount the motors?"
    )

    collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2, 0.3]],
        n_results=2,
    )

    assert result == [
        {
            "text": "Mount the motors using four M3 screws.",
            "metadata": {
                "source": "chassis.docx",
                "heading": "Motor Mounting",
            },
        },
        {
            "text": "Use a 4S LiPo battery.",
            "metadata": {
                "source": "battery.docx",
                "heading": "Battery Selection",
            },
        },
    ]


def test_retrieve_returns_empty_list_when_no_results(mocker):
    model = mocker.Mock()
    collection = mocker.Mock()

    model.encode.return_value.tolist.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    collection.query.return_value = {
        "documents": [[]],
        "metadatas": [[]],
    }

    retriever = Retriever(
        collection=collection,
        model=model,
        top_k=3,
    )

    result = retriever.retrieve("Unknown question")

    assert result == []


def test_retrieve_uses_configured_top_k(mocker):
    model = mocker.Mock()
    collection = mocker.Mock()

    model.encode.return_value.tolist.return_value = [0.1, 0.2]

    collection.query.return_value = {
        "documents": [["document"]],
        "metadatas": [
            [
                {
                    "source": "test.docx",
                    "heading": "Test",
                }
            ]
        ],
    }

    retriever = Retriever(
        collection=collection,
        model=model,
        top_k=5,
    )

    retriever.retrieve("question")

    collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2]],
        n_results=5,
    )