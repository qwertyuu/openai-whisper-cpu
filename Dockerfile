FROM python:3.9-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Whisper
RUN git clone https://github.com/MiscellaneousStuff/openai-whisper-cpu.git \
 && cd openai-whisper-cpu \
 && git submodule init \
 && git submodule update \
 && USE_NNPACK=0 pip install -e ./whisper

# Install model files
RUN whisper --model base dummy.wav; exit 0

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-v", "api.py"]
