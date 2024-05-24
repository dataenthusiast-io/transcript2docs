# Transcript2Docs

![Transcript2Docs Screenshot](assets/screenshot.png)

## Overview

Creating documentation is what everyone needs, but rarely anyone wants to take up. That's why continuously, knowledge is shared in endless handover meetings and similar sessions. At the same time, providers like Google or Microsoft offer the ability to get transcripts and summaries as part of their copilots. However, all of these general-purpose services and base models have one central problem: they lack context, which can lead to semantic errors, especially in domain-specific or technical contexts.

For example, in one of my first attempts, we handled a topic on IDs, and all of a sudden, "Microsoft Azure ID" became "Microsoft Your ID." The problem is, without context-based optimization, these semantic errors persist downstream, making it impossible to derive real benefit from the information.

That's why I came up with Transcript2Docs:

Take the transcript from any provider (e.g., Google Meet)
Simply provide semantic context by keywords
Provide the structure of the output document you want (e.g., introduction, key points, summary)
Select the type of meeting
-> Let the application correct the transcript and craft a compelling document out of it

-> Main use case for technical documentation (e.g., handover or trainings can be simply recorded and then converted into detailed documentation later)

While this is not a production-ready application, my main motivation is to showcase the integration between "human in the loop" and programmatic operations on LLMs.

## Features

- **Contextual Transcript Correction**: Automatically corrects the transcript based on the provided context.
- **Custom Document Structure**: Create documents with a user-defined structure.
- **Multiple Meeting Types**: Supports various types of meetings like Live Tutorial, Technical Walk-Through, Knowledge Sharing, and General Meeting.
- **Easy Integration**: Works with transcripts from any provider.
- **Modular Components**: Based on LangChain, Streamlit, and OpenAI (can be exchanged with local LLMs such as Ollama).
- **Configurable Chains**: Chains are configurable through the YAML files `transcript.yaml` and `docs.yaml`.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/Transcript2Docs.git
   cd Transcript2Docs
   ```

2. **Set up a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

Make sure to review the YAML files for chains and adjust models and prompts if required:

- `lib/chains/transcript.yaml`
- `lib/chains/docs.yaml`

## Usage

1. **Run the Streamlit application:**
   ```sh
   streamlit run app.py
   ```

2. **Upload your transcript file (.txt format).**
3. **Enter context keywords and document structure.**
4. **Select the type of meeting transcript.**
5. **Click on 'Generate Docs'.**

## Repository Structure

```
Transcript2Docs/
├── app.py
├── lib/
│   ├── engine.py
│   ├── chains/
│       ├── transcript.yaml
│       └── docs.yaml
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to reach out to [dataenthusiast.io].