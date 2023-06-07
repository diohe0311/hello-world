FROM ubuntu:latest
RUN rm /sys/class/hwmon/hwmon*/fan*_input

FROM python:3.9-alpine

# Copy your script and any other necessary files
COPY test_fan_reaction.py /app/

# Set the entry point
ENTRYPOINT ["python", "/app/test_fan_reaction.py"]
