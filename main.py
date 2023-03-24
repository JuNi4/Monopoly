import monopoly as mon, time, color, random, os, linecache
import itertools
# Todo:
# make rent go up when player owns all street of one color
# make houses buyable
# same for hotels
# finish card display
# add chance and community cards

# get path to current file
PATH = os.path.dirname(os.path.abspath(__file__))

###############
## Functions ##
###############

def randomName():
    # the number of lines with names
    names = 18239
    # get a random number for a line
    line = random.randrange(0,names)
    # read the random line from the file
    name = linecache.getline(PATH+"/data/names.txt", line)
    # return random name
    return name.replace("\n","") # get rid of new line after name

###########################
## color list generation ##
###########################

# generate color list
colors = []
# The possible rgb values
color_list = [0,50,100,150,200,255]

# This will result in every posible combination of the above color values
for subset in itertools.combinations(color_list+color_list+color_list, 3):
    colors.append([subset[0],subset[1],subset[2]])

# check if there are repeats in the list colors
tmp = []
indecies = []
repeats = 0

for i in range(len(colors)):
    if not colors[i] in tmp:
        tmp.append(colors[i])
        indecies.append(i)
    else:
        repeats += 1

# remove all repeats
for i in range(len(indecies)):
    colors.pop(len(indecies)-1-i)

colors = tmp

##########################
## names + playercounts ##
##########################

players = []
AIs = []
player_colors = []

# ask how many humans are playing
print("How many people want to play?")
try:
    num_players = int(input(">"))
except:
    print("Input is not a valid number!")
    exit(1)

# ask for names of players
for i in range(num_players):
    print(f"Please choose a name for player {i+1}:")
    x = input(">")
    players.append(x)
    if len(colors) > 0:
        # generate random color
        x = random.randrange(0,len(colors))
        # add color to player_colors
        player_colors.append(colors[x])
        # remove from colors
        colors.pop(x)

# ask how many ai are playing
print("How many AI want to play?")
try:
    num_ais = int(input(">"))
except:
    print("Input is not a valid number!")
    exit(1)

# add all AIs
for i in range(num_ais):
    AIs.append(randomName()+" (AI)")
    if len(colors) > 0:
        # generate random color
        x = random.randrange(0,len(colors))
        # add color to player_colors
        player_colors.append(colors[x])
        # remove from colors
        colors.pop(x)

# initialise the monopoly object
game = mon.monopoly(players, AIs, player_colors)

# display the state of the game
print("The current state of the game")
game.drawMap()

time.sleep(2)

#####################
## Main Game Logic ##
#####################

index = -1
turn = 1

while True:
    # check if only one player is remaining
    if len(game.players["player_data"]) < 2:
        print(f"Congratulations {game.getPlayer(0).name}, you have won the game!")
        print("Press <ENTER> to exit.")
        input()
        break
    # Increment index
    index += 1
    if index == len(game.players["player_data"]):
        index = 0
        # clear the screen
        os.system("clear")
        # print turn data
        print(color.rgb(0,0,0)+f"Turn: {turn}")
        # draw the map of the current state
        print(color.r+"Updated state of the map:")
        # draw map
        game.drawMap()
        # increment turn counter
        turn += 1
        # wait
        time.sleep(5)

    os.system("clear")
    # print turn data
    print(color.rgb(0,0,0)+f"Turn: {turn} Player:{index+1}/{game.totalPlayers}")
    # get player
    player = game.getPlayer(index)
    # draw the minimap for the player
    game.drawMiniMap([player.position],[player.color])
    # Tell the player whos turn it is
    if player.is_human:
        print(color.r+f"{player.name}, it's your turn. Press <ENTER> roll the dices.")
    else:
        print(color.r+f"{player.name}, it's your turn.")
    # only wait for user input if user is not ai
    if not player.is_ai:
        input()
    else:
        time.sleep(0.5)
    time.sleep(0.25)
    # if the player is not in jail
    if not player.in_prison:
        # roll a dice
        y = game.rollDice()
        # check if player lands in jail
        if y == -1:
            if player.is_human:
                print(color.r+f"{player.name} rolled a double three times in a row. You go to Jail. Press <ENTER> to continue.")
            else:
                print(color.r+f"{player.name} rolled a double three times in a row. You go to Jail.")
            # only wait for user input if user is not ai
            if not player.is_ai:
                input()
            else:
                time.sleep(1)
            # make player go to jail
            player.arrest()
            game.updatePlayer(player)
            continue
        # otherwise move player by y amount and anounce the result
        if player.is_human:
            print(color.r+f"{player.name} rolled {y}. Press <ENTER> to continue.")
        else:
            print(color.r+f"{player.name} rolled {y}.")
        # only wait for user input if user is not ai
        if not player.is_ai:
            input()
        else:
            time.sleep(1)

        # move the player
        x = player.move(y)
        if x == 1:
            print(color.r+f"You went over GO and collected {game.salery}{game.currencySymbol}.")
            player.giveCurrency(game.salery)
            time.sleep(1)
    # if the player is in jail
    else:
        # chech prison time
        player.prison_time -= 1
        # check if the player is done waiting in prison
        if player.prison_time < 1:
            # if so, un arrest player
            player.in_prison = False
            player.prison_time = 0
            # inform the player
            if player.is_ai:
                print(color.r+"Your time in jail is now over. you will be able to make a move next turn!")
                time.sleep(1)
            else:
                print(color.r+"Your time in jail is now over. you will be able to make a move next turn! Press <ENTER> to continue.")
                input()
            game.updatePlayer(player)
            continue
        # if the player has not waited long enough
        # roll 2 dices and see if it is a double
        y = game.dice()
        # if it is a double
        if y[0] == y[1]:
            # a double is rolled
            if player.is_ai:
                print(color.r+"You rolled a double! You get out of jail.")
                time.sleep(1)
            else:
                print(color.r+"You rolled a double! You get out of jail. Press <ENTER> to continue.")
                input()
            player.in_prison = False
            player.prison_time = 0
            player.move(y[0]+y[1])
        else:
            # inform the player how long to wait
            if player.is_ai:
                print(color.r+f"You didnt roll a double. You need to wait {player.prison_time} more turns.")
                time.sleep(1)
            else:
                print(color.r+f"You didnt roll a double. You need to wait {player.prison_time} more turns. Press <ENTER> to continue.")
                input()
            game.updatePlayer(player)
            continue
    # update player
    game.updatePlayer(player)

    # clear the screen
    os.system("clear")

    # print turn data
    print(color.rgb(0,0,0)+f"Turn: {turn} Player:{index+1}/{game.totalPlayers}")
    
    # Draw the updated minimap
    game.drawMiniMap([player.position],[player.color])

    # draw the card if it comes with a deed
    if game.getStreetByID(player.position).type in ["facility","street"]:
        print(color.r + "You landed on:")
        game.drawCards([player.position], 25)
    # otherwise just tell the player the name
    else:
        print(color.r + f"You landed on {game.getStreetByID(player.position).name}.")

    # Evaluate current position of the player
    result = game.evalPosition(player)

    # add bankrupt and end turn options
    result.append({"type":"end_turn"})
    result.append({"type":"declare_bankrupcy"})

    # get street
    street = game.getStreetByID(player.position)

    done = True

    if not result == None:
        if result[0]["type"] == "pay_rent":
            # tell the player that he payed rent to a player
            if player.is_ai:
                print(color.r + result[0]["msg"])
                time.sleep(1)
            else:
                print(color.r + result[0]["msg"]+" Press <ENTER> to continue.")
                input()

            result.pop(0)
        
        if result[0]["type"] == "game_over":
            # tell the player that he payed rent to a player
            if player.is_ai:
                print(color.r + result[0]["msg"])
                time.sleep(1)
            else:
                print(color.r + result[0]["msg"]+" Press <ENTER> to continue.")
                input()

            result.pop(0)
            index -= 1
            continue

    while done:
        os.system("clear")
        # print turn data
        print(color.rgb(0,0,0)+f"Turn: {turn} Player:{index+1}/{game.totalPlayers}")
        
        # Draw the updated minimap
        game.drawMiniMap([player.position],[player.color])

        # draw the card if it comes with a deed
        if game.getStreetByID(player.position).type in ["facility","street"]:
            print(color.r + "You landed on:")
            game.drawCards([player.position], 25)
        # otherwise just tell the player the name
        else:
            print(color.r + f"You landed on {game.getStreetByID(player.position).name}.")
        # print the balance of the player
        print(color.r+f"Balance: {player.currency}{game.currencySymbol}")
        # present the player or ai the options and let them choose
        if result != None:
            for i in range(len(result)):
                if result[i]["type"] == "offer_street":
                    # set color for buy option
                    Color = color.rgb(50,50,50)
                    # check if player is able to afford street
                    if player.currency >= street.cost and game.getStreetOwner(street.id)[0] == None:
                        Color = color.r
                    print(Color+f"({i}) Buy '{street.name}' for {street.cost}{game.currencySymbol}")
                # end turn
                elif result[i]["type"] == "end_turn":
                    print(color.r+f"({i}) End Turn")
                # declare bankrupt
                elif result[i]["type"] == "declare_bankrupcy":
                    print(color.r+f"({i}) Declare Bankrupcy")
        else:
            break

        # ask for input
        if player.is_human:
            x = input(">")
            try:
                x = int(x)
            except:
                print(f"{x} is not a valid number.")
                time.sleep(1)
                continue
        else:
            time.sleep(1)
            x = random.randrange(0,len(result)-1)
            print(">"+str(x))
        
        # check if input is out of range
        if not ( 0 >= x or x < len(result) ):
            print(f"{x} is not a valid input.")
            time.sleep(1)
            continue

        if result[x]["type"] == "end_turn":
            if player.is_ai:
                print("End of your turn.")
                time.sleep(1)
            else:
                print("End of your turn. Press <ENTER> to continue.")
                input()
            break
        elif result[x]["type"] == "declare_bankrupcy":
            # tell the player about what he did
            if player.is_ai:
                print("You declared bankrupcy and are now game over.")
                # wait a moment for him to read
                time.sleep(1)
            else:
                print("You declared bankrupcy and are now game over. Press <ENTER> to continue.")
                input()
            # game over the player
            game.gameOver(player)
            # make sure no errors appear
            index -= 1
            # set done to false so the programm wil jump back to the beginning of the loop
            done = False
            # break out of loop
            break
        elif result[x]["type"] == "offer_street":
            # check if no one already has the street
            if not game.getStreetOwner(street.id)[0] == None:
                if player.is_ai:
                    print("Someone already owns this street.")
                    time.sleep(1)
                else:
                    print("Someone already owns this street. Press <ENTER> to continue")
                    input()
                continue
            # buy street
            game.buyStreet(player,street.id)
            
            if player.is_ai:
                print(f"You bought {street.name} for {street.cost}.")
                time.sleep(1)
            else:
                print(f"You bought {street.name} for {street.cost}. Press <ENTER> to continue.")
                input()
            continue

    # if not done: continue
    if not done:
        continue
    # update the player
    game.updatePlayer(player)



## Demo script ##
exit(0)

# initialise monopoly object
x = mon.monopoly(["J","u","N","i"],[])

# draw map
print("-- Test of drawing map --")

while True:
    x.drawMap()
    for o in x.players["player_data"]:
        #y = x.dice()
        #o["position"] += y[0] + y[1]
        o["position"] += 1
        if o["position"] >= 40: o["position"] = 0
    time.sleep(0.25)