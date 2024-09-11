FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY ./requirements.txt /app/requirements.txt

COPY ./flag.txt /root/flag.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 80

COPY ./app /app