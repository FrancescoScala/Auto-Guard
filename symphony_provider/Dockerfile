FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY symphony_provider.py ./

CMD [ "python", "-u", "./symphony_provider.py" ]
