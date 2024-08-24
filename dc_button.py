import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = ''

# 抽籤池列表
lottery_pool = []

# 顯示當前抽籤池的內容
async def show_lottery_pool(interaction: discord.Interaction):
    if lottery_pool:
        names = ', '.join(lottery_pool)
        await interaction.followup.send(f"目前的成員有：{names}")
    else:
        await interaction.followup.send("目前是空的！")

# 按鈕類
class LotteryButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='<:anya_this:1090611661968257166> Add', style=discord.ButtonStyle.green)
    async def add_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('請輸入要加入的名字，Ex: 白癡,陳昱元,智障')

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30)
            names = [name.strip() for name in msg.content.split(',')]
            for name in names:
                if name not in lottery_pool:
                    lottery_pool.append(name)
            await interaction.followup.send(f"已加入以下名字：{', '.join(names)}")
            await show_lottery_pool(interaction)  # 顯示當前抽籤池
        except asyncio.TimeoutError:
            await interaction.followup.send("超時未輸入，請再試一次。")
        await interaction.followup.send("RollTheDice 超級大改版：", view=LotteryButtons())

    @discord.ui.button(label='<:anya_shocked:1090611654749868062> Remove', style=discord.ButtonStyle.red)
    async def remove_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('請輸入要移除的名字，Ex: 黑人,方德霖,87')

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30)
            names = [name.strip() for name in msg.content.split(',')]
            not_found = []
            for name in names:
                if name in lottery_pool:
                    lottery_pool.remove(name)
                else:
                    not_found.append(name)
            if not_found:
                await interaction.followup.send(f"以下名字根本不在：{', '.join(not_found)}")
            await interaction.followup.send(f"已移除以下名字：{', '.join([name for name in names if name not in not_found])}")
            await show_lottery_pool(interaction)  # 顯示當前抽籤池
        except asyncio.TimeoutError:
            await interaction.followup.send("超時未輸入，請再試一次。")
        await interaction.followup.send("RollTheDice 超級大改版：", view=LotteryButtons())

    @discord.ui.button(label='<:anya_sly:1090611657539067975> Roll', style=discord.ButtonStyle.blurple)
    async def draw_winner(self, interaction: discord.Interaction, button: discord.ui.Button):
        if lottery_pool:
            winner = random.choice(lottery_pool)
            lottery_pool.remove(winner)  # 抽選後移除該成員
            await interaction.response.send_message(f"🎉 恭喜 {winner} 被選中！")
            await show_lottery_pool(interaction)  # 顯示當前抽籤池
        else:
            await interaction.response.send_message("目前是空的，抽了個寂寞 🚬")
        await interaction.followup.send("RollTheDice 超級大改版：", view=LotteryButtons())

    @discord.ui.button(label='<:anya_cry:1090611620113289286> Add Me', style=discord.ButtonStyle.grey)
    async def add_me(self, interaction: discord.Interaction, button: discord.ui.Button):
        username = str(interaction.user)
        if username not in lottery_pool:
            lottery_pool.append(username)
            await interaction.response.send_message(f"{username} 已加入！")
        else:
            await interaction.response.send_message(f"{username} 已經在裡面了 ==")
        await show_lottery_pool(interaction)  # 顯示當前抽籤池
        await interaction.followup.send("RollTheDice 超級大改版：", view=LotteryButtons())

@bot.event
async def on_ready():
    print(f'{bot.user} 已上線！')

@bot.command(name='start')
async def start_lottery(ctx):
    await ctx.send('RollTheDice 超級大改版：', view=LotteryButtons())

bot.run(TOKEN)