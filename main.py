from pystyle import *
import requests
import time
import json

token = 'X'
id = 'X'

def get_response():
    return f'[{Col.purple}!{Col.reset}]'

def getheaders(token):
    headers = {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    }
    
    if token: 
        headers.update({"Authorization": token})
    return headers

def check_token(token):
    r = requests.get('https://discord.com/api/v9/users/@me', headers=getheaders(token))
        
    if r.status_code == 200:
        pass
    else:
        input(f'{Col.red}invalid token')
        exit()

def get_api():
    return 'https://discord.com/api/v8'

def get_guild():
    global guild_requests
    guild_requests = requests.get(f"{get_api()}/users/@me/guilds", headers=getheaders(token)).json()

def get_ban(guild_id):
    global get_bans
    get_bans = requests.get(f'{get_api()}/guilds/{guild_id}/bans', headers=getheaders(token))

def spoof_user(guild_id,user_id):
    global spoof_requests
    
    header = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyLUZSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE2MTg4NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        'authorization' : token
    }
    
    spoof_requests = requests.delete(f'{get_api()}/guilds/{guild_id}/bans/{user_id}', headers=header)


def spoof():
    
    get_guild()

    for guild in guild_requests:
        guild_id = guild['id']
        guild_name = guild['name']
        
        get_bans = requests.get(f'{get_api()}/guilds/{guild_id}/bans',
                            headers=getheaders(token))
        
        if get_bans.status_code == 200:
            print(f'{get_response()} checking guild : {Col.yellow}{guild_name}{Col.white} id : {Col.blue}{guild_id}{Col.white} permissions : {Col.green}True{Col.reset}')
            for user_ban in get_bans:
                
                print(f'     ╚> User ban in : {Col.yellow}{guild_name}{Col.white}')
            for user_ban in get_bans.json():
                    #print(get_bans.json())
                
                user_id = user_ban['user']['id']
                user_name = user_ban['user']['username']
                    
                if user_id == id:
                    print(f'         ╚> User ban id : {Col.yellow}{user_id}{Col.white} name : {Col.pink}{user_name}{Col.white} corresponding : {Col.green}True{Col.reset}')
                    time.sleep(1)
                    spoof_user(guild_id,user_id)

                    print(f'         ╚> {Col.green}Succesfully spoof {user_name} from {guild_name}{Col.reset}')
                    
                else:
                    print(f'         ╚> User ban id : {Col.yellow}{user_id}{Col.white} name : {Col.pink}{user_name}{Col.white} corresponding : {Col.red}False{Col.reset}')
        else:
            print(f'{get_response()} checking guild : {Col.yellow}{guild_name}{Col.white} id : {Col.blue}{guild_id}{Col.white} permissions : {Col.red}False{Col.reset}')

spoof()