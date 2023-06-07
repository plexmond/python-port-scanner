# base image
FROM python:3.11

# azure cli voor az credentials
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Set a working directory inside the container. (app directory)
WORKDIR /app

# copy requirements.txt file into the container 
COPY requirements.txt requirements.txt

# install python depends. > do before copying code for docker layer caching.
RUN pip install --no-cache-dir -r requirements.txt

# copy all code into container.
COPY . .

# expose port 5000 for the flask app
EXPOSE 5000

# flask production mode, listen on all interfaces
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0


# cmd's executed when running container from image 
CMD ["flask", "run"]
