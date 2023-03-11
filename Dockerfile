FROM pytorch/pytorch:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Whisper
RUN git clone https://github.com/MiscellaneousStuff/openai-whisper-cpu.git \
 && cd openai-whisper-cpu \
 && git submodule init \
 && git submodule update \
 && pip install -e ./whisper

# Install model files
RUN whisper --model small dummy.wav; exit 0

COPY . .
RUN pip install -r requirements.txt

CMD ["python","api.py"]
