# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /app/

# # copy the dependencies file to the working directory
COPY requirements.txt .
COPY prestart.sh .
#
# # install dependencies
RUN pip install -r requirements.txt


# copy the content of the local src directory to the working directory
COPY app/ /app/
COPY jajca.zip ./jajca.zip



# command to run on container start
