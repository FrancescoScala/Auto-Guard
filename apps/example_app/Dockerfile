FROM ubuntu:24.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    software-properties-common \
    git \
    jq \
    python3 \
    python3-pip \
    # install eCAL
    && add-apt-repository ppa:ecal/ecal-5.12 \
    && apt-get install -y python3-ecal5 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY example_app.py ./

CMD [ "python3", "-u", "./example_app.py" ]
