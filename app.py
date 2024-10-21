import asyncio
import aiohttp
from gtts import gTTS
import os
from playsound import playsound  # For playing the generated audio
import subprocess  # For calling FFmpeg

def combine_audio_video(video_path, audio_path, output_path):
    """
    Combines an audio file and a video file into one video with synchronized audio.
    
    Parameters:
        video_path (str): Path to the video file.
        audio_path (str): Path to the audio file.
        output_path (str): Path where the output video file will be saved.
    """
    # Call FFmpeg to combine audio and video
    command = [
        "ffmpeg",
        "-i", video_path,  # Input video file
        "-i", audio_path,  # Input audio file
        "-c:v", "copy",    # Copy the video codec
        "-c:a", "aac",     # Set the audio codec to AAC
        "-strict", "experimental",  # Allow experimental codecs
        output_path        # Output file
    ]
    
    # Execute the command
    subprocess.run(command, check=True)
    print(f"Combined video and audio saved to {output_path}")

async def upload_audio(session, audio_file, headers):
    print("Step 1: Uploading audio...")
    with open(audio_file, 'rb') as f:
        upload_response = await session.post("https://api.assemblyai.com/v2/upload", headers=headers, data=f)
        print("Step 1 Completed: Audio uploaded.")
        return await upload_response.json()

async def request_transcription(session, audio_url, headers):
    print("Step 2: Requesting transcription...")
    transcript_request = {"audio_url": audio_url}
    transcript_response = await session.post("https://api.assemblyai.com/v2/transcript", headers=headers, json=transcript_request)
    print("Step 2 Completed: Transcription requested.")
    return await transcript_response.json()

async def poll_transcription(session, transcript_id, headers):
    print("Step 3: Polling for transcription result...")
    transcript_result_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    max_attempts = 20  # Maximum number of polling attempts
    attempts = 0

    while attempts < max_attempts:
        result_response = await session.get(transcript_result_url, headers=headers)
        result_json = await result_response.json()
        
        if result_json["status"] == "completed":
            print("Step 3 Completed: Transcription completed successfully.")
            return result_json["text"]
        elif result_json["status"] == "failed":
            raise Exception("Transcription failed.")
        
        print("Step 3: Still polling for result...")
        attempts += 1
        await asyncio.sleep(15)  # Wait for 15 seconds before polling again

    raise Exception("Transcription polling timed out after maximum attempts.")

async def correct_grammar_with_azure(text):
    print("Step 4: Correcting grammar using Azure GPT...")
    azure_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    azure_api_key = "22ec84421ec24230a3638d1b51e3a7dc"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_api_key
    }

    data = {
        "messages": [{"role": "user", "content": f"Please correct the grammatical structure such that it makes meaningful sense and don't add additional content, just send the output: {text}"}],
        "model": "gpt-o1"
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(azure_endpoint, headers=headers, json=data)
        if response.status == 200:
            response_json = await response.json()
            corrected_text = response_json['choices'][0]['message']['content']
            print("Step 4 Completed: Grammar correction done.")
            return corrected_text
        else:
            print("Error in grammar correction:", response.status, await response.text())
            return text  # Return the original text in case of error

def text_to_speech(text):
    print("Step 5: Converting text to speech...")
    tts = gTTS(text=text, lang='en')  # Change 'en' to your preferred language code
    audio_file = "output.mp3"
    tts.save(audio_file)
    
    # Check if the file was created
    if os.path.exists(audio_file):
        playsound(audio_file)  # Play the generated audio
        print("Step 5 Completed: Text converted to speech.")
    else:
        print("Error: Audio file was not created.")

async def speech_to_text(audio_file):
    api_key = "b109e0a4c00f463384681a37c6236adc"  # AssemblyAI API key
    headers = {'authorization': api_key}
    
    async with aiohttp.ClientSession() as session:
        # Upload audio file
        upload_response = await upload_audio(session, audio_file, headers)
        audio_url = upload_response.get('upload_url')

        if audio_url:
            # Request transcription
            transcript_response = await request_transcription(session, audio_url, headers)
            transcript_id = transcript_response.get("id")
            
            # Poll for transcription result
            transcription_text = await poll_transcription(session, transcript_id, headers)
            return transcription_text
        else:
            print("Step 1 Failed: Failed to upload audio.")
            return None

async def main(audio_file_path):
    transcript = await speech_to_text(audio_file_path)
    
    if transcript:
        print("Final Transcription:", transcript)
        corrected_transcript = await correct_grammar_with_azure(transcript)
        print("Corrected Transcription:", corrected_transcript)
        text_to_speech(corrected_transcript)
        combine_audio_video("input_video.mp4", "output.mp3", "output_with_audio_async.mp4")

# To run the asynchronous function
if __name__ == "__main__":
    audio_file_path = "extracted_audio.wav"  # Path to your audio file
    asyncio.run(main(audio_file_path))
