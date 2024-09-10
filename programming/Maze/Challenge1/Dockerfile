FROM python:3.10-alpine

WORKDIR /code

COPY . .
RUN pip install -r requirements.txt
EXPOSE 9997

CMD ["python3", "maze_challenge1.py"]