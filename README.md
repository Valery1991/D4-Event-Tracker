# Diablo 4 Event Tracker
Personal Python project to track Diablo 4 events through webhooks in discord. 

This code will post a message to the discord server and channel of the webhook url, containing timers for:
- Boss spawn
- Helltide
- Legion

Name and location will be included if applicable. For Helltide, there is also an attached image of the map containing possible special chest spawns.
It will show how long it has been since the last world boss and last legion event, which boss the next will be and when the next expected spawn is. 

You can run this locally by executing `python d4_events.py`, but if you want to keep it running 24/7, I suggest getting a cheap server (I use [Sparked](https://sparkedhost.com/)).
