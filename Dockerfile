FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=1000:1000 . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

USER 1000

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]