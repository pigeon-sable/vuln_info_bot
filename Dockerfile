# syntax=docker/dockerfile:1

FROM python:3.11.4
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get install -y vim && apt-get autoremove -y
RUN pip install --no-cache-dir --upgrade pip
ADD ./requirements.txt /app
RUN pip install -r requirements.txt
ADD ./vuln_info_bot /app/vuln_info_bot
CMD [ "python", "vuln_info_bot/main.py" ]
