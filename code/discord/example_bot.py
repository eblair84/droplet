import discord, requests
from bs4 import BeautifulSoup

client = discord.Client()

@client.event

async def on_ready():
	print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    content = message.content
    payload = {'string1':'hello world!'}
    return_msg = ''
    if message.author == client.user:
        return
    if content.startswith('!8k'):
       msgParts = content.split(' ')
       if len(msgParts) < 4:
            return_msg = 'You missed a part of the request\rUsage: ![Ticker][Qtr][Year].'
            await message.channel.send(return_msg)
            return
       tkr = msgParts[1]
       qtr = msgParts[2]
       yr = msgParts[3]

    await message.channel.send('You wanted to know about 8k for Q{}, {} with {}.'.format(qtr,yr,tkr))
# 	await message.channel.send(payload)


client.run('NDY0OTQxMzY1NjcxNzU1Nzc2.XxoIkQ.96GWPW01t6VH8g9l6PNRwP5PVMQ')
