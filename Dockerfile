FROM ubuntu:latest
RUN rm /sys/class/hwmon/hwmon*/fan*_input
