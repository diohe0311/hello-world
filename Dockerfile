FROM ubuntu:18.04

RUN apt update && apt install nginx -y

CMD service nginx start && /bin/bash

COPY test_fan_reaction.py /app/

ENTRYPOINT ["python", "/app/test_fan_reaction.py"]
