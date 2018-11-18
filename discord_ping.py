import discord
from discord.ext import commands
import requests
import keywords as k
from datetime import time
from datetime import datetime

requests.packages.urllib3.disable_warnings()

TOKEN = 'NTEzNTI2NTE4NTE3ODU4MzE1.DtJT8A.2Z4SK1w2y8LP4-Nu_W6-OGwCDuc' #SET YOUR BOT TOKEN HERE 

client = discord.Client()
keywords = k.keywords
''' Store the channel name as key, store date as value '''
posted_channels = dict()

def channel_check(channel, keyword, sub_key):
    ''' Check if the channel already exists in the dictionary '''
    if channel in posted_channels:
        posted_channels[channel]
        ch_values = posted_channels[channel]

        for item in ch_values:
            ''' Retrieve stored time '''
            prev_time = item[0]
            ''' Retrieve current time '''
            curr_time = datetime.time(datetime.now().replace(microsecond=0))
            ''' Format the time and get the difference between the current and previous time '''
            fmt = "%H:%M:%S"
            diff = datetime.strptime(str(curr_time), fmt) - datetime.strptime(str(prev_time), fmt)

            ''' If its been longer than a minute '''
            if (str(diff) >= "0:01:00"):
                ''' Means its okay to post again '''
                return False
            else:
                if keyword == item[1] and sub_key == item[2]:
                    ''' It hasnt been 1 minute and keyword and sub keyword were already pinged '''
                    return True
                else:
                    return False
    else:
        posted_channels[channel] = []
        return False

    print(str(diff))
    return True

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    for keyword in keywords:
        sub_keys = keywords[keyword]
        for sub_key in sub_keys:
            if keyword.lower() in message.content.lower() and sub_key.lower() in message.content.lower() and (message.channel.name == "general" or message.channel.name =="urgent"): # SET YOUR CHANNEL NAME HERE
                has_posted = channel_check(str(message.channel), keyword, sub_key)
                if has_posted == False:
                    posted_channels[str(message.channel)].append((datetime.time(datetime.now().replace(microsecond=0)), keyword, sub_key))
                    await client.send_message(message.channel,f"@Restocks - keyword matched: {keyword} {sub_key}") #SET YOUR MESSAGE HERE YOU WANT TO USE     
                


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

while True:
    client.run(TOKEN)


