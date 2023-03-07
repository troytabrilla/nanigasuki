FROM python:3.11.2-slim-bullseye AS base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

FROM base AS test
CMD ["python3", "-m", "pytest", "tests"]

FROM base AS build
RUN rm -rf tests
