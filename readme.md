# Peregrine 2.0
Welcome to the repository of Langara Computer Science Club's discord bot, peregrine! 

Come chat in #club-projects on our discord server if you have any questions or comments :)


## Features:
 - information on langara courses
 - ephemeral channel
 - basic automoderation
 - More functionality coming soon™️


## Instructions

This project is setup to be run with Docker on our cloud [server](https://github.com/langaracpsc/server/tree/main), but you can also run it by itself for testing/development.


Note that pushing to main will automatically update the live discord bot. (If anyone knows how to do this properly with cogs instead of the current messy system PLEASE LMK)

- `git pull` to clone this project
- `cd peregrine2` to enter the directory
- `python -m venv venv` to create a virtual environment
- download the required libraries `python -m pip install -r requirements.txt`
- download `python -m spacy download en` for filtering #anonymous
- populate `.env`
- run with `python python/main.py`


## Populating .env
- `DISCORD_BOT_TOKEN`: Your bot token from discord