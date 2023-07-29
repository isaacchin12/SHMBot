import telebot

bot = telebot.TeleBot('5776933995:AAGmUwOCdb1Za2g9QPHtSTR5SbwwpGjsqok')



# class Location:
#     def __init__(self,name,inventory = []):
#         self.name = name
#         self.inventory = inventory
#     def get_name(self):
#         return self.name
#     def get_inventory(self):
#         return self.inventory
#     # def print_inventory(self):
#     #     print(self.get_name() + " has the following items:")
#     #     for e in self.inventory:
#     #         print(e.get_name())

#     # def add_item(self,item): 
#     #     self.inventory.append(item)
#     # def remove_item(self,item):
#     #     self.inventory.remove(item)

# SHM_Room = Location("SHM Room")

class Equipment:
    def __init__(self, name, type, location = "SHMRoom"):
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
    
A6_1 = Equipment("A6400.1", "Camera")
A6_2 = Equipment("A6400.2", "Camera")

equipment = [A6_1,A6_2] # LIST OF EQUIPMENT
equipment_names = list(map(lambda x : x.get_name(),equipment))
equip_dict = {}
for eqp in equipment:
    equip_dict[eqp.get_name()] = eqp
    # SHM_Room.add_item(eqp)
#print(equip_dict)

def create_eqp_table():
    text = "\n"
    for e in equipment:
        text += e.get_name() + " - " + e.get_location() + "\n"
    return text

LOCATIONS = ["SHMRoom"]

def all_locations():
    print("Current Users:")
    print(LOCATIONS)

all_locations()

@bot.message_handler(commands=['start', 'hello', 'help'])
def send_welcome(message):
    user = str(message.from_user.username)
    LOCATIONS.append(user)
    print(user + " started using SHM Bot!")
    all_locations()
    bot.reply_to(message, "Hello " + user + ", welcome to the SHM Bot. \
                            \nUse /status to check equipment status. \
                            \nUse /borrow to borrow equipment. \
                            \nUse /return to return equipment.")

@bot.message_handler(commands=['status']) # CHECK LOCATION
def send_status(message):
    bot.reply_to(message, "Equipment location:" + create_eqp_table() + \
        "\nTo borrow equipment, use /borrow. \
         \nTo return equipment, use /return. ")

@bot.message_handler(commands=['borrow']) # BORROW EQUIPMENT
def borrow_equip(message):
    user = str(message.from_user.username)
    text = "What would you like to borrow? \nChoose one: " + create_eqp_table()
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, battery_count, user, "B")

@bot.message_handler(commands=['return']) # RETURN EQUIPMENT
def return_equip(message):
    user = str(message.from_user.username)
    text = "What would you like to return? \nChoose one: " + create_eqp_table()
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, battery_count, user, "R")

def battery_count(message,user,transaction_type):
    camera = message.text
    if camera not in equipment_names:
        text = "Not a valid camera name, please try again."
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        if transaction_type == "B": # BORROW
            text = "How many batteries do you need?"
            sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
            bot.register_next_step_handler(sent_msg, summary_message, camera, user, transaction_type)
        elif transaction_type == "R": # RETURN
            text = "How many batteries are you returning?"
            sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
            bot.register_next_step_handler(sent_msg, summary_message, camera, user, transaction_type)

def summary_message(message,camera,user,transaction_type):
    if transaction_type == "B":
        batteries = message.text
        text = "You have selected " + str(camera) + " and " + str(batteries) + " batteries. \
            \nTo check who has borrowed equipment, use /status."
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        edit_location(message,camera,user) # CHANGE LOCATION TO USER
        #SHM_Room.print_inventory()
    elif transaction_type == "R":
        batteries = message.text
        text = "You are returning " + str(camera) + " and " + str(batteries) + " batteries. \
            \nTo check who has borrowed equipment, use /status."
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        edit_location(message,camera,"SHMRoom") # RETURN TO SHM ROOM    
        #SHM_Room.print_inventory()


def edit_location(message,camera,user): 
    curr_equipment = equip_dict[camera]
    curr_equipment.change_location(user) # change location in equipment
    #print(curr_equipment.get_location() + " returned " + camera + " to " + user + ".")


# ADD BATTERY COUNT TO STATUS
# FOR BORROW AND RETURN, CHANGE TO EQUIPMENT LOCATION FORMAT
# FUNCTION FOR GETTING PROPERLY FORMATTED LIST OF EQUIPMENT 
# BUTTON FOR BORROW AND RETURN OF ITEMS 
# PRINT TO LOG
# TRACKER
# check battery int type and > 0

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Type /start to begin!")

bot.infinity_polling()