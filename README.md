# OmniAI - Modular Personal Assistant

OmniAI is a modular, personal AI assistant and life automation system built with Python.

## Features
- **Natural Language Workflows**: Define your routines in YAML and trigger them with plain English.
- **LLM Powered**: Uses Google Gemini to understand complex intents.
- **Modern GUI**: Built with PyQt6 for a premium desktop experience.
- **Voice Interaction**: Integrated Speech-to-Text and Text-to-Speech.
- **Secure & Persistent**: SQLite database for history/metrics and basic security command filtering.

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup environment:
   - Copy `.env.example` to `.env`
   - Fill in your `GEMINI_API_KEY`

## Configuration
Add your own workflows to `config.yaml`:
```yaml
custom_routine:
  trigger: "I want to code"
  actions:
    - open_app: "code.exe"
    - speak: "Coding mode activated."
```

## Running
- **Dashboard (GUI)**: `python gui.py`
- **Console (CLI)**: `python main.py`

