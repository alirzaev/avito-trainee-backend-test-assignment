FROM python:3.9
EXPOSE 80

WORKDIR /usr/src/project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./docker/runserver.sh"]
