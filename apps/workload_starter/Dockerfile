FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY app.py ./

CMD [ "python3", "-u", "./app.py" ]
