FROM python:3.9

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

# Exponer los tres puertos
EXPOSE 9997
EXPOSE 9998
EXPOSE 9999

# Ejecutar los tres scripts en puertos diferentes
CMD ["sh", "-c", "python3 maze_challenge1.py & python3 maze_challenge2.py & python3 maze_challenge3.py"]