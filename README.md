
# OratorAI


![image](https://github.com/user-attachments/assets/5a75b890-ae42-4379-ab56-19040ca2589e)

OratorAI is an advanced voice assistant application that integrates cutting-edge speech-to-text and text-to-speech technologies with a powerful conversational AI model. Utilizing Whisper for accurate speech recognition and Piper for natural text-to-speech synthesis, OratorAI offers dynamic voice options and seamless interaction. The application is ideal for real-time voice interaction scenarios, providing users with a customizable and intelligent conversational experience.

## Features

- **Real-time Speech-to-Text**: Leverages OpenAI's Whisper model to transcribe spoken words into text with high accuracy.
- **Text-to-Speech Synthesis**: Converts AI-generated text responses into natural-sounding speech using Piper, with customizable male and female voice options.
- **Conversational AI Integration**: Powered by Google’s Gemini-1.5-Pro model, providing intelligent and context-aware responses.
- **Dynamic Voice Switching**: Users can switch between male and female voices during a conversation.
- **Robust Logging**: All interactions are logged in `voice_assistant.log` for review and debugging.

## Installation

Follow these steps to set up and run OratorAI on your local machine.

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Virtual environment tools (e.g., `venv` or `virtualenv`)

### Clone the Repository

```bash
git clone https://github.com/debjit-mandal/OratorAI.git
cd OratorAI
```

### Set Up the Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configuration

1. **API Key**: Create a `.env` file in the root directory and add your Google API key for the Gemini model:

   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

2. **Model Paths**: Ensure that the paths in `config.json` point to the correct locations of your Piper models. The `config.json` file should look like this:

   ```json
   {
       "male_model_path": "piper_models/male/en_US-hfc_male-medium.onnx",
       "female_model_path": "piper_models/female/en_US-hfc_female-medium.onnx",
       "sample_rate": 22050,
       "channels": 1,
       "sample_width": 2
   }
   ```

## Usage

To start the OratorAI voice assistant, run the following command:

```bash
python live_transcribe.py
```

### Interaction

- **Voice Selection**: At the start, you will be prompted to choose between a male or female voice.
- **Dynamic Voice Switching**: During the conversation, you can switch voices by saying "switch to male voice" or "switch to female voice."
- **Exit**: Say "exit" to terminate the session.

### Logging

All interactions and events are logged to `voice_assistant.log`. This includes:

- Transcribed text (with symbols filtered out)
- AI-generated responses
- Errors and warnings

### Example Commands

- "What’s the weather like today?"
- "Play some rock music and set the temperature to cool."
- "Switch to female voice."
- "Exit."

## Contributing

Contributions to OratorAI are welcome! Feel free to submit issues and pull requests on the [GitHub repository](https://github.com/debjit-mandal/OratorAI).

### To Contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **OpenAI Whisper**: For speech-to-text transcription.
- **Piper**: For text-to-speech synthesis.
- **Google Gemini-1.5-Pro**: For powering the conversational AI.
- **LangChain**: For chaining together prompts and AI responses.
