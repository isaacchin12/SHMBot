from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
  
# Put the token that you received from BotFather in the quotes
bot = Bot(token='5776933995:AAGmUwOCdb1Za2g9QPHtSTR5SbwwpGjsqok')
  
# Initializing the dispatcher object
dp = Dispatcher(bot)

class Location:
    def __init__(self,name,batteries = 0):
        self.name = name
        self.inventory = []
        self.batteries = batteries
    def get_name(self):
        return self.name
    def get_inventory(self):
        return self.inventory
    def print_inventory(self):
        print(self.get_name() + " has the following items:")
        for e in self.inventory:
            print(e.get_name())
    def get_battery(self):
        return self.batteries

    def add_item(self,item): 
        self.inventory.append(item)
    def remove_item(self,item):
        self.inventory.remove(item)
    def change_battery_count(self,n):
        self.batteries += n

location_map = [
    ("SHM Room", 10)
]
SHM_Room = Location("SHM Room",10)

class Equipment:
    def __init__(self, name, type, location = SHM_Room):
        self.name = name
        self.type = type # Camera, Battery, Mic, Tripod
        self.location = location

    def get_name(self):
        return self.name
    def get_type(self):
        return self.type
    def get_location(self):
        return self.location

    def change_location(self, new_loc):
        self.location = new_loc

equipment_map = {
    "A6400": 4,
    'A7 III':1
}
 
A6 = Equipment("A6400", "Camera")
A7 = Equipment("A7", "Camera")

# Creating the reply keyboard
keyboard_reply = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True).add("_button1", "_button2")
  
# Handling the /start and /help commands
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    # Sending a greeting message that includes the reply keyboard
    await message.reply("Hello! how are you?", reply_markup=keyboard_reply)
  
  
# Handling all other messages
@dp.message_handler()
async def check_rp(message: types.Message):
  
    if message.text == '_button1':
        # Responding with a message for the first button
        await message.reply("Hi! this is first reply keyboards button.")
  
    elif message.text == '_button2':
        # Responding with a message for the second button
        await message.reply("Hi! this is second reply keyboards button.")
  
    else:
        # Responding with a message that includes the text of the user's message
        await message.reply(f"Your message is: {message.text}")
  
# Starting the bot
executor.start_polling(dp)