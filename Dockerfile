# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /app/

# # copy the dependencies file to the working directory
COPY requirements.txt .
#
# # install dependencies

RUN pip install -r requirements.txt

COPY prestart.sh .
# copy the content of the local src directory to the working directory
COPY app/ /app/
COPY src ./src
COPY test ./test

COPY example.zip ./example.zip

RUN echo $(./prestart.sh)

EXPOSE 80
# command to run on container start
