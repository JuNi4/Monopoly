import monopoly as mon, time, color, random, os, linecache
import itertools

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

index = 0
turn = 1

while True:
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
            print(color.r+"You went over GO and collected 200"+game.currencySymbol)
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
                print(color.r+f"You didnt roll a double. You need to wait {player.prison_time} turns.")
                time.sleep(1)
            else:
                print(color.r+f"You didnt roll a double. You need to wait {player.prison_time} turns. Press <ENTER> to continue.")
                input()
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
        if player.is_ai:
            print(color.r + f"You landed on {game.getStreetByID(player.position).name}.")
        else:
            print(color.r + f"You landed on {game.getStreetByID(player.position).name}. Press <ENTER> to continue.")
    # wait if player is ai or wait for enter to be pressed
    if player.is_ai:
        time.sleep(2)
    else:
        input()

    # Evaluate current position of the player
    result = game.evalPosition(player)
    time.sleep(2)

    # present the player or ai the options and let them choose






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