from fastapi import FastAPI, HTTPException
import json
import base64
import requests

app = FastAPI()


def decode_and_save_audio(base64_data, output_audio_file_path):
    decode_string = base64.b64decode(base64_data)
    with open(output_audio_file_path, "wb") as audio_file:
        audio_file.write(decode_string)


@app.post("/convert_and_transcribe")
async def convert_and_transcribe(json_data: dict):
    try:
        # Ensure 'audio' key is present in the JSON input
        if "audio" not in json_data:
            raise HTTPException(
                status_code=400, detail="Missing 'audio' key in JSON input"
            )

        # Decode base64 string and save audio file
        decode_and_save_audio(json_data["audio"], "audioResponse.wav")

        # Use CONVAI API
        url = "https://api.convai.com/stt/"
        payload = {"enableTimestamps": "False"}
        files = [("file", ("audio.wav", open("audioResponse.wav", "rb"), "audio/wav"))]
        headers = {"CONVAI-API-KEY": "c1e746cb3782b24cc075464e201ccd76"}

        response = requests.post(url, headers=headers, data=payload, files=files)

        return {"transcription": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
