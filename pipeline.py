from speech_to_text import speech_to_text
from audio_video_utils import combine_audio_video, text_to_speech
from grammar_correction import correct_grammar_with_azure

async def main(audio_file_path):
    transcript = await speech_to_text(audio_file_path)
    
    if transcript:
        corrected_transcript = await correct_grammar_with_azure(transcript)
        text_to_speech(corrected_transcript)
        combine_audio_video("input_video.mp4", "output.mp3", "output_with_audio_async.mp4")

if __name__ == "__main__":
    audio_file_path = "extracted_audio.wav"
    asyncio.run(main(audio_file_path))
