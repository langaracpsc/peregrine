# Peregrine (version 2.0)
Welcome to the repository of our discord bot, peregrine! (version 2.0)

<br/>

Features:
 - Custom role menu
 - Custom role button
 - More functionality coming soon™️

<br/>

Note that pushing to main will automatically update the live discord bot. (If anyone knows how to do this properly with cogs instead of the current messy system PLEASE LMK)

Come chat in #club-projects on our discord server if you have any questions or comments!

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>


You can run this bot manually with `main.py`, but we highly reccomend you use Docker!

This bot is designed to run with our server setup at [https://github.com/langaracpsc/server/tree/main](https://github.com/langaracpsc/server/tree/main) but it is also possible to run the image alone (not reccomended):

- Download [Docker](https://www.docker.com/)
- Obtain a discord [bot token](https://docs.pycord.dev/en/stable/discord.html)
- Pull the image for peregrine with `docker pull ghcr.io/langaracpsc/peregrine:main`
- Run the image with `docker run -e DISCORD_TOKEN=your_discord_token_here -d --name peregrine ghcr.io/langaracpsc/peregrine:main`
    - -e passes in the discord token
    - -d runs the container in background
    - --name sets name of container
- run `docker logs peregrine` to check that the bot launched correctly.
- run `docker stop peregrine` and `docker rm peregrine` to stop and clear the container.
