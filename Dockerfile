FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./video_converter /app
COPY ./frontend /app