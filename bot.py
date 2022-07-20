import discord
import configparser
import random
from datetime import datetime


class MyClient(discord.Client):
    async def on_ready(self):
        print("Ready to insults someone! ÒwÓ")

    async def on_message(self, message):
        if message.guild.get_role(target) in message.author.roles: # Only take action if the message author has target role assigned
            number = random_number()
            if number == 69:
                # Get insult and mock this fucker with his own words
                insult = get_insult()
                await message.channel.send(f'"{alternate_case(message.content)}" - {insult}')

            # Internal terminal output so you can see that the bot is properly working
            # Everytime a target group member writes a message you can see the 
            # current time, the authors name, and the generated random number for that message
            print(f"{datetime.now()}   {message.author}    {number}")


def get_config(language_list):
    print("Load config...")

    config = configparser.ConfigParser()
    config.read("config.txt")

    token = config['DEFAULT']['token']
    while token == 'BOT_TOKEN_HERE' or token == '':         # Check if a bot token is already in config file. If not, politely ask for one
        token = input("Please enter a valid bot token: ")
    print("Bot token loaded...")

    language = config['DEFAULT']['language']
    possible_languages = language_list
    while language.lower() not in possible_languages:       # Check if the chosen language is available. If not, politely ask for an available one
        language = input("Please enter an available language [GER|ENG]: ")
    print(f"Language: {language}...")

    target = config['DEFAULT']['target']
    while target == 'ROLE_ID_HERE' or target == '':
        target = input("Please enter a valid group id: ")   # Check if a group id is already in config file. If not, politely ask for one
    try:
        target = int(target)    # Check if target string can be converted to integer. If not, it isn't a valid id
    except:
        print("No valid group id...")
        print("Terminate...")
        exit()
    print(f"Targeted group id is {target}...")
    
    return token, language, target


def get_insult():
    # Parse the chosen insult file line by line and randomly select an insult
    # This happens everytime a vicitm is chosen so that you can edit the insults while the bot is running
    insults = open(f"insults_{language.lower()}.txt", "r").readlines()
    insult = insults[random.randint(0, len(insults))]
    return insult


def random_number():
    # Determine if someone gets some attention by generating a random number
    # If the number matches the funny number, insult this fucker
    rand_num = random.randint(1, 100)
    return rand_num


def alternate_case(string):
    # Mock the target by quote its silly words in a very sarcastic way...
    changed_string = ""
    i = True
    for char in string:
        if i:
            changed_string += char.upper()  # Alternately change the characters in a string to lowercase or uppercase
        else:
            changed_string += char.lower()
        if char != ' ':     # Skip spaces
            i = not i
    return changed_string


language_list = ['ger', 'eng'] # Available languages (Might put that in the config file in the future...)

global language, target
token, language, target = get_config(language_list)
print("Config loaded...")

print("Logging in...")
client = MyClient()
client.run(token)
