from twitchio.ext import commands
import os
from pointsdb import PointsDB
from question import Question
import asyncio


DATABASE = PointsDB()

QUESTIONS = Question()

TOKEN = os.getenv("TRIVIA_TOKEN")

CHANNEL = 'practicex'

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=TOKEN, prefix='?', initial_channels=[CHANNEL])

        self.state = 'wait'
        self.a = ''

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.channel = self.get_channel(CHANNEL)


    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print("RAW: ", message.content)
        print(self.state, self.a, message.content.strip().lower() == self.a and self.state == 'q')


        if message.content.strip().lower() == self.a.strip().lower() and self.state == 'q':
            points = DATABASE.get(message.author.name)
            points += 5
            DATABASE.update(message.author.name, points)
            await self.channel.send(f"{message.author.name} got it: {self.a}. Total points: {points}")
            self.state = 'wait'
            self.loop.create_task(self.question_timeout())
        await self.handle_commands(message)

    @commands.command()
    async def q(self, ctx: commands.Context):
        if self.state == 'wait':
            # Trigger a new question
            q, a = QUESTIONS.get_question()
            print(q,a)
            self.q = q
            self.a = a
            self.state = 'q'
            await self.channel.send(f"{q}")
            self.loop.create_task(self.question_timeout())

    @commands.command()
    async def points(self, ctx: commands.Context):
        points = DATABASE.get(ctx.author.name)
        await self.channel.send(f"{ctx.author.name} has {points} Trivia Points!")  

    async def question_timeout(self):
        q = self.q
        await asyncio.sleep(15)
        if self.state == 'q' and self.q == q:
            await self.channel.send(f"Nobody got it! Answer: {self.a}")  
            self.state = 'wait'

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
