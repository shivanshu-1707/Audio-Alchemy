import aiohttp
from config.py import ASSEMBLYAI_API_KEY 

async def upload_audio(session, audio_file, headers):
    with open(audio_file, 'rb') as f:
        upload_response = await session.post("ASSEMBLYAI_API_KEY", headers=headers, data=f)
        return await upload_response.json()

async def request_transcription(session, audio_url, headers):
    transcript_request = {"audio_url": audio_url}
    transcript_response = await session.post("ASSEMBLYAI_API_KEY ", headers=headers, json=transcript_request)
    return await transcript_response.json()

async def poll_transcription(session, transcript_id, headers):
    transcript_result_url = f"ASSEMBLYAI_API_KEY/{transcript_id}"
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
