#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

#COPY ./video_converter /app
#COPY ./frontend /frontend/
#COPY requirements.txt /app/requirements.txt

#RUN pip3 install -r requirements.txt


FROM python:3.8

RUN pip install fastapi uvicorn

COPY ./video_converter /video_converter
COPY ./frontend /frontend/
COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "video_converter.main:app", "--host", "0.0.0.0", "--port", "80"]
