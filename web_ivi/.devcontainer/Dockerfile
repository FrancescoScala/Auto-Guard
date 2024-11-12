FROM docker.io/ubuntu:24.04 as dev

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    software-properties-common \
    python3 \
    python3-pip \
    protobuf-compiler \
    net-tools \
    && \
    rm -rf /var/lib/apt/lists/* \
    && add-apt-repository ppa:ecal/ecal-5.12 \
    && apt-get install -y python3-ecal5

RUN PIP_BREAK_SYSTEM_PACKAGES=1 pip install \
    fastapi \
    uvicorn

FROM dev as prod

COPY main.py /web_ivi/main.py
COPY static /web_ivi/static

WORKDIR /web_ivi

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5500"]