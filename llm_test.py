from src.llm.openai_client import generate_answer


def test_generate_answer():
    chunks = [
        {
            "text": "Mount the motors using four M3 screws.",
            "metadata": {
                "source": "chassis.docx",
                "heading": "How/where do I mount motors?",
            },
        }
    ]

    answer = generate_answer(
        "How do I mount the motors?",
        chunks,
    )

    print("\nChatGPT response:")
    print(answer)

    assert answer

    answer = generate_answer(
        "How do I train a dragon?",
        chunks,
    )

    print("\nChatGPT response:")
    print(answer)

    assert answer

if __name__ == "__main__":
    test_generate_answer()