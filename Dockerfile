
FROM python:3-alpine

LABEL authors="Tomkat"

WORKDIR /app

COPY requirements.txt /app/
COPY *.py /app/
COPY *.json /app/

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]

#CMD ["sh"]