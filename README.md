# Combat Robotics RAG Assistant

A retrieval-augmented generation (RAG) chatbot that lets Cornell combat robotics members ask questions about team documentation directly through Slack.

The system retrieves relevant sections from the team's technical documentation, provides them as context to an OpenAI model, and returns an answer with source citations. It is designed to answer questions from the team's documentation without relying on unsupported information.

## Features

* **Semantic document search** using Sentence Transformers embeddings
* **Vector storage and retrieval** with ChromaDB
* **RAG-based question answering** using the OpenAI Responses API
* **Slack integration** using Slack Bolt
* **Source citations** linking generated answers back to retrieved documentation
* **Conversation context** from Slack threads
* **Automated tests** with pytest and mocked external services
* **Modular architecture** separating ingestion, retrieval, generation, and Slack functionality

## Architecture

The application follows a standard RAG pipeline:

```text
                         ┌────────────────────┐
                         │  Robotics Docs      │
                         │      (.docx)        │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Document Parser    │
                         │ & Chunker          │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Sentence           │
                         │ Transformer        │
                         │ Embeddings         │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │     ChromaDB       │
                         │   Vector Store     │
                         └─────────┬──────────┘
                                   │
                              Top-k chunks
                                   │
                                   ▼
┌───────────────┐       ┌────────────────────┐
│     Slack     │──────▶│     Retriever      │
│    Question   │       └─────────┬──────────┘
└───────────────┘                 │
                                  ▼
                         ┌────────────────────┐
                         │ OpenAI Responses   │
                         │       API          │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Answer + Citations │
                         └────────────────────┘
```

### Pipeline

1. `.docx` documentation is parsed into sections.
2. Sections are split into retrieval-friendly chunks while preserving their source and heading metadata.
3. Each chunk is embedded using a Sentence Transformer model.
4. Embeddings and metadata are stored in a persistent ChromaDB collection.
5. A user asks a question through Slack.
6. The question is embedded and compared against the document embeddings.
7. The most relevant chunks are retrieved.
8. Retrieved documentation and relevant Slack conversation context are passed to the OpenAI model.
9. The model generates an answer grounded in the retrieved documentation.
10. Sources referenced by the answer are included as citations.

## Project Structure

```text
combat_rag_remaster/
├── documents/                 # Source robotics documentation
├── scripts/                   # Utility scripts for project setup/maintenance
├── src/
│   ├── ingestion/
│   │   ├── parser.py          # Parses .docx files into sections
│   │   ├── chunker.py         # Splits sections into retrieval chunks
│   │   ├── embedder.py        # Generates document embeddings
│   │   └── ingest.py          # Runs the ingestion pipeline
│   │
│   ├── retrieval/
│   │   ├── vector_store.py    # ChromaDB storage and collection management
│   │   └── retriever.py       # Semantic document retrieval
│   │
│   ├── generation/
│   │   ├── prompt.py          # Builds prompts and document context
│   │   └── generator.py       # Generates answers using OpenAI
│   │
│   ├── slack/
│   │   └── bot.py             # Slack event handling
│   │
│   └── rag.py                 # High-level RAG orchestration
│
├── tests/                     # Unit and integration tests
├── pytest.ini                 # Pytest configuration
├── .gitignore
└── README.md
```

## Tech Stack

| Component       | Technology               |
| --------------- | ------------------------ |
| Language        | Python                   |
| LLM             | OpenAI Responses API     |
| Embeddings      | Sentence Transformers    |
| Vector Database | ChromaDB                 |
| Chat Platform   | Slack                    |
| Slack Framework | Slack Bolt               |
| Testing         | pytest                   |
| Mocking         | pytest-mock              |
| Version Control | Git / GitHub             |
| CI              | GitHub Actions           |

## Getting Started

### Prerequisites

* Python 3.10+
* A Slack app with the required permissions
* An OpenAI API key
* Slack bot credentials

### Clone the repository

```bash
git clone https://github.com/vinsonchen3/combat_rag_remaster.git
cd combat_rag_remaster
```

### Create a virtual environment

Using `venv`:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

Do not commit `.env` or API credentials to the repository.

## Ingesting Documents

The RAG system uses local `.docx` files stored in `documents/`.

Run the ingestion pipeline to parse, chunk, embed, and store the documentation:

```bash
python -m src.scripts.ingest
```

The resulting embeddings are persisted locally in ChromaDB.

### Document Format

The parser uses Word document headings to preserve document structure.

For example:

```text
Heading 1: Weapon Design

    Technical information about weapon design...

Heading 2: Motor Selection

    Information about selecting motors...

Heading 2: Gear Ratios

    Information about gear ratios...
```

Chunks retain metadata such as:

```text
source
heading
```

This metadata allows retrieved information to be traced back to its original documentation.

## Running the Slack Bot

After configuring the Slack credentials and ingesting the documentation:

```bash
python -m src.slack.main
```

The bot listens for Slack mentions and responds in the relevant thread.

A typical interaction looks like:

```text
User:
@Combat Robotics RAG What motor should I use for a 3 lb spinning weapon?

Bot:
According to the team's documentation, ...

Sources:
- How-To_ Design an Asymmetric Spinning Weapon.docx
  - Motor Selection
```

The bot uses retrieved documentation as the primary source of information rather than relying on the model's general knowledge.

## Retrieval

The retrieval system uses Sentence Transformers to convert both documentation and queries into dense vector representations.

The project uses:

```text
all-MiniLM-L6-v2
```

with cosine similarity in ChromaDB.

At query time:

```text
Question
   │
   ▼
Query embedding
   │
   ▼
ChromaDB similarity search
   │
   ▼
Top-k document chunks
   │
   ▼
LLM context
```

Each retrieved chunk contains both its text and metadata, allowing the generation layer to identify the original document and section.

## Answer Generation

The generation layer receives:

* The user's question
* Retrieved documentation
* Relevant Slack conversation context
* Source metadata

The model is instructed to answer using the supplied documentation and conversation context.

When the retrieved documentation does not contain enough information to answer a question, the system is designed to avoid inventing an answer and instead indicate that the available documentation does not provide enough information.

### Citations

Retrieved chunks are tracked through the generation process so that sources referenced by the final answer can be displayed to the user.

This makes answers easier to verify and helps users locate the original robotics documentation.

## Testing

The project uses pytest for automated testing.

Run the complete test suite with:

```bash
pytest
```

Tests cover individual components as well as interactions between components.

Examples include:

* Document parsing
* Document chunking
* Embedding behavior
* Vector-store interactions
* Retrieval behavior
* Prompt/context construction
* OpenAI response handling
* Citation generation
* Slack event handling
* End-to-end RAG behavior

External services such as OpenAI and Slack are mocked during tests so that the test suite does not require live API requests.

This keeps tests:

* Fast
* Deterministic
* Reproducible
* Independent of external API availability

## Development

A typical development workflow is:

```text
Add/update documentation
        │
        ▼
Run ingestion pipeline
        │
        ▼
Test retrieval
        │
        ▼
Test generation
        │
        ▼
Test Slack integration
        │
        ▼
Run pytest
        │
        ▼
Push changes
```

Before submitting changes, run:

```bash
pytest
```

## Design Decisions

### Why RAG?

The robotics team maintains specialized technical documentation that is not part of a general-purpose LLM's knowledge.

RAG allows the assistant to retrieve the team's own documentation at query time instead of attempting to encode that information into the model itself.

### Why ChromaDB?

ChromaDB provides a lightweight local vector database suitable for storing document embeddings and performing similarity search without requiring a separate database service.

### Why Sentence Transformers?

Sentence Transformers provides a local embedding model, allowing document ingestion and retrieval to run without making an embedding API request for every document or query.

### Why Slack?

Slack is already where the robotics team communicates and shares technical knowledge. Integrating the assistant directly into Slack makes the documentation searchable without requiring users to leave their existing workflow.