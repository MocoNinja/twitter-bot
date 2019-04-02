FROM ubuntu:bionic

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./bot.py /app/app.py

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

