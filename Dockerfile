FROM python:3.11-slim
WORKDIR /app
COPY app/ /app/
RUN pip install --no-cache-dir flask==3.0.0
EXPOSE 8080
CMD ["python", "server.py"]
