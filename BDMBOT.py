import datetime
import json
import aiohttp
import discord
import numpy as np
import requests
import xmltodict
from bs4 import BeautifulSoup
from discord import app_commands
import random


mercsmemberlists = []
akamemberlists = []
gymmemberlists = []
enragedmemberlists = []

cookies = {
    PUT YOUR COOKIE HERE
}
loginheaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': 'https://dbonk.com',
    'Referer': 'https://dbonk.com/bdmbsmv2/login.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

logindata = {
    'action': 'login',
    'username': 'USERNAME',
    'password': 'PASSWORD',
}

loginsession = requests.Session()
sendlogin = requests.post('https://dbonk.com/bdmbsmv2/login.php', headers=loginheaders, data=logindata, cookies=cookies)
TOKEN = "BOTTOKENHERE"
GUILD = "GUILDIDHERE"
headers = {
    'Accept': '*/*',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://dbonk.com',
    'Referer': 'https://dbonk.com/bdmbsmv2/index.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def login():
    global loginheaders, logindata, cookies
    requests.post('https://dbonk.com/bdmbsmv2/login.php', headers=loginheaders, data=logindata, cookies=cookies)


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync(guild=discord.Object(
                id=GUILD))  # guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True


aclient = client()
tree = app_commands.CommandTree(aclient)


@tree.command(guild=discord.Object(id=GUILD), name='blacksun', description='black sun')  # guild specific slash command
@app_commands.default_permissions()
async def bsakatsuki(interaction: discord.Interaction, checkdate: str):
    await interaction.response.defer()
    global cookies, loginheaders, headers, logindata
    login()

    data = {
        'type': 'changechan',
        'channel': 'nodesiege',
    }

    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)

    data = {
        'type': 'getstats',
        'guildid': 'g40',
    }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    gymlist = []
    pointdata = ""
    counterxxx = 0
    gymplayername = ""
    siteJson = json.loads(response.text)

    for o in siteJson["members"]:
        gymlist.append(o["playerid"])
    for i in gymlist:
        if counterxxx == 10:
            embed = discord.Embed(title="xAKATSUKIx")
            embed.add_field(name="Name", value=gymplayername)
            embed.add_field(name="POINTS", value=pointdata)
            await interaction.followup.send(embed=embed)
            pointdata = ""
            gymplayername = ""
            counterxxx = 0
        data = {
            'type': 'getstats',
            'playerid': i,
        }
        response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
        siteJson = json.loads(response.text)
        try:
            date = siteJson["rankp"]["blacksun"]["date"]
        except Exception:
            family_name = siteJson["playerinfo"]["family_name"]
            gymplayername = gymplayername + family_name + "\n"
            pointdata = pointdata + "Not in top 300 / No info " + "\n"
            counterxxx = counterxxx + 1
            continue
        date = siteJson["rankp"]["blacksun"]["date"]
        if checkdate != date:
            family_name = siteJson["playerinfo"]["family_name"]
            gymplayername = gymplayername + family_name + "\n"
            pointdata = pointdata + "Not in top 300 / No info " + "\n"
            counterxxx = counterxxx + 1
            continue
        date = siteJson["rankp"]["blacksun"]["date"]

        points = siteJson["rankp"]["blacksun"]["points"]

        rank = siteJson["rankp"]["blacksun"]["rank"]
        pointdata = pointdata + "Points = " + points + " Date = " + date + " Rank = " + rank + "\n"
        family_name = siteJson["playerinfo"]["family_name"]
        gymplayername = gymplayername + family_name + "\n"
        counterxxx = counterxxx + 1

    gymplayername = gymplayername + "This is the end."
    embed = discord.Embed(title="AKATSUKI")
    embed.add_field(name="Name", value=gymplayername)
    embed.add_field(name="POINTS", value=pointdata)

    await interaction.followup.send(embed=embed)


@tree.command(guild=discord.Object(id=GUILD), name='memberlist',
              description='Check member list')  # guild specific slash command

async def xakatsukixlist(interaction: discord.Interaction):
    global cookies, loginheaders, headers, logindata
    await interaction.response.defer()
    login()
    data = {
        'type': 'changechan',
        'channel': 'nodesiege',
    }

    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    mercsmemberlist = ""
    mercscplist = ""
    mercsfcplist = ""
    mercscounter = 0
    data = {
        'type': 'getstats',
        'guildid': 'g40',
    }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    raw = response.text
    siteJson = json.loads(response.text)
    for o in siteJson['members']:
        mercsmemberlist = mercsmemberlist + o["playername"] + "\n"
    for p in siteJson["members"]:
        mercscplist = mercscplist + p["cpm"] + "\n"
    for p in siteJson["members"]:
        characterclass = p["class"]
        mercsfcplist = mercsfcplist + characterclass.split("title=",1)[1] + "\n"

    embed = discord.Embed(title="xAKATSUKIx")
    embed.add_field(name="Name", value=mercsmemberlist)
    embed.add_field(name="CP", value=mercscplist)
    embed.add_field(name="Class", value=mercsfcplist)
    await interaction.followup.send(embed=embed)


@tree.command(guild=discord.Object(id=GUILD), name='nodewar',
              description='Check if we have a node war')  # guild specific slash command
async def nodewar(interaction: discord.Interaction):
    global cookies, loginheaders, headers, logindata
    await interaction.response.defer()
    login()
    data = {
        'type': 'changechan',
        'channel': 'nodesiege',
    }

    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    datenow = datetime.datetime.now()
    datelater = datenow + datetime.timedelta(hours=-15)
    data = {
        'type': 'search',
        'query': 'xAKATSUKIx',
    }

    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    dates = str(datelater) + " to " + str(datenow)
    data = {
        'type': 'changedate',
        'filter': dates,
    }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    params = {
        'type': 'newchat',
        'mtd': 'sse',
    }
    response = requests.get('https://dbonk.com/bdmbsmv2/', params=params, cookies=cookies, headers=headers)
    if response.json == "<div id='noref nsf'><div>No Search Found...</div></div>":
        await interaction.followup.send("We have no nodewar.")
    databox = response.text.removeprefix("data: ")
    from lxml import etree
    parser = etree.XMLParser(recover=True)
    doc = etree.fromstring(databox, parser=parser)
    workingxml = xmltodict.parse(etree.tostring(doc))
    data = {
        'type': 'getstats',
        'nwwarid': workingxml["div"]["@id"],
    }
    response = requests.post('https://dbonk.com/bdmbsmv2/', data=data, cookies=cookies, headers=headers)
    raw = response.text
    siteJson = json.loads(raw)
    try:
        if 'xAKATSUKIx' in ([d.get('guild') for d in siteJson['guilds'] if d.get('guild')]):
            guilds = [d.get('guild') for d in siteJson['guilds'] if d.get('guild')]
            guild1 = guilds[0]
        if len(guilds) > 1:
            guild2 = guilds[1]
        if len(guilds) > 2:
            guild3 = guilds[2]
        warinfo = siteJson.get('warinfo')
        nwtime = warinfo.get('wartime')
        location = warinfo.get('location')
        averagecp = [d.get('averagecp') for d in siteJson['guilds'] if d.get('averagecp')]
        a1 = "Have war : "
        embed = discord.Embed(title="We have a war!", description=guilds)
        embed.add_field(name="Average CP", value=averagecp)
        embed.add_field(name="Time", value=nwtime)
        embed.add_field(name="Location", value=location)
        await interaction.followup.send(embed=embed)
    except:
        await interaction.followup.send("We have no nodewar.")
@tree.command(guild = discord.Object(id=GUILD), name = 'addmanual', description='add someone manually') #guild specific slash command

async def addmanual(interaction: discord.Interaction, name:str):
    writeable = "\n" + name
    with open("manual.txt","a", encoding="utf8", ) as file_object:
        file_object.write(writeable)
    await interaction.response.send_message("Done, added " + name)
@tree.command(guild=discord.Object(id=GUILD), name='couponredeemer',
              description='Redeem coupons')  # guild specific slash command

async def couponredeemer(interaction: discord.Interaction, coupon: str):
    
    global cookies, loginheaders, headers, logindata
    couponlist = open("coupons.txt", encoding="utf8").readlines()
    couponend = coupon + "\n"
    if coupon in couponlist:
        await interaction.response.send_message("Coupon already redeemed, cancelling... ")
        return
    elif couponend in couponlist:
        await interaction.response.send_message("Coupon already redeemed, cancelling... ")
        return
    else:
        await interaction.response.defer()
        with open("coupons.txt","a", encoding="utf8", ) as file_object2:
            file_object2.write("\n" + coupon)
        couponcookies = {
            PUT YOUR COOKIE HERE
        }

        couponheaders = {
            'Accept': '*/*',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://game.world.blackdesertm.com',
            'Referer': 'https://game.world.blackdesertm.com/coupon',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        mylist = []
        alreadyredeemedlist = []
        faillist = []
        token1 = 'TOKEN HERE'

        for i in mercsmemberlists:
            
            data = {
                'userNickname': i,
                'region': 'EU',
                '__RequestVerificationToken': token1,
                'couponCode': coupon,
            }
            response = requests.post('https://game.world.blackdesertm.com/Coupon/ApplyCouponInWeb', cookies=couponcookies,
                                    headers=couponheaders, data=data)
            result = json.loads(response.text)
            if result["resultCode"] == 0:
                mylist.append(i)
            elif result["resultCode"] == -20007:
                alreadyredeemedlist.append(i)
            else:
                faillist.append(i)
        embed = discord.Embed(title="DONE MERCS {}".format(coupon))
        embed.add_field(name="Success", value=mylist)
        embed.add_field(name="Already Redeemed", value=alreadyredeemedlist)
        embed.add_field(name="Failed", value=faillist)
    #    await interaction.followup.send(embed=embed)
        mylist = []
        alreadyredeemedlist = []
        faillist = []
        token1 = 'TOKEN HERE'
        for i in gymmemberlists:
            data = {
                'userNickname': i,
                'region': 'EU',
                '__RequestVerificationToken': token1,
                'couponCode': coupon,
            }

            response = requests.post('https://game.world.blackdesertm.com/Coupon/ApplyCouponInWeb', cookies=couponcookies,
                                    headers=couponheaders, data=data)
            result = json.loads(response.text)
            if result["resultCode"] == 0:
                mylist.append(i)
            elif result["resultCode"] == -20007:
                alreadyredeemedlist.append(i)
            else:
                faillist.append(i)    
        embed = discord.Embed(title="DONE GYM {}".format(coupon))
        embed.add_field(name="Success", value=mylist)
        embed.add_field(name="Already Redeemed", value=alreadyredeemedlist)
        embed.add_field(name="Failed", value=faillist)
        
        #await interaction.followup.send(embed=embed)
        
        mylist = []
        alreadyredeemedlist = []
        faillist = []

        for i in akamemberlists:

            data = {
                'userNickname': i,
                'region': 'EU',
                '__RequestVerificationToken': token1,
                'couponCode': coupon,
            }

            response = requests.post('https://game.world.blackdesertm.com/Coupon/ApplyCouponInWeb', cookies=couponcookies,
                                    headers=couponheaders, data=data)
            result = json.loads(response.text)
            if result["resultCode"] == 0:
                mylist.append(i)
            elif result["resultCode"] == -20007:
                alreadyredeemedlist.append(i)
            else:
                faillist.append(i)    
        embed = discord.Embed(title="DONE XAKATSUKI {}".format(coupon))
        embed.add_field(name="Success", value=mylist)
        embed.add_field(name="Already Redeemed", value=alreadyredeemedlist)
        embed.add_field(name="Failed", value=faillist)
        await interaction.followup.send(embed=embed)
        mylist = []
        alreadyredeemedlist = []
        faillist = []

        for i in enragedmemberlists:

            data = {
                'userNickname': i,
                'region': 'EU',
                '__RequestVerificationToken': token1,
                'couponCode': coupon,
            }

            response = requests.post('https://game.world.blackdesertm.com/Coupon/ApplyCouponInWeb', cookies=couponcookies,
                                    headers=couponheaders, data=data)
            result = json.loads(response.text)
            if result["resultCode"] == 0:
                mylist.append(i)
            elif result["resultCode"] == -20007:
                alreadyredeemedlist.append(i)
            else:
                faillist.append(i)    
        embed = discord.Embed(title="DONE ENRAGED {}".format(coupon))
        embed.add_field(name="Success", value=mylist)
        embed.add_field(name="Already Redeemed", value=alreadyredeemedlist)
        embed.add_field(name="Failed", value=faillist)
        await interaction.followup.send(embed=embed)
        
        webhook.send(embed=embed)
        List = open("manual.txt", encoding="utf8").readlines()
        mylist = []
        alreadyredeemedlist = []
        faillist = []
        mercs2list = []
        for o in List:
            mercs2list.append(o.strip().split('\n'))
        for i in mercs2list:

            data = {
                'userNickname': i,
                'region': 'EU',
                '__RequestVerificationToken': token1,
                'couponCode': coupon,
            }

            response = requests.post('https://game.world.blackdesertm.com/Coupon/ApplyCouponInWeb', cookies=couponcookies,
                                    headers=couponheaders, data=data)
            result = json.loads(response.text)
            if result["resultCode"] == 0:
                mylist.append(i)
            elif result["resultCode"] == -20007:
                alreadyredeemedlist.append(i)
            else:
                faillist.append(i)
        embed = discord.Embed(title="DONE MANUAL {}".format(coupon))
        embed.add_field(name="Success", value=mylist)
        embed.add_field(name="Already Redeemed", value=alreadyredeemedlist)
        embed.add_field(name="Failed", value=faillist)
        await interaction.followup.send(embed=embed)
@tree.command(guild = discord.Object(id=GUILD), name = 'siegelist', description='Check siege attendee list') #guild specific slash command

async def tesstt(interaction: discord.Interaction):
    await interaction.response.defer()
    global cookies, loginheaders, logindata, headers
    login()



    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://dbonk.com/bdmbsmv2/login.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    response = requests.get('https://dbonk.com/bdmbsmv2/index.php', cookies=cookies, headers=headers)


    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://dbonk.com',
        'Referer': 'https://dbonk.com/bdmbsmv2/index.php',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'type': 'getinfo',
        'channel': 'nodeholder',
    }

    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    print(response.text)
    siteJson = json.loads(response.text)
    List1 = ""
    List2 = ""
    List3 = ""
    for nodes in siteJson["graphs"]:
        if siteJson["graphs"][nodes]["info"]["tier"] == 'T2':
            List1 += siteJson["graphs"][nodes]["info"]["name"] + "\n"
            List2 += siteJson["graphs"][nodes]["info"]["tier"] + "\n"
            List3 += siteJson["graphs"][nodes]["holder"][8]["holder"] + "\n"
    for nodes in siteJson["graphs"]:
        if siteJson["graphs"][nodes]["info"]["tier"] == 'T3':
            List1 += siteJson["graphs"][nodes]["info"]["name"] + "\n"
            List2 += siteJson["graphs"][nodes]["info"]["tier"] + "\n"
            List3 += siteJson["graphs"][nodes]["holder"][8]["holder"] + "\n"
    embed = discord.Embed(title="Possible siege attendees")
    embed.add_field(name="Node Name", value=List1)
    embed.add_field(name="Tier", value=List2)
    embed.add_field(name="Holder", value=List3)
    await interaction.followup.send(embed=embed)
@tree.command(guild = discord.Object(id=GUILD), name = 'stackednodes', description='Check all the nodes if they are stacked or not broken due to dbnk') #guild specific slash command

async def tesstt(interaction: discord.Interaction):
    await interaction.response.defer()
    global cookies, loginheaders, logindata, headers
    login()



    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://dbonk.com/bdmbsmv2/login.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    response = requests.get('https://dbonk.com/bdmbsmv2/index.php', cookies=cookies, headers=headers)


    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://dbonk.com',
        'Referer': 'https://dbonk.com/bdmbsmv2/index.php',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'type': 'getinfo',
        'channel': 'nodeholder',
    }

    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    print(response.text)
    siteJson = json.loads(response.text)
    List1 = ""
    List2 = ""
    List3 = ""
    counter = 0
    countback = 8
    for nodes in siteJson["graphs"]:
        
        if siteJson["graphs"][nodes]["holder"][8]["holder"] == "" or "No Bidder":
            List1 += siteJson["graphs"][nodes]["info"]["name"] + " / " + siteJson["graphs"][nodes]["info"]["day"] + " / " + siteJson["graphs"][nodes]["info"]["time"] + "\n"
            List2 += siteJson["graphs"][nodes]["info"]["tier"] + "\n"
            counter = 0
            countback = 8
            
            while countback >= 0:
                countback -= 1
                counter += 1
                if siteJson["graphs"][nodes]["holder"][countback]["holder"] != "" or "No bidder":
                    countback = -1
            if counter == 8:
                List3 += "Stacked 8+ days" + "\n"
                embed = discord.Embed(title="Stacked nodes")
                embed.add_field(name="Node Name", value=siteJson["graphs"][nodes]["info"]["name"] + " / " + siteJson["graphs"][nodes]["info"]["day"] + " / " + siteJson["graphs"][nodes]["info"]["time"] + "\n")
                embed.add_field(name="Tier", value=siteJson["graphs"][nodes]["info"]["tier"] + "\n")
                embed.add_field(name="Days", value="Stacked 8+ days" + "\n")
                await interaction.followup.send(embed=embed)
            elif counter >= 2:
                List3 += "Stacked " + str(counter) + " days" + "\n"
                embed = discord.Embed(title="Stacked nodes")
                embed.add_field(name="Node Name", value=siteJson["graphs"][nodes]["info"]["name"] + " / " + siteJson["graphs"][nodes]["info"]["day"] + " / " + siteJson["graphs"][nodes]["info"]["time"] + "\n")
                embed.add_field(name="Tier", value=siteJson["graphs"][nodes]["info"]["tier"] + "\n")
                embed.add_field(name="Days", value="Stacked " + str(counter) + " days" + "\n")
                await interaction.followup.send(embed=embed)
            
@tree.command(guild=discord.Object(id=GUILD), name='primeredeemer',
              description='Redeem coupons')  # guild specific slash command

async def couponredeemer(interaction: discord.Interaction, coupon: str):
    await interaction.response.defer()
    global cookies, loginheaders, headers, logindata
    login()
    data = {
        'type': 'getstats',
        'guildid': 'g40',
    }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    siteJson = json.loads(response.text)
    mercs2list = []
    for i in siteJson["members"]:
        mercs2list.insert(0, i["playername"])
    couponheaders = {
        'Accept': '*/*',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://game.world.blackdesertm.com',
        'Referer': 'https://game.world.blackdesertm.com/coupon',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    mylist = []
    alreadyredeemedlist = []
    faillist = []
    token1 = 'TOKEN HERE'

    while True:
        randomnumber = mercs2list[random.randint(0,47)]
        data = {
            'userNickname': randomnumber,
            'region': 'EU',
            '__RequestVerificationToken': token1,
            'couponCode': coupon,
        }
        response = requests.post('https://game.world.blackdesertm.com/Coupon/ApplyCouponInWeb', cookies=couponcookies,
                                 headers=couponheaders, data=data)
        result = json.loads(response.text)
        if result["resultCode"] == 0:
            mylist.append(randomnumber)
            
            break
        elif result["resultCode"] == -20007:
            alreadyredeemedlist.append(randomnumber)
        else:
            faillist.append(randomnumber)
    embed = discord.Embed(title="DONE prime")
    embed.add_field(name="Success", value=mylist)
    embed.add_field(name="Already Redeemed", value=alreadyredeemedlist)
    embed.add_field(name="Failed", value=faillist)
    await interaction.followup.send(embed=embed)


@tree.command(guild = discord.Object(id=GUILD), name = 'refreshmemberlist', description='memberlist') #guild specific slash command

async def refreshmemberlist(interaction: discord.Interaction):
    global cookies, loginheaders, headers, logindata, mercsmemberlists, gymmemberlists, akamemberlists, enragedmemberlists
    await interaction.response.defer()
    
    mercsmemberlists = []
    gymmemberlists = []
    akamemberlists = []
    enragedmemberlists = []
    login()
    data = {
            'type': 'getstats',
            'guildid': 'g4793',
        }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    siteJson = json.loads(response.text)
    for i in siteJson["members"]:
        
        mercsmemberlists.append(i["playername"])
    
    data = {
            'type': 'getstats',
            'guildid': 'g40',
        }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    siteJson = json.loads(response.text)
    for i in siteJson["members"]:
        gymmemberlists.append(i["playername"])
    data = {
            'type': 'getstats',
            'guildid': 'g16081',
        }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    siteJson = json.loads(response.text)
    for i in siteJson["members"]:
        akamemberlists.append(i["playername"])
    data = {
            'type': 'getstats',
            'guildid': 'g16049',
        }
    response = requests.post('https://dbonk.com/bdmbsmv2/', cookies=cookies, headers=headers, data=data)
    siteJson = json.loads(response.text)
    for i in siteJson["members"]:
        enragedmemberlists.append(i["playername"])
    
        
    await interaction.followup.send("Done")

aclient.run(TOKEN)

