FROM python:3
WORKDIR /app

# install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# get all files of the bot
COPY . .

# run code
# -u required for output see https://stackoverflow.com/a/24183941/15456176
CMD ["python3", "-u", "python/main.py"]

