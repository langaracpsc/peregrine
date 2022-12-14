Welcome to the discord repository of peregrine (version 2.0)!

<br/>

To use this bot:
- Download the bot files `git clone https://github.com/langaracpsc/peregrine.git`
- create a virtual environment: `python -m venv venv` (you may have to use python3 or py instead of python)
- enter the virtual environment: `venv/Scripts/activate` (`. venv/bin/activate` on linux)
- install py-cord and dot-env: `pip install py-cord` `pip install python-dotenv`
- place your token in a `.env` file: inside the file place `DISCORD_TOKEN="your_token_here"`
- run `python main.py`


(Almost all functionality in this bot is hardcoded to roles in the langara computer science club discord. Fork the bot if you want to use it in another server!)

<br/>
<br/>

Contact Highfire1#1942 if you have questions about the bot!

More functionality coming soon™️

<br/>
<br/>
<br/>
<br/>

If running on an oracle vm:
- update to python 3.9 because py-cord requires it `sudo yum install python39`
- install pip `python3.9 -m ensurepip`
- install libraries with `python3.9 -m pip install <library>`

also:
- use tmux `tmux` to create a session
- escape the session with `ctrl+b then d` 
- re-enter the session with `tmux attach -t 0 `
