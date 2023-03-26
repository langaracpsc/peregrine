Welcome to the discord repository of peregrine (version 2.0)!

<br/>

You can run this bot manually with `main.py`, but we highly reccomend you use Docker!

To run the bot you can use our server setup at [https://github.com/langaracpsc/server/tree/main](https://github.com/langaracpsc/server/tree/main)(reccomended) or run the image alone:

- Download Docker
- Obtain a discord bot token
- Pull the image for peregrine with `docker pull ghcr.io/langaracpsc/peregrine:main`
- Run the image with `docker run -e DISCORD_TOKEN=your_discord_token_here -d -i --name peregrine ghcr.io/langaracpsc/peregrine:main`
    - -e forwards the token to the python code
    - -d runs container in background
    - -i keeps std open
    - --name sets name of container
- run `docker logs peregrine` to check that the bot launched correctly
- run `docker stop peregrine` and `docker rm peregrine` to stop and clear the container


(Almost all functionality in this bot is hardcoded to roles in the langara computer science club discord. Fork the bot if you want to use it in another server!)

<br/>
<br/>

Contact Highfire1#1942 if you have questions about the bot!

More functionality coming soon™️
