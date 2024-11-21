import requests

url = 'https://0e2c-217-92-84-125.ngrok-free.app/api/upload_video'
file_path = '/Users/mac/zzzzz/hackathon/sdv_hackathon_chapter2/final/CaliperKings/backend/reports-backend/my_file.mp4'

with open(file_path, 'rb') as video_file:
    files = {'video': video_file}
    response = requests.post(url, files=files)

print(response.text)
