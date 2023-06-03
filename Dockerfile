FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN rasa train
EXPOSE 5005
CMD ["sh", "start.sh"]