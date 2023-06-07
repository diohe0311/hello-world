FROM alpine

RUN apk update && apk add --no-cache python3
RUN apk update && apk add --no-cache py3-pip

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "test_fan_reaction.py"]
