from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import whisper
import wave

app = Flask(__name__)
CORS(app)

base_model = whisper.load_model("small.en")


def decode_and_save_audio(base64_data, output_audio_file_path):
    decode_string = base64.b64decode(base64_data)
    with open(output_audio_file_path, "wb") as audio_file:
        audio_file.write(decode_string)


@app.route("/convert_and_transcribe", methods=["POST"])
def convert_and_transcribe():
    try:
        json_data = request.get_json()

        # Ensure 'audio' key is present in the JSON input
        if "audio" not in json_data:
            return jsonify({"error": "Missing 'audio' key in JSON input"}), 400

        # Decode base64 string and save audio file
        decode_and_save_audio(json_data["audio"], "audioResponse.wav")
        result = base_model.transcribe("audioResponse.wav")
        text_input = result["text"]

        # Use CONVAI API
        # url = "https://api.convai.com/stt/"
        # payload = {"enableTimestamps": "False"}
        # files = [("file", ("audio.wav", open("audioResponse.wav", "rb"), "audio/wav"))]
        # headers = {"CONVAI-API-KEY": "c1e746cb3782b24cc075464e201ccd76"}
        # response = requests.post(url, headers=headers, data=payload, files=files)

        # return jsonify({"transcription": response.text})
        return jsonify({"transcription": text_input})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
