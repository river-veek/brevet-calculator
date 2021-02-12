FROM python:3
MAINTAINER River Veek "riverv@uoregon.edu"
# ADD . /todo
# WORKDIR /todo
# RUN pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]
