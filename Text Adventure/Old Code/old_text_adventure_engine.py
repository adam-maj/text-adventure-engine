#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Variables & Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
recognizedCommand = 0
selectedPlayer = "gonzo"

parseCommand = []

locations = {}
objectLocations = {}
objectNames = {}
interactions = {}
transactions = {}
players = {}
creatureLocations = {}
creatureNames = {}

#To Do
"""
Typewriter with text wrapping
Internal debugging system for everything like in _scenario.reveal()
All _scenario parameters for delete/reveal should be in one also option to delete scenario
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#add typewriter effect and TEXT WRAPPING
def typewrite(text):
    print(text)

def parse(text, split, parseList):
    del parseList[:]
    letter = 0
    word = ""
    while(letter < len(text)):
        if text[letter] == split:
            parseList.append(word)
            word = ""
        else:
            word += text[letter]
        letter += 1
    parseList.append(word)

def getName():
    name = ""
    item = 0
    while(item < len(parseCommand)):
        name += parseCommand[item]
        item += 1
    return name

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Player~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class _user:
    def __init__(self, name, health, money, x, y, z, hidden, inventory):
        self.name = name
        self.health = health
        self.money = money
        self.x = x
        self.y = y
        self.z = z
        self.location = str(self.x) + str(self.y) + str(self.z)
        self.hidden = hidden
        self.inventory = inventory
        if self.hidden == 0:
            players[self.name] = self
    def reveal(self):
        players[self.name] = self
    def move(self, direction, x, y, z, exitIndex):
        if direction in parseCommand and locations[self.location].exits[exitIndex] == 1:
            self.x += x
            self.y += y
            self.z += z
            self.location = str(self.x) + str(self.y) + str(self.z)
            locations[self.location].describe()
            global recognizedCommand
            recognizedCommand = 2
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Locations~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class _location:
    def __init__(self, x, y, z, name, description, exits, hidden):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = str(self.x) + str(self.y) + str(self.z)
        self.name = name
        self.description = description
        self.exits = exits
        self.hidden = hidden #hidden can = 1, 0, or a list that tells which of the adjacent locations have an exit back into this one [north, south, east, west, up, down]
        self.visited = 0
        if self.hidden == 0 or not self.hidden:
            locations[self.xyz] = self
    def checkExit(self, deltaX, deltaY, deltaZ, exitIndex, hiddenIndex):
        newX = self.x + deltaX
        newY = self.y + deltaY
        newZ = self.z + deltaZ
        newLocation = str(newX) + str(newY) + str(newZ)
        if newLocation in locations.keys():
            if self.hidden == 1:
                locations[newLocation].exits[exitIndex] = 1
                self.hidden = 0
            elif not isinstance(self.hidden, int):
                locations[newLocation].exits[exitIndex] = self.hidden[hiddenIndex]
                self.hidden = 0
            elif self.hidden == 0:
                locations[newLocation].exits[exitIndex] = 0
                self.hidden = 1
    def reveal(self):
        locations[self.xyz] = self
        self.checkExit(0, 0, 1, 5, 4)
        self.checkExit(0, 0, -1, 4, 5)
        self.checkExit(1, 0, 0, 3, 2)
        self.checkExit(-1, 0, 0, 2, 3)
        self.checkExit(0, 1, 0, 1, 0)
        self.checkExit(0, -1, 0, 0, 1)
    def delete(self):
        locations.pop(self.xyz)
        self.checkExit(0, 0, 1, 5, 4)
        self.checkExit(0, 0, -1, 4, 5)
        self.checkExit(1, 0, 0, 3, 2)
        self.checkExit(-1, 0, 0, 2, 3)
        self.checkExit(0, 1, 0, 1, 0)
        self.checkExit(0, -1, 0, 0, 1)        
    def describe(self):
        self.visited = 1
        typewrite("You are at " + self.name)
        typewrite(self.description)
        if self.xyz in objectLocations.keys():
            index = 0
            roomObjects = ""
            while index < len(objectLocations[self.xyz]) - 1:
                roomObjects += ", " + objectLocations[self.xyz][index].roomLocation
                index += 1
            if index > 0:
                roomObjects += ", and " + objectLocations[self.xyz][index].roomLocation
                roomObjects = "There is" + roomObjects[1:]
            else:
                roomObjects = objectLocations[self.xyz][index].roomLocation
                roomObjects = "There is " + roomObjects
            typewrite(roomObjects)
        if self.xyz in creatureLocations.keys():
            index = 0
            creatureObjects = ""
            while index < len(creatureLocations[self.xyz]) - 1:
                creatureObjects += ", " + creatureLocations[self.xyz][index].roomLocation
                index += 1
            if index > 0:
                creatureObjects += ", and " + creatureLocations[self.xyz][index].roomLocation
                creatureObjects = "There is" + roomObjects[1:]
            else:
                creatureObjects = creatureLocations[self.xyz][index].roomLocation
                creatureObjects = "There is " + creatureObjects
            typewrite(creatureObjects)
        index = 0
        directions = ""
        directionKey = ["NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"]
        while index < len(directionKey):
            if self.exits[index] == 1:
                directions += ", " + directionKey[index]
            index += 1
        directions = "You can go:" + directions[1:]
        typewrite(directions)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Objects~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class _object:
    def __init__(self, x, y, z, takeable, hidden, name, roomLocation, description):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = str(self.x) + str(self.y) + str(self.z)
        self.takeable = takeable
        self.hidden = hidden
        self.name = name
        self.roomLocation = roomLocation
        self.description = description
        if self.hidden == 0:
            if self.xyz in objectLocations.keys():
                objectLocations[self.xyz].append(self)
            else:
                objectLocations[self.xyz] = [self]
            objectNames[self.name] = self
    def reveal(self):
        if self.xyz in objectLocations.keys():
            objectLocations[self.xyz].append(self)
        else:
            objectLocations[self.xyz] = [self]
        objectNames[self.name] = self
    def delete(self):
        if self.xyz in objectLocations.keys() and self in objectLocations[self.xyz]:
            objectLocations[self.xyz].remove(self)
            if not objectLocations[self.xyz]:
                objectLocations.pop(self.xyz)        
        elif self.name in players[selectedPlayer].inventory:
            players[selectedPlayer].inventory.remove(self.name)
        else:
            typewrite("ERROR: Object " + self.name + " Deletion Failed. \'deleteObjects\' parameter in _scenario object likely misspelled.")
        objectNames.pop(self.name)
    def describe(self):
        if players[selectedPlayer].location in objectLocations.keys() and self in objectLocations[players[selectedPlayer].location] or self.name in players[selectedPlayer].inventory:
            typewrite(self.description)
        else:
            typewrite("There is no such object here.")
    def take(self):
        if self.name not in players[selectedPlayer].inventory:
            if players[selectedPlayer].location in objectLocations.keys() and self in objectLocations[players[selectedPlayer].location]:
                if self.takeable == 0:
                    self.delete()
                    objectNames[self.name] = self
                    players[selectedPlayer].inventory.append(self.name)
                    typewrite(self.name.upper() + " has been added to your inventory.")
                elif self.takeable == -1:
                    typewrite("You can't take that.")
                elif self.takeable > 0:
                    typewrite("You can't take that, it costs money.")
            else:
                typewrite("There is no such object here.")
        else:
            typewrite("You already took that. It's in your inventory.")
    def buy(self):
        if self.xyz == players[selectedPlayer].location:
            if self.takeable > 0:
                if players[selectedPlayer].money >= self.takeable:
                    self.delete()
                    objectNames[self.name] = self
                    players[selectedPlayer].inventory.append(self.name)
                    players[selectedPlayer].money -= self.takeable
                    typewrite("You spent " + str(self.takeable) + " and purchased a " + self.name)
                else:
                    typewrite("You can't afford that. It costs " + str(self.takeable) + ". You only have " + str(players[selectedPlayer].money))
            else:
                typewrite("That doesn't have a price.")
        else:
            typewrite("There is no such object here.")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Scenario~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class _interaction:
    def __init__(self, usedObject, scenarioLocation, hidden, message, **kwargs):
        self.usedObject = usedObject
        self.scenarioLocation = scenarioLocation
        self.hidden = hidden
        self.message = message
        self.kwargs = kwargs
        if self.hidden == 0:
            if self.usedObject.name in interactions.keys():
                interactions[self.usedObject.name].append(self)
            else:
                interactions[self.usedObject.name] = [self]
    def reveal(self):
        if self.usedObject.name in interactions.keys() and self in interactions[self.usedObject.name]:
            typewrite("ERROR: Scenario already revealed")#apply to all
        elif self.usedObject.name in interactions.keys():
            interactions[self.usedObject.name].append(self)
        else:
            interactions[self.usedObject.name] = [self]
    def delete(self):
        interactions[self.usedObject.name].remove(self)
        if not interactions[self.usedObject.name]:
            interactions.pop(self.usedObject.name)
    def activate(self):
        global recognizedCommand
        if self.usedObject.name in players[selectedPlayer].inventory:
            if players[selectedPlayer].location == self.scenarioLocation:
                recognizedCommand = 2
                for key, value in self.kwargs.items():
                    if key == "reveal":
                        for i in value:
                            i.reveal()
                    if key == "delete":
                        for i in value:
                            i.delete()
                    if key == "open":
                        for i in value:
                            i.description += " It is open."
                    if key == "money":
                        players[selectedPlayer].money += value
                    if key == "newmsg": #dictionary format with {creature:"new message"}
                        for i in value.keys():
                            i.newMessage(value[i])#add debug thingy here for why this wouldnt work IE if the creature doesnt even have "message" in its kwargs
                typewrite(self.message)
                if "money" in self.kwargs.keys():
                    typewrite("You earned " + str(self.kwargs["money"]))
        else:
            typewrite("There is no such object in your inventory.")
            recognizedCommand = 2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Creature~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class _creature:
    def __init__(self, x, y, z, hidden, name, roomLocation, description, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = str(self.x) + str(self.y) + str(self.z)
        self.name = name
        self.description = description
        self.hidden = hidden
        self.roomLocation = roomLocation
        self.kwargs = kwargs
        #self.movement = movement
        #self.interaction = interaction
        if self.hidden == 0:
            if self.xyz in creatureLocations.keys():
                creatureLocations[self.xyz].append(self)
            else:
                creatureLocations[self.xyz] = [self]
            creatureNames[self.name] = self
    def describe(self):
        if players[selectedPlayer].location in creatureLocations.keys() and self in creatureLocations[players[selectedPlayer].location]:
            typewrite(self.description)
        else:
            typewrite("There is no such creature here.")
    def reveal(self):
        if self.xyz in creatureLocations.keys() and self in creatureLocations[self.name]:
            typewrite("ERROR: Scenario already revealed")#apply to all
        elif self.xyz in creatureLocations.keys():
            creatureLocations[self.xyz].append(self)
            creatureNames[self.name] = self
        else:
            interactions[self.xyz] = [self]
            creatureNames[self.name] = self
    def newMessage(self, newmessage):
        if "message" in self.kwargs.keys():
            self.kwargs["message"] = newmessage
    def talk(self):
        if players[selectedPlayer].location in creatureLocations.keys() and self in creatureLocations[players[selectedPlayer].location]:
            if "message" in self.kwargs.keys():
                typewrite(self.kwargs["message"])
            else:
                typewrite("There is nothing to talk about.")
        else:
            typewrite("There is no such creature here.")
    #def move(self):#scenario or when someone gets to a place
        
#put an interaction in the interactions variable; this is the interaction triggered by giving the person something

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
bunzulus = _user("gonzo", 100, 0, 0, 0, 0, 0, [])

teownSquare = _location(0, 0, 0, "the town square", "it reeks of bunzalus balloons gas. this explains how he was \'deflated\'", [1, 0, 0, 0, 0, 0], 0)
tunzunzulus = _location(0, 1, 0, "the garbage", "AHH!. It's disgusting. The murder weapon of bunzulus balloon lies in front of you... the garbage can. Tears start rushign to your eyes as you start to get tears at your eyes because of sadness.", [0, 1, 0, 0, 0, 0], 0)
testloc = _location(0, -1, 0, "the test", "meh", [1, 0, 0, 0, 0, 0], 1)

thingy = _object(0, 1, 0, 0, 0, "thingy", "a THINGY in the corner", "is jus a lil thingymebober chillin there.")
hillew = _object(0, 1, 0, 100, 1, "bunz", "a new BUNZ on the floor", "its there nib.")

bunzulusb = _creature(0, 1, 0, 0, "bunzulus", "a wild bunzulus in the corner", "issa bunzulus", message = "chopsy cropsy")

interaction2 = _interaction(hillew, "0-10", 1, "new", delete = [tunzunzulus, hillew])
interaction1 = _interaction(thingy, "000", 0, "henlo", reveal = [testloc, hillew, interaction2], delete = [thingy], open = [hillew], money = 100, newmsg = {bunzulusb:"chopsycropsy the senior"})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Engine~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#update players[selectedPlayer] location after every move
#update if the location was visited

def gameEngine():
    terminate = 0
    while terminate != 1:
        command = str(input(">")).lower()
        parse(command, " ", parseCommand)
        global recognizedCommand
        recognizedCommand = 0
        if "go" in parseCommand:
            recognizedCommand = 1
            players[selectedPlayer].move("north", 0, 1, 0, 0)
            players[selectedPlayer].move("south", 0, -1, 0, 1)
            players[selectedPlayer].move("east", 1, 0, 0, 2)
            players[selectedPlayer].move("west", -1, 0, 0, 3)
            players[selectedPlayer].move("up", 0, 0, 1, 4)
            players[selectedPlayer].move("down", 0, 0, -1, 5)
            if recognizedCommand != 2:
                typewrite("You can't go that way.")
        if "look" in parseCommand and "at" in parseCommand:
            recognizedCommand = 1
            parseCommand.remove("look")
            parseCommand.remove("at")
            objectName = getName()
            if objectName in objectNames.keys():
                objectNames[objectName].describe()
            elif objectName in creatureNames.keys():
                creatureNames[objectName].describe()
            else:
                typewrite("There is no such thing here.")
        if "take" in parseCommand:
            recognizedCommand = 1
            parseCommand.remove("take")
            objectName = getName()
            if objectName in objectNames.keys():
                objectNames[objectName].take()
            else:
                typewrite("There is no such object here.")
        if "use" in parseCommand:
            recognizedCommand = 1
            parseCommand.remove("use")
            objectName = getName()
            if objectName in interactions.keys():
                for i in interactions[objectName]:
                    i.activate()
            else:
                recognizedCommand = 2
                typewrite("There is no such object in your inventory")
            if recognizedCommand != 2:
                typewrite("There is no use for that here.")
        if "buy" in parseCommand:
            recognizedCommand = 1
            parseCommand.remove("buy")
            objectName = getName()
            if objectName in objectNames.keys():
                objectNames[objectName].buy()
            else:
                typewrite("There is no such object here")
        if "talk" in parseCommand and "to" in parseCommand:
                recognizedCommand = 1
                parseCommand.remove("talk")
                parseCommand.remove("to")
                objectName = getName()
                if objectName in creatureNames.keys():
                    creatureNames[objectName].talk()
                else:
                    typewrite("There is no such creature here")
        if "info" in parseCommand:
            recognizedCommand = 1
            typewrite("Inventory: " + str(players[selectedPlayer].inventory))
            typewrite("Money: " + str(players[selectedPlayer].money))
        if "help" in parseCommand:
            typewrite("Here are all the valid commands: help; go <north/south/east/west/up/down>; info; take <objectName>; use <objectName>; buy <objectName>")
            recognizedCommand = 1
        if recognizedCommand < 1:
            typewrite("That is not a valid command. Type \"help\" to see a list of all valid commands")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Game~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
locations[players[selectedPlayer].location].describe()
gameEngine()




