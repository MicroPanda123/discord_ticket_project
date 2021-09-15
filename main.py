import os
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import random
from os.path import isfile

with open('token.txt', 'r') as token_file:
	TOKEN = token_file.read()
client = commands.Bot(command_prefix='.')
client.remove_command('help')
permissions = 230750179874045952
ignored = ['i', 'a', 'and', 'but', 'then', 'that', 'you', 'me']

def count_words(guild, member, text):
	text = text.lower() #make text lowercase so it won't count different cases as different words
	if not text in ignored and member != client.user.name:
		import json
		from os.path import isfile
		text = text.split(' ')
		if not(isfile('words.json')):
		    with open('words.json', 'w') as words:
		        json.dump({'testguild': {'testmember': {'test_word': 1}}}, words) #create testmember for json file if not existing
		with open('words.json') as words:
		    data = json.load(words) #read data from json file
		try:
		    guild_data = data[f'{guild}']
		except KeyError as e:
		    print("New guild")
		    guild_data = {'member': 0}
		try:
		    member_data = guild_data[f'{member}'] #read data of specified member
		except KeyError as e:
		    print("New user")
		    member_data = {'word': 0} #create template data for new member
		for word in text:
		    try:
		        said = member_data[f'{word}'] #get info if word was said and how much
		    except KeyError as e:
		        said = 0 #set said counter to one if word was never said
		    said += 1
		    write_data = {f'{word}': said}
		    #print(write_data)
		    member_data.update(write_data) #update members data
		guild_write_data = {f'{member}': member_data}
		guild_data.update(guild_write_data)
		final_data = {f'{guild}': guild_data} #update members data for whole json
		data.update(final_data) #add members data to final
		#print(data)
		with open('words.json', 'w') as words:
		    json.dump(data, words, indent=3) #save json data to file

def get_words(): #get data from json file
    import json
    with open('words.json') as words:
        data = json.load(words)
    return data

def get_guild(guild: discord.Guild):
    return get_words()[f'{guild.id}']

def get_member_words(guild: discord.Guild, member: discord.Member): #get members data from json file
    return get_guild(guild)[f'{member.id}']

def get_usages_of_word_per_member(guild: discord.Guild, member: discord.Member, word): #get usages of word from specific user
    member_words = get_member_words(guild, member)
    try:
        usages = member_words[f'{word}']
    except KeyError:
        usages = 0
    return usages

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_command_error(ctx, error):
	creator = await client.fetch_user(230750179874045952)
	if isinstance(error,
	              (MissingRequiredArgument, BadArgument, ArgumentParsingError)):
		await ctx.channel.send(error)
	else:
		await ctx.channel.send(str(error) + f" report that to {creator}")


@client.event
async def on_message(message):
    msg = message.content
    count_words(message.guild.id, message.author.id, msg)
    await client.process_commands(message)


client.run(TOKEN)
