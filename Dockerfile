FROM linuxserver/calibre:5.38.0

WORKDIR /epub_to_pdf

RUN apt-get -y update \
    && apt -y install python3-pip
RUN python3 -m pip install python-telegram-bot

COPY . .

CMD ["python3", "main.py"]
