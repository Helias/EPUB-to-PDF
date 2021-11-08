FROM linuxserver/calibre:latest

WORKDIR /epub_to_pdf

RUN apt-get -y update \
    && apt -y install python3-pip \
    && pip3 install python-telegram-bot
COPY . .

CMD ["python3", "main.py"]