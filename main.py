from twitchio import Client
import numpy as np
import configparser
from chat import *
from send import *
import time



class Bot(Client):

    def __init__(self):
        super().__init__(token='token here', initial_channels=['sardoche'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        chan = self.get_channel('sardoche')
        print(chan)
        await chan.send("salut sard")

    async def event_message(self, message):
        if message.echo:
            return

        global state
        global global_timer
        (state_to_change, concurrent_state) = processNewMessage(message.content, state, advancement)

        state = state_to_change

        print("this is the current state: ")
        print(concurrent_state)

        message_to_send, state, global_timer = send(state, concurrent_state, global_timer, 2, 19, 60, [80,80,35])
        if message_to_send is not None:
            print(message_to_send)
            print(message.channel)
            await message.channel.send(message_to_send)






n=15
advancement = createAdvancement(n)
state = createState(n)
global_timer = time.time()

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
