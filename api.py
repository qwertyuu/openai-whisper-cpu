import base64
import uuid
from flask import Flask, request, jsonify
import subprocess
import whisper
import torch
import os
import time

print(subprocess.check_output(['ffmpeg', '-version']))
language = "French"

model_fp32 = whisper.load_model(
    name="base",
    device="cpu"
#   ,in_memory=True
)

quantized_model = torch.quantization.quantize_dynamic(
    model_fp32, {torch.nn.Linear}, dtype=torch.qint8
)


def time_model_evaluation(model, audio_file):
    eval_start_time = time.time()

    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    mel   = whisper.log_mel_spectrogram(audio).to(model_fp32.device)
    options = whisper.DecodingOptions(language=language,fp16=False,temperature=0,without_timestamps=True)
    result = whisper.decode(model, mel, options)
    print(result)
    eval_end_time = time.time()
    eval_duration_time = eval_end_time - eval_start_time

    print("Evaluate total time (seconds): {0:.1f}".format(eval_duration_time))
    return result.text


app = Flask(__name__)


@app.route('/api/stt', methods=['POST'])
def save_wav():
    # Receive the base64 encoded string from the request
    base64_string = request.json['audio_data']
    filetype = request.json.get('file', 'mp3')

    # Decode the base64 string to binary data
    binary_data = base64.b64decode(base64_string)

    # Generate a unique filename for the WAV file
    filename = str(uuid.uuid4()) + '.' + filetype
    filepath = os.path.join('audio_files', filename)

    # Write the binary data to disk as a WAV file
    with open(filepath, 'wb') as f:
        f.write(binary_data)

    trs = time_model_evaluation(quantized_model, filepath)

    # Return a JSON response indicating the filename and filepath of the saved WAV file
    response = {
        'trs': trs,
    }
    return jsonify(response)


if __name__ == '__main__':
    # Create the 'audio_files' directory if it doesn't exist
    if not os.path.exists('audio_files'):
        os.makedirs('audio_files')
    app.run(host="0.0.0.0")




def print_size_of_model(model):
    path = "temp.p"
    torch.save(model.state_dict(), path)
    size = os.path.getsize(path)/1e6
    print('Size (MB):', size)
    os.remove(path)
    return size


