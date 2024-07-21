FROM python:3

COPY . /EncurtaPy
WORKDIR /EncurtaPy

RUN pip install -r requirements.txt

CMD python main.py
