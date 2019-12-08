FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=0
RUN apt-get update && apt-get install -y git
RUN python -m pip install --upgrade pip
RUN pip install pytest
WORKDIR /app
COPY . /app
RUN pip install -e .
