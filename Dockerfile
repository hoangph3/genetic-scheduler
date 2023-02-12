
FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN apt-get update -y
RUN apt-get install nano telnet curl -y
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]
