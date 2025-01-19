
FROM python:3.14-rc-slim

RUN pip install uv

WORKDIR /app

# ...additional setup if needed...