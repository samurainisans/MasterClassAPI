# # use the official python image as a base image
# FROM python:3.10
#
# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# # set the working directory in the container
# WORKDIR /app
#
# # copy the requirements file into the container
# COPY requirements.txt /app/
#
# # install the python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
#
# # copy the project files into the container
# COPY . /app/
#
# # run the django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# use a specific version of the official python image
FROM python:3.10

# set environment variables with comments
ENV PYTHONDONTWRITEBYTECODE 1
# prevents python from writing .pyc files

ENV PYTHONUNBUFFERED 1
# ensures output is sent straight to the terminal

# set the working directory in the container
WORKDIR /app

# copy the requirements file into the container
COPY requirements.txt /app/

# install the python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the project files into the container
COPY . /app/

# run gunicorn server for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MasterClassAPI.wsgi:application"]