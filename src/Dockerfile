FROM python:3.12-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir -p /usr/src/app/tmp
VOLUME [ "/usr/src/app/tmp" ]
ENV PYTHONPATH=/usr/src/app
EXPOSE 8000
CMD ["python", "app.py"]