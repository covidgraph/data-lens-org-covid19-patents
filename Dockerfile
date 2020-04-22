
FROM python:3.6

RUN mkdir -p /app/dataset
RUN mkdir -p /app/dataloader
WORKDIR /app/dataloader

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY dataloader .

CMD [ "python3", "./main.py" ]