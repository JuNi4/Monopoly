# Monopolie in python
import os, sys, random, color, json

# get path to current file
PATH = os.path.dirname(os.path.abspath(__file__))

# A street object
class street:
    # constructor for street object
    def __init__(self, index:int, street_json:dict):
        # check if type is in street_json
        if not "type" in street_json:
            print("Required key 'type' not found in street_json!")
            exit(1)
        # a list of required keys
        required = ["name","id","symbol","color","color2","type"]
        # add requirements based on type
        if street_json["type"] == "street":
            required.append("cost")
            required.append("house_cost")
            required.append("hotel_cost")
            required.append("rent")
            required.append("color_id")
        elif street_json["type"] == "facility":
            required.append("cost")
            required.append("rent")
        elif street_json["type"] == "start":
            required.append("salery")
        # check if json object has requiered keys
        for o in required:
            if not o in street_json:
                print(f"Required key '{o}' not found in street_json from index {index}!")
                exit(1)
        # setup variables
        self.index = index
        self.id = street_json["id"]
        self.name = street_json["name"]
        self.symbol = street_json["symbol"]
        self.color = street_json["color"]
        self.color2 = street_json["color2"]
        self.type = street_json["type"]
        # extra variables
        if street_json["type"] == "street":
            self.cost = street_json["cost"]
            self.house_cost = street_json["house_cost"]
            self.hotel_cost = street_json["hotel_cost"]
            self.rent = street_json["rent"]
            self.color_id = street_json["color_id"]
        elif street_json["type"] == "facility":
            self.cost = street_json["cost"]
            self.rent = street_json["rent"]
        elif street_json["type"] == "start":
            self.salery = street_json["salery"]

# a function to get a street by id not by index
def getStreetByID(street_list:list,id:int):
    # get length of list
    length = len(street_list)
    # go through all objects in list
    for i in range(length):
        # check if id of street matches target id
        if street_list[i]["id"] == id:
            # create street object
            streeto = street(i,street_list[i])
            # return street object
            return streeto

# a function to get a street by id not by index
def getStreetByType(street_list:list,type:str):
    # get length of list
    length = len(street_list)
    # go through all objects in list
    for i in range(length):
        # check if id of street matches target id
        if street_list[i]["type"] == type:
            # create street object
            streeto = street(i,street_list[i])
            # return street object
            return streeto

# A player object
class player():
    # constructor for player object
    def __init__(self, id:int, field_count:int, jail_position:int, name:str = "", color:list[int] = [0,0,0], position:int = 0, currency:float = 0, streets:list[street] = [], in_prison:bool = False, prison_time:int = 0, type:str = "human", ai_parameters:dict = {}, player_json = {}):
        if player_json == {}:
            # set internal variables
            self.id = id
            self.name = name
            self.color = color
            self.position = position
            self.currency = currency
            self.streets = streets
            self.type = type
            self.ai_parameters = ai_parameters
            self.in_prison = in_prison
            self.prison_time = prison_time
            # More information
            if type == "human":
                self.is_ai = False
                self.is_human = True
            else:
                self.is_ai = True
                self.is_human = False
        else:
            # check if json object has requiered keys
            required = ["name","color","position","currency","streets_owned","type","in_prison","prison_time"]
            for o in required:
                if not o in player_json:
                    print(f"Required key '{o}' not found in player_json with id {id}!")
                    exit(1)
            # load player object from json
            self.id = id
            self.name = player_json["name"]
            self.color = player_json["color"]
            self.position = player_json["position"]
            self.currency = player_json["currency"]
            self.streets = player_json["streets_owned"]
            self.type = player_json["type"]
            self.in_prison = player_json["in_prison"]
            self.prison_time = player_json["prison_time"]
            # More information
            if player_json["type"] == "human":
                self.is_ai = False
                self.is_human = True
                self.ai_parameters = {}
            else:
                self.is_ai = True
                self.is_human = False
                self.ai_parameters = player_json["ai"]

        # General values
        self.field_count = field_count
        self.jail_position = jail_position

    # give the player currency
    def giveCurrency(self,amount:float):
        self.currency += amount

    def chargeCurrency(self,a:float):
        # remove amount from currency
        self.currency -= a

    # move the player x amount
    def move(self, steps:int):
        code = 0
        # add steps to position
        self.position += steps
        # check if position is out of bounds
        if self.position < 0: self.position = 0
        if self.position >= self.field_count:
            self.position = 0
            # indicate that player went over start
            code = 1

        return code
    
    # move the player to jail
    def arrest(self, t:int=5):
        # set in_prison to true
        self.in_prison = True
        # set the position to the jail position
        self.position = self.jail_position
        # set time the player spends in jail
        self.prison_time = t

    def buyStreet(self, id:int, street_list:list):
        # get data of the street
        street = getStreetByID(street_list,id)
        # if street is not buyable, tell the player
        if not street.type in ["facility","street"]:
            print("Field is not buyable.")
            return
        # check if player is able to afford street
        if self.currency < street.cost:
            print(f"Player can't afford {street.name}!")
            return
        # the json dict of the date for the street attached to the user
        userAddedStreetData = {
            "id": street.id,
            "houses": 0,
            "hotels": 0,
            "current_rent": street.rent[0]
        }
        # add data to player
        self.streets.append(userAddedStreetData)
        # remove player money
        self.currency -= street.cost

    def buyHotel(self,id:int, hotel_limit:int=1,house_requirement:int=4,rm_houses:bool=True):
        # check if player owns street
        index = -1
        for i in range(len(self.streets)):
            if self.streets[i].id == id:
                index = i
        # check if plyer owns street
        if index == -1:
            print(f"You do not own the {street.type} {street.name}.")
            return
        # check if player has enough houses to upgrade hotel
        if not self.street[index]["houses"] >= house_requirement:
            print("You do not have enough houses to upgrade to a hotel.")
            return
        # check if player has enough money
        if street.hotel_cost > self.currency:
            print(f"Can not afford hotel for {street.name}")
        # check if player already has to many hotels
        if self.streets[index]["hotels"] >= hotel_limit:
            print(f"Can not buy more hotels than {hotel_limit}.")
            return
        # buy hotel
        self.streets[index]["hotels"] += 1
        # remove money from player
        self.currency -= street.hotel_cost
        if rm_houses:
            self.streets[index]["houses"] -= house_requirement

    def buyHouse(self,id:int, house_limit:int=1,hotel_limit=1):
        # check if player owns street
        index = -1
        for i in range(len(self.streets)):
            if self.streets[i].id == id:
                index = i
        # check if plyer owns street
        if index == -1:
            print(f"You do not own the {street.type} {street.name}.")
            return
        # check if player has enough money
        if street.hotel_cost > self.currency:
            print(f"Can not afford house for {street.name}")
        # check if player already has to many hotels
        if self.streets[index]["houses"] >= hotel_limit:
            print(f"Can not buy more houses than {house_limit}.")
            return
        # buy hotel
        self.streets[index]["houses"] += 1
        # remove money from player
        self.currency -= street.hotel_cost
        
    # convert the player object to a json object
    def dump(self):
        playerData = {
            "name": self.name,
            "color": self.color,
            "position": self.position,
            "currency": self.currency,
            "streets_owned": self.streets,
            "in_prison": self.in_prison,
            "prison_time": self.prison_time,
            "type": self.type
        }

        # add ai parameters if ai
        if self.type == "ai":
            playerData["ai"] = self.ai_parameters

        return playerData
    

################
## Main Class ##
################
class monopoly():

    # a function to get a street by id not by index
    def getStreetByID(self,id:int):
        street_list = self.streets["streets"]
        # get length of list
        length = len(street_list)
        # go through all objects in list
        for i in range(length):
            # check if id of street matches target id
            if street_list[i]["id"] == id:
                # create street object
                streeto = street(i,street_list[i])
                # return street object
                return streeto

    # a function to get a street by id not by index
    def getStreetByType(self,type:str):
        street_list = self.streets["streets"]
        # get length of list
        length = len(street_list)
        # go through all objects in list
        for i in range(length):
            # check if id of street matches target id
            if street_list[i]["type"] == type:
                # create street object
                streeto = street(i,street_list[i])
                # return street object
                return streeto

    # Init function for the monopoly object
    def __init__(self, name_list:list, ai_list:list, colors:list = [], dataName:str = "test"):
        # check if name list has at least 1 person in it
        if len(name_list)+len(ai_list) < 1:
            print("There must be at least two people (players + ai) playing!")
            exit(0)
        # set data file suffix
        self.dataFile = dataName
        # load streets data
        if not os.path.isfile(PATH+f'/data/data_{self.dataFile}.json'):
            print(f'Data file \'streets_{self.dataFile}.json\' not found!')
            exit(1)

        f = open(PATH+f'/data/data_{self.dataFile}.json')
        # load data file
        self.streets = json.load(f)
        f.close()

        ## Setup vars
        self.playerCount = len(name_list)
        self.aiCount = len(ai_list)
        self.totalPlayers = len(name_list) + len(ai_list)

        self.streetCount = len(self.streets["streets"])

        # the symbol of the currency
        self.currencySymbol = self.streets["currency_symbol"]

        # get position of the jail, goto_jail and free_parking
        # jail
        self.jail_position = self.getStreetByType("jail").id
        # goto_jail
        self.goto_jail_position = self.getStreetByType("goto_jail").id
        # free_parking
        self.free_parking_position = self.getStreetByType("free_parking").id

        # get the amount of currency you get when going over start
        self.salery = self.getStreetByType("start").salery

        # index all the street color ids
        self.color_index = []

        for i in range(0,40):
            count = 0
            data = {"id": i}
            # go over all streets and get theire id
            for o in self.streets["streets"]:
                if o["type"] == "street":
                    if o["color_id"] == i:
                        count += 1
            # add count to data
            data["count"] = count
            # add data to index
            self.color_index.append(data)

        # Initialise player object
        self.players = {
            "player_count": len(name_list),
            "player_data": [],
            "lost_players": []
        }

        # create users
        for o in name_list:
            demoPlayerData = {
                "name": "",
                "color": [0,0,0],
                "position": 0,
                "currency": 1500,
                "streets_owned": [],
                "in_prison": False,
                "prison_time": 0,
                "type": "human",
            }
            # set color
            if len(colors) > 0:
                demoPlayerData["color"] = colors[0]
                colors.pop(0)
            # set name
            demoPlayerData["name"] = o
            # add data to list
            self.players["player_data"].append(demoPlayerData)

        # create AIs
        for o in ai_list:
            demoAIData = {
                "name": "",
                "color": [0,0,0],
                "position": 0,
                "currency": 1500,
                "streets_owned": [],
                "in_prison": False,
                "prison_time": 0,
                "type": "ai",
                "ai": {}
            }
            demoAIData["name"] = o
            # Give the 'ai' paramaters
            # how much money the ai will spend at the start
            demoAIData["ai"]["initial_threshold"] = random.randint(500,1250)
            # random percentage of a street being bought when 2 people already claimed a street
            demoAIData["ai"]["secure_street_percentage"] = random.randint(1,33)
            # auction money
            demoAIData["ai"]["initial_threshold"] = random.randint(300,750)
            # add color
            if len(colors) > 0:
                demoAIData["color"] = colors[0]
                colors.pop(0)
            # add ai data to player list
            self.players["player_data"].append(demoAIData)
        
    # A function for drawing the monopoly map with players
    def drawMap(self):
        # Draw a monopolie map
        map = ''
        first = ''
        second = ''
        c = 0
        line = 0
        for o in self.streets["streets"]:
            # get information of tile
            #symbol
            symbol = o["symbol"].replace(' ','█')
            #color
            streetColorList = o["color"]
            fColor = color.lrgb(streetColorList)
            bColor = color.lbrgb(streetColorList)
            Color = fColor + bColor

            Color2 = color.lrgb(o["color2"]) + color.lbrgb(o["color2"])

            id = o["id"]
            players = []

            name1 = "█"
            name2 = "█"
            name3 = "█"
            name4 = "█"

            # get the amounts of players on the field
            for o2 in self.players["player_data"]:
                if o2["position"] == id:
                    players.append(o2["name"][:1])

            if len(players) == 1:
                name1 = players[0]
            elif len(players) == 2:
                name1 = players[0]
                name2 = players[1]
            elif len(players) == 3:
                name1 = players[0]
                name2 = players[1]
                name3 = players[2]
            elif len(players) == 4:
                name1 = players[0]
                name2 = players[1]
                name3 = players[2]
                name4 = players[3]
            elif len(players) > 4:
                name1 = "4"
                name2 = "+"

            # assemble
            if line == 0:
                # if the current line is the first line, add the "blank" space for the players first and then the colored bit
                first += Color2 + name1+name2+name3+name4 + color.r
                second += Color + symbol*4 + color.r
            elif line == 10:
                # if the line is the last line, do the opposite of the first line
                first += Color + symbol*4 + color.r
                second += Color2 + name1+name2+name3+name4 + color.r
                # otherwise if the position is the first position, just add the thing
            elif c == 0:
                first += Color2 + name1+name2 + Color + symbol*2 + color.r
                second += Color2 + name3+name4 + Color + symbol*2 + color.r
            elif c == 1:
                first += color.rgb(0,0,0) + "|  "+"    "*8 + "|" + Color + symbol*2 + Color2 + name1+name2 + color.r
                second += color.rgb(0,0,0) + "|  "+"    "*8 + "|" + Color + symbol*2 + Color2 + name3+name4 + color.r
                
            # at the end of a line, add line to map
            if ((line == 0 or line == 10) and c == 10) or ((0 < line and line < 10) and c == 1):
                map += color.rgb(0,0,0) + "|" + first + color.rgb(0,0,0) + '|\n'
                map += color.rgb(0,0,0) + "|" + second + color.rgb(0,0,0) + '|\n'
                first = ''
                second = ''
                c = -1
                line += 1

            c+=1

        print(map)

        # A function for drawing a tiny monopoly map
    def drawMiniMap(self, highlights:list = [], highlight_colors:list = []):
        # Draw a monopolie map
        map = ''
        first = ''
        c = 0
        line = 0
        for o in self.streets["streets"]:
            # get information of tile
            symbol = "▀"
            symbol2 = "█"
            #color
            streetColorList = o["color"]
            fColor = color.lrgb(streetColorList)
            bColor = color.lbrgb(streetColorList)
            Color = fColor + bColor

            fColor2 = color.lrgb(o["color2"])
            bColor2 = color.lbrgb(o["color2"])

            color1 = o["color2"]
            color2 = o["color2"]

            # Get the highlight color
            id = o["id"]
            highlights_field = []
            # go through all highlights
            for i in range(len(highlights)):
                # if the highlight is for this field, add its index to the highlights_field var
                if highlights[i] == id:
                    highlights_field.append(i)

            # if only one highlight is on the field, set both available spots to the color
            if len(highlights_field) == 1:
                color1 = highlight_colors[highlights_field[0]]
                color2 = color1
            if len(highlights_field) > 1:
                color1 = highlight_colors[highlights_field[0]]
                color2 = highlight_colors[highlights_field[1]]

            fcolor1 = color.lrgb(color1)
            fcolor2 = color.lrgb(color2)

            bcolor1 = color.lbrgb(color1)
            bcolor2 = color.lbrgb(color2)

            # assemble
            if line == 0:
                # if the current line is the first line, add the "blank" space for the players first and then the colored bit
                first += bColor + fcolor1 + symbol + fcolor2 + symbol + color.r
            elif line == 10:
                # if the line is the last line, do the opposite of the first line
                first += fColor + bcolor1 + symbol + bcolor2 + symbol + color.r
                # otherwise if the position is the first position, just add the thing
            elif c == 0:
                first += fcolor1 + bcolor2 + symbol + Color + symbol + color.r
            elif c == 1:
                first += color.rgb(0,0,0) + "|"+"  "*8 + "|" + Color + symbol + fcolor1 + bcolor2 + symbol + color.r
                
            # at the end of a line, add line to map
            if ((line == 0 or line == 10) and c == 10) or ((0 < line and line < 10) and c == 1):
                map += color.rgb(0,0,0) + "|" + first + color.rgb(0,0,0) + '|\n'
                first = ''
                c = -1
                line += 1

            c+=1

        print(map)

    # function for drawing a list of cards
    def drawCards(self,cards:list, width_of_card:int = 10):
        # set up vars
        
        border = 1
        mid = width_of_card - border*2
        
        rows = []
        for i in range(10):
            rows.append("")
        symbol = "▀"
        symbol2 = "█"
        deco = color.r + color.rgb(0,0,0) + "|"
        # go through all cards
        for i in cards:
            streeto = self.getStreetByID(i)
            if streeto.type != "street" and streeto.type != "facility":
                continue
            #streeto = street(i,self.streets["streets"][i])
            #color
            streetColorList = streeto.color
            fColor = color.lrgb(streetColorList)
            bColor = color.lbrgb(streetColorList)
            Color = fColor + bColor

            fColor2 = color.lrgb(streeto.color2)
            bColor2 = color.lbrgb(streeto.color2)
            Color2 = fColor2+bColor2
            # name length
            lname = len(streeto.name)
            fill = mid-lname
            fillstr = symbol2*fill
            # first row
            rows[0] += " " + deco + Color2 + symbol*border + bColor + symbol*mid + Color2 + symbol*border + deco
            #color row
            #rows[1] += " " + deco + Color2 + symbol*border + fColor + symbol*mid + Color2 + symbol*border + deco
            rows[1] += " " + deco + Color2 + symbol*border + color.r + bColor + streeto.name + fColor + fillstr + Color2 + symbol*border + deco
            # blank row
            rows[2] += " " + deco + Color2 + symbol2*width_of_card + deco
            # Rent: 100
            text = "Rent"
            rent = str(streeto.rent[0])
            length = mid-len(text + rent)
            rows[3] += " " + deco + Color2 + symbol2*border + color.r + bColor2 + text + Color2 + symbol2*length + rent + Color2 + symbol2*border + deco


        # print all rows
        for o in rows:
            print(o)


    # roll 2 d6 dices
    def dice(self):
        # generate first random number for the dice
        x = random.randint(1,6)
        # generate second random number for the dice
        y = random.randint(1,6)
        # return result
        return [x,y]
    
    # Whole dice logic
    # Two D6 Dices get thrown
    # if a double is rolled, the dices will be rolled again.
    # if a double is rolled again, same thing.
    # if a double is rolled for the third time, a -1 is returned to indicate that the player may now go to jail
    def rollDice(self):
        return -1
        moves = 0
        # roll two d6 dices
        result = self.dice()
        # added the result to the amount of moves
        moves += result[0]+result[1]

        # if a double is rolled
        if result[0] == result[1]:
            # roll two d6 dices again
            result = self.dice()
            # added the result to the amount of moves
            moves += result[0]+result[1]
            # if a double is rolled again
            if result[0] == result[1]:
                # roll two d6 dices again
                result = self.dice()
                # added the result to the amount of moves
                moves += result[0]+result[1]
                # if a double is rolled 3 times over
                if result[0] == result[1]:
                    # return -1 for go to prison
                    return -1
                # otherwise, return number of moves
                else:
                    return moves
            # otherwise, return number of moves
            else:
                return moves
        # otherwise, return number of moves
        else:
            return moves
        
    def getPlayer(self, id:int):
        # Get the player object
        if id >= len(self.players["player_data"]) or id < 0:
            print("Id not found!")
            return

        # store information of the target player in a variable
        playerd = self.players["player_data"][id]

        # create the player object
        p = player(id,self.streetCount,self.jail_position,player_json=playerd)

        # return the player object
        return p
    
    def updatePlayer(self, p:player):
        self.players["player_data"][p.id] = p.dump()

    # Get the owner of a street, returns player or none if the street has no owner
    def getStreetOwner(self, id):
        # go through all players and find one who owns the street
        for i in range(len(self.players["player_data"])):
            for i2 in range(len(self.players["player_data"][i]["streets_owned"])):
                if self.players["player_data"][i]["streets_owned"][i2]["id"] == id:
                    return self.getPlayer(i), i2
        return None, -1

    # takes player a's money and gives it to player b
    def pay(self,pa:player, pb:player, a:float):
        # add currency to another player
        pa.currency -= a
        pb.giveCurrency(a)
        # update players
        self.updatePlayer(pa)
        self.updatePlayer(pb)
        # return player a
        return pa
    
    # checks if a player has all streets of a color
    def hasPlayerAllOfColor(self,p:player,id:int):
        pass

    ##
    # converts a string to instruction
    # example 1: "goto_jail"
    # example 2: "goto_1|no_salery"
    # example 3: "!keep|un_arrest|move_1"
    # list of all attributes
    # !keep - whether or not the card is givin to the player until it is used
    # !uses_x - makes the card reusable x amount of times
    # list of all action
    # arrest - arrests the player
    # un_arrest - frees the player
    # move_x - move the player x amount
    # goto_x - directly moves the player to a card with a specific index
    # no_salery - disables the salery if the player goes over GO
    # salery_times_x - a multiplier for the salery if the player goes over GO
    ##
    def __compile_action(self, a:str, p:list[int] = [-1,-1],file_name:str = ""):
        # split the string of actions to a list
        a = a.split("|")

        # the variable that will be returned
        out = {}

        # a list of all valid actions
        valid_action_list = ["!keep","!uses","arrest","un_arrest","move","goto","no_salery","salery_times"]

        # the length to calculate the column
        length = p[1]

        if not p[0] == -1:
            error_line = "E: <{a} {b}:{c}> "
        else:
            error_line = "E: "

        # go through all actions
        for o in a:
            index = -1
            # check if action is valid
            for vo in valid_action_list:
                if vo in o:
                    index = valid_action_list.index(vo)
            # if action not found, return
            if index == -1:
                print(error_line.format(a = file_name, b = p[0], c = length)+f"action '{o}' not found!")
                return {"error":error_line.format(a = file_name, b = p[0], c = length)+f"action '{o}' not found!"}

            # Values for the actions
            jail = self.jail_position
            
            # Next, convert to dict
            key = valid_action_list[index]

            if key == "!keep" or key == "arrest" or key == "un_arrest" or key == "no_salery":
                value = str(True)
            else:
                value = o[len(valid_action_list[index]+"_"):]

            # evaluate value to add things
            try:
                out[ key ] = eval(value)
            except Exception as e:
                print(error_line.format(a = file_name, b = p[0], c = length) + value + " " +str(e))

            # increment lenght to calculate column
            length += len( o + "|" )

        # return out var
        return out

    ##
    # executes actions from a dictionary
    # example 1: {"goto": 11}
    # example 2: {"goto": 1, "salery": 0}
    # example 3: {"keep": true, "un_arrest": true, "move": 1}
    # list of all attributes
    # !keep - whether or not the card is givin to the player until it is used
    # !uses_x - makes the card reusable x amount of times
    # list of all action
    # arrest - arrests the player
    # un_arrest - frees the player
    # move_x - move the player x amount
    # goto_x - directly moves the player to a card with a specific index
    # no_salery - disables the salery if the player goes over GO
    # salery_times_x - a multiplier for the salery if the player goes over GO
    ##
    def __execute_action(self, a:dict, p:player):
        pass


    # evaluate a position
    def evalPosition(self,p:player):
        # get street
        streeto = self.getStreetByID(p.position)
        # get street owner
        streetOwner, index = self.getStreetOwner(streeto.id)
        # check if field is street
        if streeto.type in ["street","facility"]:
            # check if it is owned by another player
            if streetOwner != None and streetOwner.id != p.id:
                # pay player rent
                self.pay(p, streetOwner, streetOwner.streets[index]["current_rent"])
                return [{"type":"pay_rent","amount":streetOwner.streets[index]["current_rent"],"msg":f"Payed {streetOwner.streets[index]['current_rent']} in rent to {streetOwner.name}"}]
            # check if no one owns the street
            if streetOwner == None:
                return [{"type":"offer_street","id":streeto.id}]
            # check if player owns street
            if streetOwner.id == p.id:
                pass
        else:
            return []
        self.updatePlayer(p)
        # compile the action
        #x = self.__compile_action("move_8|goto_jail|no_salery",[0,0], "demo")
        # execute the compiled action
        #self.__execute_action(x,p)

    def gameOver(self,p:player):
        # add player to lost player list
        self.players["lost_players"].append(self.players["player_data"][p.id])

        # recount total players
        if p.is_human:
            self.playerCount -= 1
        else:
            self.aiCount -= 1
        self.totalPlayers = self.playerCount + self.aiCount
        # remove player from active list
        self.players["player_data"].pop(p.id)