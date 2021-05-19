FROM python:3.8

COPY ./video_converter /video_converter
COPY ./frontend /frontend/
COPY requirements.txt /requirements.txt

RUN apt update
RUN apt -y install ffmpeg
RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "video_converter.main:app", "--host", "0.0.0.0", "--port", "80"]
