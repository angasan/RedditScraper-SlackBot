##################################################################################
# CHOSE THE BASE IMAGE 
##################################################################################

# The first step is to choose a base image that your application will run on. 
# This base image should contain the operating system and any necessary 
# dependencies required to run your application. For example, if your application 
# is written in Python, you might choose the official Python base image.

FROM python:3.9

##################################################################################
# SPECIFY THE WORKING DIRECTORY
##################################################################################

# The next step is to specify the working directory where your application 
# files will be located.

WORKDIR /app

##################################################################################
# COPY APPLICATION FILES
##################################################################################

# You can copy your application files from your local machine to the Docker 
# image using the COPY directive.

COPY . /app
COPY requirements.txt /app

##################################################################################
# INSTALL DEPENDENCIES
##################################################################################

# If your application has dependencies, you can install them using the RUN 
# directive.
# - r is the recursive option

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

##################################################################################
# EXPOSE PORTS
##################################################################################

# If your application listens on a specific port, you can expose that port using 
# the EXPOSE directive

# We don't have any in this case

##################################################################################
# DEFINE THE STARTUP COMMAND
##################################################################################

# Finally, you need to define the startup command for your application using the 
# CMD or ENTRYPOINT directive.

CMD ["python", "get_reddits.py"]