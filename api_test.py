import subprocess

import requests
import base64
import time

API_ENDPOINT = 'http://localhost:5000/api/stt'

before = time.time()
compressed = "/mnt/c/Users/USER/Documents/iluanncath_c.wav"
subprocess.call(['ffmpeg', "-y", '-i', "/mnt/c/Users/USER/Documents/iluanncath_c.wav", "-codec:a", "pcm_s16le", "-ac", "1", "-ar", "15000", compressed])

# Read the WAV file as binary data
with open(compressed, 'rb') as f:
    binary_data = f.read()

# Encode the binary data to base64
base64_string = base64.b64encode(binary_data).decode('utf-8')

# Send a POST request to the API endpoint with the base64 encoded string in the payload
response = requests.post(API_ENDPOINT, json={'audio_data': base64_string})

# Print the response
print(response.json())
print(time.time() - before)