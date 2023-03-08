FROM python:3.9.14-bullseye

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
 && pip install -e ./whisper

# Install model files
RUN whisper --model base dummy.wav; exit 0

WORKDIR /usr/src/app

CMD ["whisper","python3"]
