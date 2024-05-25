# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-05-25

### Added
- **Support for Multiple LLM Providers**: 
  - Introduced a factory pattern to dynamically create LLM instances based on the provider specified in the YAML configuration.
  - Supported providers include OpenAI, Anthropic, and Ollama.
  - Updated YAML configuration to include the `provider` field.
- **Session State Management**:
  - Utilized Streamlit's session state to persist the generated document on the frontend even after downloading.
- **Download Button**:
  - Added a download button to allow users to download the generated documentation as a Markdown file.
- **Error Handling and Logging**:
  - Enhanced error handling with try-except blocks and logging for better debugging.
- **Caching**:
  - Implemented caching to avoid reprocessing the same transcript, improving efficiency.

### Changed
- **User Interface**:
  - Moved input fields to the sidebar for a cleaner main interface.
  - Added a progress spinner to indicate processing status.
- **Backend Code**:
  - Refactored backend code to support dynamic importing of required libraries based on the LLM provider.
  - Improved chunking logic to handle edge cases better.

### Fixed
- **State Persistence**:
  - Fixed an issue where the generated document would disappear from the frontend after clicking the download button.

## [0.1.0] - 2024-05-24

### Added
- Initial release of Transcript2Docs with basic functionality:
  - Upload transcript file.
  - Enter context keywords and document structure.
  - Generate optimized transcript and documentation.
  - Display generated documentation on the frontend.
