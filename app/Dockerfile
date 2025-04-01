#Official python image as a parent image
FROM python:3.9-slim

# Working directory
WORKDIR /app

#Copying of current content into the container at /app
COPY . /app

#Install any needed packages specified in requirments.txt
RUN pip install --no-cache-dir -r requirements.txt

#Make port 5000 available
EXPOSE 5000

#Define environment variable
ENV FLASK_APP=app.py

#Run app.py when the container launches
CMD [ "flask", "run", "--host", "0.0.0.0" ]