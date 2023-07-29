import telebot

bot = telebot.TeleBot('5776933995:AAGmUwOCdb1Za2g9QPHtSTR5SbwwpGjsqok')

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
    "A6400": 4
}
 
A6 = Equipment("A6400", "Camera")
A7 = Equipment("A7", "Camera")

equipment = [A6,A7] # LIST OF EQUIPMENT
equipment_names = list(map(lambda x : x.get_name(),equipment))
equip_dict = {}
for eqp in equipment:
    equip_dict[eqp.get_name()] = eqp
    SHM_Room.add_item(eqp)
#print(equip_dict)

def create_eqp_table():
    text = ""
    # for e in equipment:
    #     text += e.get_name() + " - " + e.get_location().get_name() + "\n"
    for loc in LOCATIONS.values():
        text += "\n" + loc.get_name() + " - " + str(loc.get_battery()) + " Batteries;"
        for item in loc.get_inventory():
            text += "\n" + item.get_name()
    return text

LOCATIONS = {SHM_Room.get_name():SHM_Room}

def all_locations():
    print("Current Users:")
    users = []
    for u in LOCATIONS:
        users.append(u)
    print(users)

all_locations()

@bot.message_handler(commands=['start', 'hello', 'help'])
def send_welcome(message):
    username = str(message.from_user.username)
    LOCATIONS[username] = Location(username)
    print(LOCATIONS[username].get_name() + " started using SHM Bot!")
    all_locations()
    bot.reply_to(message, "Hello " + LOCATIONS[username].get_name() + ", welcome to the SHM Bot. \
                            \nUse /status to check equipment status. \
                            \nUse /borrow to borrow equipment. \
                            \nUse /return to return equipment.")

@bot.message_handler(commands=['status']) # CHECK LOCATION
def send_status(message):
    bot.reply_to(message, "Equipment locations:" + create_eqp_table() + \
        "\nTo borrow equipment, use /borrow. \
         \nTo return equipment, use /return. ")

@bot.message_handler(commands=['borrow']) # BORROW EQUIPMENT
def borrow_equip(message):
    username = str(message.from_user.username)
    user = LOCATIONS[username]
    text = "What would you like to borrow? \nChoose one: " + create_eqp_table()
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="HTML")
    bot.register_next_step_handler(sent_msg, battery_count, user, "B")

@bot.message_handler(commands=['return']) # RETURN EQUIPMENT
def return_equip(message):
    username = str(message.from_user.username)
    user = LOCATIONS[username]
    text = "What would you like to return? \nChoose one: " + create_eqp_table()
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="HTML")
    bot.register_next_step_handler(sent_msg, battery_count, user, "R")

def battery_count(message,user,transaction_type):
    camera = message.text
    if camera not in equipment_names:
        text = "Not a valid camera name, please try again."
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="HTML")
    else:
        if transaction_type == "B": # BORROW
            text = "How many batteries do you need?"
            sent_msg = bot.send_message(message.chat.id, text, parse_mode="HTML")
            bot.register_next_step_handler(sent_msg, summary_message, camera, user, transaction_type)
        elif transaction_type == "R": # RETURN
            text = "How many batteries are you returning?"
            sent_msg = bot.send_message(message.chat.id, text, parse_mode="HTML")
            bot.register_next_step_handler(sent_msg, summary_message, camera, user, transaction_type)

def summary_message(message,camera,user,transaction_type):
    batteries = message.text
    # if type(batteries) != int:
    #     text = "Please restart and type a number."
    #     bot.reply_to(message.chat.id, text, parse_mode="HTML")        
    if int(batteries) > int(equip_dict[camera].get_location().get_battery()): # Check for enough batteries
        text = "Not enough batteries at that location."
        bot.reply_to(message.chat.id, text, parse_mode="HTML")
    # elif int(batteries) < 1:
    #     text = "u think u funny. Restart"
    #     bot.reply_to(message.chat.id, text, parse_mode="HTML")       
    else:
        if transaction_type == "B":
            text = "You have selected " + str(camera) + " and " + str(batteries) + " batteries. \
                \nTo check who has borrowed equipment, use /status."
            bot.send_message(message.chat.id, text, parse_mode="HTML")
            edit_location(message,camera,batteries,user) # CHANGE LOCATION TO USER
        elif transaction_type == "R":
            text = "You are returning " + str(camera) + " and " + str(batteries) + " batteries. \
                \nTo check who has borrowed equipment, use /status."
            bot.send_message(message.chat.id, text, parse_mode="HTML")
            edit_location(message,camera,batteries,SHM_Room) # RETURN TO SHM ROOM    

def edit_location(message,camera,batteries,user): 
    curr_equipment = equip_dict[camera]
    old_loc = curr_equipment.get_location()
    old_loc.change_battery_count(-int(batteries))

    old_loc.remove_item(curr_equipment)
    curr_equipment.change_location(user) # change location in equipment

    user.add_item(curr_equipment)
    user.change_battery_count(int(batteries))
    print(user.get_name() + " took " + camera + " from " + old_loc.get_name() + ".")
    
    

# FOR BORROW AND RETURN, CHANGE TO EQUIPMENT LOCATION FORMAT -> use equipment maps
# BUTTON FOR BORROW AND RETURN OF ITEMS 
# TRACKER
# check battery int type and > 0

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Type /start to begin!")

bot.infinity_polling()