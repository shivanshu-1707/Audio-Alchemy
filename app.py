import asyncio
import aiohttp
from gtts import gTTS
import os
from playsound import playsound
import subprocess
from config import ASSEMBLYAI_API_KEY, AZURE_API_KEY

def combine_audio_video(video_path, audio_path, output_path):
    command = ["ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_path]
    subprocess.run(command, check=True)

async def upload_audio(session, audio_file, headers):
    with open(audio_file, 'rb') as f:
        upload_response = await session.post("https://api.assemblyai.com/v2/upload", headers=headers, data=f)
        return await upload_response.json()

async def request_transcription(session, audio_url, headers):
    transcript_request = {"audio_url": audio_url}
    transcript_response = await session.post("https://api.assemblyai.com/v2/transcript", headers=headers, json=transcript_request)
    return await transcript_response.json()

async def poll_transcription(session, transcript_id, headers):
    transcript_result_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    max_attempts = 20
    attempts = 0

    while attempts < max_attempts:
        result_response = await session.get(transcript_result_url, headers=headers)
        result_json = await result_response.json()
        
        if result_json["status"] == "completed":
            return result_json["text"]
        elif result_json["status"] == "failed":
            raise Exception("Transcription failed.")
        
        attempts += 1
        await asyncio.sleep(15)

    raise Exception("Transcription polling timed out.")

async def correct_grammar_with_azure(text):
    azure_endpoint = "https://your-azure-endpoint"
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    data = {
        "messages": [{"role": "user", "content": f"Correct the grammatical structure: {text}"}],
        "model": "gpt-o1"
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(azure_endpoint, headers=headers, json=data)
        if response.status == 200:
            response_json = await response.json()
            return response_json['choices'][0]['message']['content']
        else:
            return text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_file = "output.mp3"
    tts.save(audio_file)
    
    if os.path.exists(audio_file):
        playsound(audio_file)

async def speech_to_text(audio_file):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    
    async with aiohttp.ClientSession() as session:
        upload_response = await upload_audio(session, audio_file, headers)
        audio_url = upload_response.get('upload_url')

        if audio_url:
            transcript_response = await request_transcription(session, audio_url, headers)
            transcript_id = transcript_response.get("id")
            return await poll_transcription(session, transcript_id, headers)
        return None

async def main(audio_file_path):
    transcript = await speech_to_text(audio_file_path)
    
    if transcript:
        corrected_transcript = await correct_grammar_with_azure(transcript)
        text_to_speech(corrected_transcript)
        combine_audio_video("input_video.mp4", "output.mp3", "output_with_audio_async.mp4")

if __name__ == "__main__":
    audio_file_path = "extracted_audio.wav"
    asyncio.run(main(audio_file_path))
