# We are targeting arm
# TODO: figure out cross-platform compilation
# Feel free to build yourself
FROM arm64v8/python:3.10-slim
WORKDIR /app

# install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# get all files of the bot
COPY . .

# run code
# -u required for output see https://stackoverflow.com/a/24183941/15456176
CMD ["python3", "-u", "python/main.py"]

