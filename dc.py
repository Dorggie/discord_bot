import discord
from discord.ext import commands
import random
# 建立機器人的客戶端
intents = discord.Intents().all()  # 使用所有特權意圖
#intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 存儲參加抽籤的名單
participants = []
@bot.command()
async def helpme(ctx):
    help_msg = "add:新增一人進抽籤清單(輸入名稱)\n"
    help_msg +="delete:從抽籤名單刪除一人(輸入名稱)\n"
    help_msg +="reset:清空抽籤清單\n"
    help_msg +="add_multi:新增多人進抽籤名單(名稱用, 隔開)\n"
    help_msg +="check:確認抽籤名單\n"
    help_msg +="roll:從抽籤名單抽一人, 並把那人移出抽籤清單"
    await ctx.send(help_msg)

@bot.command()
async def add(ctx, name):
    participants.append(name)
    await ctx.send(f'{name} 已加入抽籤名單！')

@bot.command()
async def delete(ctx, name):
    participants.remove(name)
    await ctx.send(f'{name} 已經移出抽籤名單')

@bot.command()
async def reset(ctx):
    participants.clear()
    await ctx.send('所有人都已經移除抽籤清單')

@bot.command()
async def add_multi(ctx, names):
    for name in names.split(','):
        participants.append(name)
    await ctx.send(f'{names} 已經加入抽籤清單')

@bot.command()
async def check(ctx):
    if participants:
        participant_list = '\n'.join(participants)
        await ctx.send(f'目前抽籤名單有：\n{participant_list}')
    else:
        await ctx.send('抽籤名單中沒有參加者！')

@bot.command()
async def roll(ctx):
    if participants:
        winner = random.choice(participants)
        await ctx.send(f'恭喜 {winner} 中獎了！')
        participants.remove(winner)
        await ctx.send(f'{winner} 已被移出清單')
    else:
        await ctx.send('抽籤名單中沒有參加者！')

'''
@bot.command()
async def show_buttons(ctx):
    embed = discord.Embed(title='按鈕範例', description='請點擊按鈕進行操作')
    button_roll = discord.ui.Button(style=discord.ButtonStyle.primary, label='抽籤', custom_id='roll_button')
    button_add = discord.ui.Button(style=discord.ButtonStyle.primary, label='新增人員', custom_id='add_button')
    button_check = discord.ui.Button(style=discord.ButtonStyle.primary, label='顯示人員', custom_id='check_button')
    view = discord.ui.View()
    view.add_item(button_roll)
    view.add_item(button_add)
    view.add_item(button_check)
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_button_click(interaction):
    if interaction.component.custom_id == 'roll_button':
        if participants:
            winner = random.choice(participants)
            participants.remove(winner)
            await interaction.respond(content=f'恭喜 {winner} 中獎了！')
        else:
            await interaction.respond(content='抽籤名單中沒有參加者！', ephemeral=True)
    elif interaction.component.custom_id == 'add_button':
        await interaction.respond(content='請輸入要新增的人員名稱：', ephemeral=True)
        try:
            add_interaction = await bot.wait_for('message', check=lambda message: message.author == interaction.user, timeout=60)
            name = add_interaction.content
            participants.append(name)
            await interaction.followup(content=f'{name} 已加入抽籤名單！')
        except asyncio.TimeoutError:
            await interaction.followup(content='新增人員逾時，請重新操作。', ephemeral=True)
    elif interaction.component.custom_id == 'check_button':
        if participants:
            participant_list = '\n'.join(participants)
            await interaction.respond(content=f'目前抽籤名單有：\n{participant_list}')
        else:
            await interaction.respond(content='抽籤名單中沒有參加者！', ephemeral=True)

'''

@bot.event
async def on_ready():
    print(f'Bot已成功登入：{bot.user.name} ({bot.user.id})')

# 定義一個指令
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, Discord!')

# 機器人啟動
bot.run('token')# put your bot token here

