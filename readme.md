Welcome to the discord repository of peregrine (version 2.0)!

<br/>

(Almost all functionality in this bot is hardcoded to roles in the langara computer science club discord. Fork the bot if you want to use it in another server!)

<br/>
<br/>

Contact Highfire1#1942 if you have questions about the bot!

More functionality coming soon™️


You can run this bot manually with `main.py`, but we highly reccomend you use Docker!

This bot is designed to run with our server setup at [https://github.com/langaracpsc/server/tree/main](https://github.com/langaracpsc/server/tree/main) but it is also possible to run the image alone (not reccomended):

- Download [Docker](https://www.docker.com/)
- Obtain a discord [bot token](https://docs.pycord.dev/en/stable/discord.html)
- Pull the image for peregrine with `docker pull ghcr.io/langaracpsc/peregrine:main`
- Run the image with `docker run -e -d DISCORD_TOKEN=your_discord_token_here --name peregrine ghcr.io/langaracpsc/peregrine:main`
    - -e passes in the discord token
    - -d runs container in background
    - --name sets name of container
- run `docker logs peregrine` to check that the bot launched correctly.
- run `docker stop peregrine` and `docker rm peregrine` to stop and clear the container.