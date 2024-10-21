# Audio-Alchemy

# Speech-to-Text and Grammar Correction with Azure GPT

This project is a Python application that performs speech-to-text conversion using AssemblyAI, corrects the grammar of the transcribed text using Azure's GPT model, and converts the corrected text to speech. It also combines the generated audio with a video file.

## Features

- Speech-to-text conversion using AssemblyAI
- Grammar correction using Azure GPT
- Text-to-speech conversion using Google Text-to-Speech (gTTS)
- Combining audio and video using FFmpeg

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- FFmpeg (for combining audio and video)

## 📥 Installation

### Install Required Python Packages

Run the following command to install the necessary Python packages:

```bash
pip install aiohttp gtts playsound
```

### Install FFmpeg

Follow the installation instructions for your operating system:

- **Windows:** Download from the [FFmpeg official website](https://ffmpeg.org/download.html).
- **macOS:** Use Homebrew:
  ```bash
  brew install ffmpeg
  ```
- **Linux:** Use your package manager (e.g., for Debian-based systems, you can use):
  ```bash
  sudo apt install ffmpeg
  ```

## ⚙️ Configuration

### API Keys

1. Replace `your_azure_api_key_here` with your Azure API key in the `correct_grammar_with_azure` function.
2. Replace `your_assemblyai_api_key_here` with your AssemblyAI API key in the `speech_to_text` function.

### Azure Endpoint

You will be prompted to enter your Azure endpoint when you run the application.

## 📝 Usage

1. Prepare an audio file (e.g., `extracted_audio.wav`) that you want to transcribe and correct.
2. Ensure you have a video file (e.g., `input_video.mp4`) that you want to combine with the generated audio.
3. Run the application:
   ```bash
   python your_script_name.py
   ```
4. Follow the prompts to enter the Azure endpoint.

## 🌟 Example Workflow

1. **Upload** an audio file to be transcribed.
2. The application will:
   - **Transcribe** the audio
   - **Correct** the grammar
   - **Convert** the corrected text to speech
3. The generated audio will be **combined** with the specified video file.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the repository.**
2. **Create a new branch**: 
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Make your changes** and commit them: 
   ```bash
   git commit -m 'Add some feature'
   ```
4. **Push to the branch**: 
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request.**

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- **AssemblyAI** for the speech-to-text API.
- **Azure OpenAI Service** for providing GPT capabilities.
- **gTTS** for text-to-speech conversion.
- **FFmpeg** for multimedia processing.
