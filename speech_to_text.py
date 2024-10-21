from api_utils import upload_audio, request_transcription, poll_transcription
import aiohttp
from config import ASSEMBLYAI_API_KEY

async def speech_to_text(audio_file):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    
    async with aiohttp.ClientSession() as session:
        upload_response = await upload_audio(session, audio_file, headers)
        audio_url = upload_response.get('upload_url')

        if audio_url:
            transcript_response = await request_transcription(session, audio_url, headers)
            transcript_id = transcript_response.get("id")
            transcription_text = await poll_transcription(session, transcript_id, headers)
            return transcription_text
        return None
