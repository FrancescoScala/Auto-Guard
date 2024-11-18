FROM docker.io/ubuntu:24.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    software-properties-common \
    python3 \
    python3-pip \
    protobuf-compiler \
    net-tools \
    # install eCAL
    && add-apt-repository ppa:ecal/ecal-5.12 \
    && apt-get install -y python3-ecal5 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY main.py /web_ivi/main.py
COPY static /web_ivi/static

WORKDIR /web_ivi

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5500"]