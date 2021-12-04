FROM python:3.7-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x radiobot.py
CMD [ "python", "radiobot.py" ]
