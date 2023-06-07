FROM alpine:3.10

# Copy your script and any other necessary files
COPY test_fan_reaction.py /app/

# Set the entry point
ENTRYPOINT ["python", "/app/test_fan_reaction.py"]
