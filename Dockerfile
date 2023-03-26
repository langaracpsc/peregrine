FROM python:3
WORKDIR /app

# install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# get all files of the bot
COPY . .

# run code
CMD ["python3", "main.py"]

