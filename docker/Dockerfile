FROM nvidia/cuda:12.6.1-runtime-ubuntu22.04

WORKDIR /app
COPY requirements.txt requirements.txt
COPY sttt sttt

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libcudnn8

RUN pip install torch==2.7.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cu126
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "-m", "sttt"]
