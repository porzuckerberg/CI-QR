import os
import cv2
import qrcode
import discord
import datetime
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from itertools import cycle
from discord.ext import commands, tasks


def newURL(URL) :
    return "https://media.discordapp.net/attachments/"+URL.split("/attachments/")[1]+"?width=672&height=897"

def QRToCode(newURL):
    response = requests.get(newURL)
    image = Image.open(BytesIO(response.content))
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    detector = cv2.QRCodeDetector()
    decoded_data, points, _ = detector.detectAndDecode(gray)

    if decoded_data:
        strr = ""
        for data in decoded_data:
          strr = strr+str(data)
        return strr
    else:
        return "QR CODE NOT FOUND"
#===========================================================================================================================

TestRoomID  = '''
1117158081420349552
1117053877812998186
'''.strip().split("\n")

AdminRoomID = '''
1116617021430431794
1116617227630805002
1116617477615521822
1116617519806038126
1116617560654356531
1116617590782038066
1116617617696895017
1116617655797948417
1116617698231726121
1116617722923581450
1116617749624520816
1116617778003202078
1116617810542592071
1116617840791924736
1116617865114681444
1116623348089241650
1116623441206968330
1116623465747853312
1116623490955612283
1116623518956785695
1117167377537302599
1117216551368663050
'''.strip().split("\n")

CodeList = '''
SIR12345678
SIR87654321
SIR00000000
SIR88888888
SIR74185263
SIR96385274
SIR78945612
SIR25836947
SIR36958014
SIR45632105
'''.strip().split("\n")

StatusList,Checker,Time= [],[],[]
   
for i in range(len(CodeList))  :    
    StatusList.append(True)
    Checker.append("")
    Time.append("")

#===========================================================================================================================
intents = discord.Intents.default()
intents.members = True
self  = commands.Bot(command_prefix='stand ', intents=intents)

statuss = cycle([ 'Singing' , 'in the' , 'Rain'    ])
ac      = cycle([ discord.Status.dnd , discord.Status.idle , discord.Status.online    ])
T = '='*28
 
@self.event
async def on_ready():   
    change_status.start()    
    print(self.user.name,"ONLINE !") 
  
@tasks.loop(seconds=3)
async def change_status():
    await self.change_presence(status=next(ac), activity=discord.Game(next(statuss)) )    
    #await self.change_presence(status=discord.Status.offline)


#===========================================================================================================================
self.remove_command('help')
#===========================================================================================================================


# #===========================================================================================================================
# #=========================================================================================================================== 
# #=========================================================================================================================== 
@self.event
async def on_message(message):     
    now = (datetime.datetime.now()).strftime("%#d %B %Y, %H:%M:%S ")
    name = str(message.author)  
    ID = str(message.author.id)
    if ID == "1116626317241237567": return
    tag = "<@!"+ID+">"  
    content = '"'+str(message.content)+'"'
    try:
        server = str(message.author.guild)
    except:
        server = ' '
    try:
        MU=message.attachments[0].url
    except:
        MU=''    
    room = str(message.channel)
    
# #===========================================================================================================================
# #=========================================================================================================================== 
# #=========================================================================================================================== LOG
    strr = '''    
    Name     : %s
    ID       : %s
    Server   : %s
    Channel  : %s'''%(name,tag,server,room) 
    if content != '""':
        strr += "\n    Content  : %s"%content
    if MU != '':
        strr += "\n    Media URL: %s"%MU            
    print('\n\n************ '+now+'************'+strr+"\n************************************************")
    if MU :  
        result = (QRToCode(newURL(MU)))
        print(result)   
# #===========================================================================================================================
# #===========================================================================================================================
# #=========================================================================================================================== Test Detect/Decode
        if str(message.channel.id) in TestRoomID :                       
            embed = discord.Embed(title=result, description="\n" + "\n===================================", color=discord.Color.green())  
            embed.set_footer(text=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")              
            await message.channel.send(embed=embed)
            
# #===========================================================================================================================
# #===========================================================================================================================
# #=========================================================================================================================== Check QR-Code
        elif str(message.channel.id) in AdminRoomID :            
            if result == "QR CODE NOT FOUND" :
                embed = discord.Embed(title="ไม่พบ QR-Code กรุณาถ่ายภาพใหม่", description="\n" + "\n===================================", color=discord.Color.red())  
                embed.set_footer(text=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")              
                await message.channel.send(embed=embed)
            else :
                if result in CodeList :
                    indexNumber = CodeList.index(result)
                    username = "user"+CodeList[indexNumber][0:3]
                    phone    = "09"+CodeList[indexNumber][3:]
                    
                    data = "**ข้อมูลบัตร %s**\nชื่อ-สกุล : %s\nเบอร์โทร : %s"%(result,username,phone)
                    print(data)
                    
                    if StatusList[indexNumber] :     
                        StatusList[indexNumber] = False      
                        Checker[indexNumber]    = name   
                        Time[indexNumber]       = now 
                            
                        embed = discord.Embed(title=result+" สามารถใช้งานได้ ✅", description="\n" + "\n===================================\n"+data, color=discord.Color.green())  
                        embed.set_footer(text=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")              
                        await message.channel.send(embed=embed)
                        print("\nสามารถใช้งานได้")
                        
                    else :
                        descriptionx = "ผู้เช็ค : "+Checker[indexNumber]  
                        descriptionx +="\nเวลาที่เช็ค : "+Time[indexNumber]                         
                        embed = discord.Embed(title=result+" ถูกใช้งานแล้ว ❌", description="\n" +descriptionx+ "\n===================================\n"+data, color=discord.Color.red())  
                        embed.set_footer(text=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")              
                        await message.channel.send(embed=embed)
                        print(descriptionx+"\n\nถูกใช้แล้ว") 
                        
                else :
                    embed = discord.Embed(title="QR-Code ไม่อยู่ในระบบ (บัตรปลอม)", description="\n" +result+ "\n===================================", color=discord.Color.red())  
                    embed.set_footer(text=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")              
                    await message.channel.send(embed=embed)
        
    
# #===========================================================================================================================
# #===========================================================================================================================
# #===========================================================================================================================
    elif str(message.content).lower() == "reset" : 
        for i in range(len(CodeList))  :    
            StatusList[i] = True
            Checker[i] = ""
            Time[i] = ""
        await message.channel.send("RESET COMPLETE")
            

self.run('MTExNjYyNjMxNzI0MTIzNzU2Nw.G73Y9l.5wx6a5e1qUtKMv7br62Zq2vNk1JXC199ej3kag')