FROM ubuntu:20.04

COPY test_fan_reaction.py /app/

ENTRYPOINT ["python", "/app/test_fan_reaction.py"]
