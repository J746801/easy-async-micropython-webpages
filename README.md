# Easy asynchronous webpages hoster
A very easy way to host multiple webpages with micropython.
# Use
Simply connect to a wifi network, create a Webpage() object (see example.py for example), then use asyncio.create_task(Webpage.start()) and asyncio.run() to start, while allowing other asynchronous tasks to run.
