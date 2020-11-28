import asyncio
import discord
import random
import re
import pickle
import time

app = discord.Client()

global cooltime
cooltime = 0

def cool():
    cooltime = 1
    time.sleep(0.5)
    cooltime = 0

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    await app.change_presence(activity=discord.Game(name="민쵸 관리봇 중 하나에요!"))

with open('wordlist.txt', 'rb') as f:
    word_list = pickle.load(f)
with open('giftboxboyou.txt', 'rb') as f:
    boyou = pickle.load(f)
with open('giftboxman.txt', 'rb') as f:
    man = pickle.load(f)

@app.event
async def on_message(message):
    if 'cooltime' in locals():
        pass
    else:
        cooltime = 0
    authid = message.author.id
    yes = "no"
    messageContent = message.content
    if messageContent.startswith("욕설리스트 빼줘 ") == True:
        if message.author.guild_permissions.administrator or message.author.id == 770025636148150302:
            yes = "yes"
            topop = messageContent[9:]
            if topop in word_list:
                word_list.remove(topop)
            else:
                await message.channel.send(":no_entry: 리스트 안에 항목이 존재하지 않아요!")
            await message.channel.send(":white_check_mark: 네, 성공적으로 뺐어요!")
            with open('wordlist.txt', 'wb') as f:
                pickle.dump(word_list, f)
        else:
            embed = discord.Embed(title = ":no_entry: 욕설리스트 관리 불가", description = message.author.mention + "님, 권한이 없어요!", colour=0xff0000)
            await message.channel.send(embed=embed)
    if message.author.bot:
        return None
    if len(messageContent) > 0:
        for word in word_list:
            if word in messageContent:
                if yes != "yes":
                    await message.delete()
                    await message.channel.send(message.author.mention+' :no_entry: 욕하지 마세요')
    messageattachments = message.attachments
    if len(messageattachments) > 0:
        for attachment in messageattachments:
            if attachment.filename.endswith(".dll"):
                await message.delete()
                await message.channel.send(message.author.mention+" :no_entry: DLL이나 EXE 파일은 무단 배포를 막기 위해 올릴 수 없어요!")
            elif attachment.filename.endswith('.exe'):
                await message.delete()
                await message.channel.send(message.author.mention+" :no_entry: DLL이나 EXE 파일은 무단 배포를 막기 위해 올릴 수 없어요!")
            else:
                return None
    if messageContent.startswith("욕설리스트 더해 ") == True:
        if message.author.guild_permissions.administrator or message.author.id == 770025636148150302:
            toadd = messageContent[9:]
            word_list.append(toadd)
            await message.channel.send(":white_check_mark: 네, 성공적으로 더했어요!")
            with open('wordlist.txt', 'wb') as f:
                pickle.dump(word_list, f)
        else:
            embed = discord.Embed(title = ":no_entry: 욕설리스트 관리 불가", description = message.author.mention + "님, 권한이 없어요!", colour=0xff0000)
            await message.channel.send(embed=embed)
    if messageContent == "욕설리스트":
        await message.channel.send(word_list)
    if messageContent == "도움" or messageContent == "help":
        embed = discord.Embed(title='도움!',description='`욕설리스트 더해 ...` - `...`를 욕설리스트에 추가합니다.\n`욕설리스트 빼줘 ...` - `...`를 욕설리스트에서 뺍니다.\n`욕설리스트` - 욕설리스트를 보여줍니다. 욕설리스트는 개발자의 컴퓨터에 저장되고 어떤 사람이 욕을 할 때마다 걸러냅니다.\n`뽑기` - 선물상자를 랜덤 개수로 뽑습니다. 데이터는 개발자의 컴퓨터에 저장됩니다.\n`내 상자 수` - 내가 보유하고 있는 상자 수를 측정합니다.\n`상자 ~~~` - 상자 명령입니다. "배워 (명령어) (답변)"으로 배우게 할 수 있습니다. 참고로 명령어에는 띄어쓰기가 들어가면 안되고, 답변에는 띄어쓰기를 넣지 않는 걸 추천합니다.', color = 0xC60000)
        await message.channel.send(embed=embed)
    if messageContent == "뽑기":
        with open('giftboxboyou.txt', 'rb') as f:
            boyou = pickle.load(f)
        with open('giftboxman.txt', 'rb') as f:
            man = pickle.load(f)
        checkid = 0
        lenboyou = len(boyou)
        lenman = len(man)
        checked = 0
        for checkid in range(0, lenman):
            if man[checkid] == authid:
                checked = 1
                break
            else:
                pass
        if checked != 1:
            man.append(authid)
            boyou.append(0)
            checkid = lenman
            with open('giftboxman.txt', 'wb') as f:
                pickle.dump(man, f)
            with open('giftboxboyou.txt', 'wb') as f:
                pickle.dump(boyou, f)
        else:
            pass
        await message.channel.send("뽑기 시작합니다!")
        bobgi = random.randint(0, 20)
        bobgistr = str(bobgi)
        await message.channel.send("당첨 결과는 "+bobgistr+"개입니다! 축하드려요!")
        boyou[checkid] = boyou[checkid]+bobgi
        with open('giftboxboyou.txt', 'wb') as f:
            pickle.dump(boyou, f)
    if messageContent == "내 상자 수":
        with open('giftboxboyou.txt', 'rb') as f:
            boyou = pickle.load(f)
        with open('giftboxman.txt', 'rb') as f:
            man = pickle.load(f)
        checkid = 0
        lenboyou = len(boyou)
        lenman = len(man)
        checked = 0
        for checkid in range(0, lenman):
            if man[checkid] == authid:
                checked = 1
                break
            else:
                pass
        if checked != 1:
            await message.channel.send(":no_entry: "+message.author.mention+"님의 데이터가 존재하지 않아요!")
        elif message.author.id == 674569768811888641 or message.author.id == 770025636148150302:
            await message.channel.send(message.author.mention+"("+str(message.author.id)+", 프리미엄)님의 선물상자 개수는 **"+str(boyou[checkid])+"**개에요!")
        else:
            await message.channel.send(message.author.mention+"("+str(message.author.id)+")님의 선물상자 개수는 **"+str(boyou[checkid])+"**개에요!")
    if messageContent.startswith("상자 ") == True:
        ne = messageContent[3:]
        if messageContent[3:] == "안녕":
            await message.channel.send("안녕하세요! 저는 Gift Box의 뒤를 이을 민쵸 관리봇이에요!")
        elif messageContent[3:] == "고마워":
            await message.channel.send("감사합니다! 앞으로도 이 서버를 이용해주세요!")
        elif messageContent[3:] == "바보":
            await message.channel.send("상자 바보 아니라구요!")
        elif messageContent[3:] == "죽어":
            await message.channel.send("싫은데요??")
        elif messageContent[3:] == "누가 최고니":
            await message.channel.send("당근 아직은 Gift Box님이 최고죠! 하지만 제가 곧 최고가 될거라고요! ><")
        elif messageContent.startswith("상자 배워 ") == True:
            slicedcont = messageContent.split(' ')
            whatask = slicedcont[2]
            whatans = slicedcont[3:]
            with open('minchoask.txt', 'rb') as f:
                minask = pickle.load(f)
            with open('minchoans.txt', 'rb') as f:
                minans = pickle.load(f)
            if ne in minask:
                await message.channel.send(":no_entry: 이미 해당 항목이 존재해요.")
            else:
                minask.append(whatask)
                minans.append(whatans)
                await message.channel.send("완료!")
                with open('minchoans.txt', 'wb') as f:
                    pickle.dump(minans, f)
                with open('minchoask.txt', 'wb') as f:
                    pickle.dump(minask, f)
        else:
            with open('minchoask.txt', 'rb') as f:
                minask = pickle.load(f)
            with open('minchoans.txt', 'rb') as f:
                minans = pickle.load(f)
            if ne in minask:
                ind = minask.index(ne)
                tosend = str(minans[ind])
                tosendd = tosend.lstrip("[")
                tosendd = tosendd.lstrip("'")
                tosendd = tosendd.rstrip("]")
                tosendd = tosendd.rstrip("'")
                await message.channel.send(tosendd)
            else:
                olo = random.randint(0,5)
                if olo == 0:
                    await message.channel.send("`"+ne+"`??")
                elif olo == 1:
                    await message.channel.send("`"+ne+"`가 뭔가요?")
                elif olo == 2:
                    await message.channel.send("`"+ne+"`는 아직 모르겠네요.")
                elif olo == 3:
                    await message.channel.send("`"+ne+"`에 대해 알고 싶네요!")
                elif olo == 4:
                    await message.channel.send("`"+ne+"`라니?!")
                elif olo == 5:
                    await message.channel.send("`"+ne+"`에 대해 설명해주세요!")

app.run('token')
