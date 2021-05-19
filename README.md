# web-video-converter
The online video bit-rate converter. Written in Python 3.8 with FastAPI and utilizing ffmpeg (https://www.ffmpeg.org/).

Run locally (in Linux) from project root:
> uvicorn video_converter.main:app

Or, using Docker (from project root):
> docker build -t web-video-converter .

> docker run -e AWS_DEFAULT_REGION="eu-north-1" -e AWS_ACCESS_KEY_ID="xxx" -e AWS_SECRET_ACCESS_KEY="xxx" -e MAX_WORKERS="1" -p 80:80 --name web-video-converter web-video-converter
