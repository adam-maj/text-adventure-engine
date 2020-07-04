#========================================
#Title: Text Adventure Engine

#Creator: Adam Majmudar

#Date Created: Wednesday, July 4th, 2018

#Change Log: https://tinyurl.com/y7lzltvk
#========================================

"""
TO DO:
    - Make the coordinate max from 9 to 35 by using Base 36 digits (A-Z)
      Edit this in get_adjacent_location function
"""


#Used in the run_text_adventure_engine command to test how many parameters each function takes
from inspect import signature

#Stores instance variable of the current player
current_player = None

#Stores all the visible locations in the map at a given point
locations = {}

#Stores the triggers of all the visible events
event_triggers = {}

#Stores the names of all the referencable objects
object_names = {}

#Stores the locations of all visible objects
object_locations = {}

#Stores the names of all referencable creatures
creature_names = {}

#Stores the locations of all visible creatures
creature_locations = {}

#Stores the names of the directions, their delta changes, and their exit indices from the locations point of view, and from the location in that directions point of view
directions = {"north" : (0, 1, 0, 0, 2),
              "east" : (1, 0, 0, 1, 3),
              "south" : (0, -1, 0, 2, 0),
              "west" : (-1, 0, 0, 3, 1),
              "up" : (0, 0, 1, 4, 5),
              "down" : (0, 0, -1, 5, 4)}

   
class Player(object):
    
    def __init__(self, x, y, z, money = 0, inventory_capacity = 10, inventory = None):
        """
        <money>: Optional argument which tells how much money the player has
        at the start of the game. Defaults to 0.
        
        <inventory_capacity>: The maximum number of objects the players
        inventory can hold at the begining of the game
        
        <inventory>: Optional argument which stores the instances of the 
        objects inside the players inventory. Defaults to empty
        """
        
        self.location = str(x) + str(y) + str(z)
        self.money = money
        self.inventory_capacity = inventory_capacity
        self.inventory = get_list_default(inventory)
        
        global current_player
        current_player = self

    def move_player(self, location):
        """
        Moves the player to a new location with the given coordinates
        """
        
        self.location = str(location)
        
    def get_location(self):
        """
        Returns the instance of the location class that the player
        is currently 'in'
        
        This is simply for easy access throughout the code
        """
        
        return locations[self.location]
        
    
class Location(object):    
    
    def __init__(self, name, x, y, z, visible, exits, 
                 description = None, initial_description = None):   
        """
        <exits>: Which directions you can exit from the room where 'True' 
        denotes an exit and 'False' denotes no exit; Order: [N, E, S, W, U, D]
        
        <description>: Message displayed whenever the user enters this location
                
        <initial_description>: Message displayed ONLY the first time the player
        enters this location
        
        <visible>: Whether the location is visible at the start of the engine.
        Can later be made visible through an <Event> class
        """
        
        self.name = name
        self.location = str(x) + str(y) + str(z)
        self.exits = exits
        self.description = description
        self.initial_description = initial_description
        self.visible = visible
        self.visited = False
        
        if visible:
            self.reveal()
            
    def check_exit(self, delta_x, delta_y, delta_z, exit_index):
        """
        Checks if a player can move in a given direction to an
        adjacent location
        
        Verifies if such a location exists
        
        Verifies if there is an exit from the current location into the 
        new location
        
        Returns the value of the current player's location's exit in the
        desired direction (True or False)
        """
        
        adjacent_location = get_adjacent_location(delta_x, delta_y, delta_z, self.location)

        if adjacent_location in locations.keys():
            return self.exits[exit_index]
    
    def change_exit(self, delta_x, delta_y, delta_z, exit_index, new_value):
        """
        This function changes the exits of the locations adjacent to
        the newly revealed or deleted location to the desired value <new_value>
        
        <delta_z>, <delta_y>, <delta_z>: Determines which locations exits
        will be changed. The difference in value between the coordinates of 
        the current location and the location whose exit will be changed
        
        <exit_index>: The index of the exit you are changing in the adjacent
        locations <exits> attribute where the exits are [N, E, S, W, U, D]
        
        <new_value>: The value that the adjacent locations exits are being
        change to. False if a location is being deleted, or the same value as
        the locations exit into them if a location is being revealed
        """
        
        adjacent_location = get_adjacent_location(delta_x, delta_y, delta_z, self.location)
        
        if adjacent_location in locations.keys():
            locations[adjacent_location].exits[exit_index] = new_value
        
    def reveal(self):
        """
        Makes a location visible to the rest of the environment
        
        Adds location to the list of referencable locations <locations>
        
        If the location is being revealed midgame rather than at 
        initialization, changes the exits of all adjacent locations to match 
        the exits of the location being revealed - Every location that the 
        newly revealed location has exits to will have exits back into the
        newly revealed location
        """
        
        locations[self.location] = self
        
        #Does not occur if this function is called at initialization
        if not self.visible:
            for direction, values in directions.items():
                self.change_exit(values[0], values[1], values[2], values[4], self.exits[values[3]])
            self.visible = True
    
    def delete(self):
        """
        Removes a location from the rest of the environment
        
        Removes it from the list of referencable locations <locations>
        
        Changes the exits of the adjacent locations to no longer lead to this location
        """
        
        locations.pop(self.location)
        
        for direction, values in directions.items():
            self.change_exit(values[0], values[1], values[2], values[4], False)
        
        self.visible = False

    def get_instances(self, dictionary):
        """
        Takes either the dictionary <object_locations> or <creature_locations>
        in the input <dictionary>
        
        Returns a string containing the names of the visible objects or creatures in this 
        location
        
        Used in the <describe> command for Locations to print which objects or creatures
        are in a room
        
        Inserts the name of each object or creature into the objects <room_location> 
        variable in all caps if the variable is not set to its default value
        and uses this <room_location> in the returned string <valid_objects>
        
        For example: a <room_location> of 'a {} in the corner reads' like 
        'a KEY in the corner'
        
        If the object has a default value for <room_location>, then just use 
        its name in the returned string <vaid_objects>
        """

        names_of_instances = [instance.room_location.format(instance.name.upper()) if instance.room_location else instance.name.upper() for instance in dictionary[self.location]]
        if len(names_of_instances) > 1:
            valid_instances = "There is " + ", ".join(names_of_instances[:-1])
            valid_instances += "," if len(names_of_instances) > 2 else ""
            valid_instances += " and " + names_of_instances[-1]
        else:
            valid_instances = "There is " + names_of_instances[0]
        
        return valid_instances
    
    def get_directions(self):
        """
        Returns a string containing the directions the player can travel
        from the current location
        
        Used in the <describe> command for Locations to print which directions
        the player can travel from the current location based on that
        location's <exits> attribute
        """
        
        names_of_directions = [direction.upper() for direction, values in directions.items() if self.exits[values[3]] == 1] 
        if len(names_of_directions) > 1:
            valid_directions = "You can go " + ", ".join(names_of_directions[:-1])
            valid_directions += "," if len(names_of_directions) > 2 else ""
            valid_directions += " and " + names_of_directions[-1]
        else:
            valid_directions = "You can go " + names_of_directions[0] 
        
        return valid_directions
    
    def describe(self):
        """
        Returns a description of the location containing the following:
        
        The name of the location
        
        The description of the location itself stored in <description>
        or <initial_description>
        
        The visible objects in that location
        
        The visible creatures in that location
        
        The directions the player can travel from that location
        """
        
        #Add location name to description
        description = "You are at {}".format(self.name) + "\n"
        
        #Add the location's description to the description
        if self.initial_description and not self.visited:
            description += self.initial_description + "\n"
            self.visited = True
        elif self.description:
            description += self.description + "\n"                 
        
        #Add the objects in the player's location to the description
        if self.location in object_locations.keys():
            description += self.get_instances(object_locations) + "\n"
        
        #Add the creatures in the player's location to the description
        if self.location in creature_locations.keys():
            description += self.get_instances(creature_locations) + "\n"
        
        #Adds the available directions to the description
        description += self.get_directions()
        
        return description
        
    
class Object(object):
    
    def __init__(self, name, x, y, z, visible, takeable = True, room_location = None,
                 description = None):
        """
        <visible>: Whether the object is visible at the start of the engine.
        Can later be made visible through an <Event> class
                
        <room_location>: Optional variable that states where the object is in
        its room. Format is as folows: 'a {} in the corner.' In this case the
        name of the object is substituted for the brackets
                
        <takeable>: Determines if the player can take the object and move it 
        into their inventory
        """
        
        self.name = name.lower()
        self.location = str(x) + str(y) + str(z)
        self.visible = visible
        self.takeable = takeable
        self.room_location = room_location
        self.description = description
        
        #The object is added to the list regardless of whether it is visible or not
        #Because it does not to be deleted from a list to make the object invisible
        #Since the game can only see the object if it is a location <object_locations> or <inventory>
        object_names[self.name] = self
        
        if visible:
            self.reveal()
    
    def reveal(self):
        """
        Makes the object visible to the rest of the environment by adding
        it to the specified location
        
        Adds the object to the dictionary <object_locations>
        """
        
        if self.location in object_locations.keys():
            object_locations[self.location].append(self)
        else:
            object_locations[self.location] = [self]

        self.visible = True
    
    def delete(self):
        """
        Removes the object from its current location
        
        If there are no other objects in that location, then pop the
        location from the dictionary <object_locations>
        
        If the object is not in any location, then this removes the object 
        from the players inventory
        """
        
        if self.location in object_locations.keys() and self in object_locations[self.location]:
            object_locations[self.location].remove(self)
            if not object_locations[self.location]:
                object_locations.pop(self.location)
        else:
            current_player.inventory.remove(self.name)
            
        self.visible = False

    def describe(self):
        """
        Returns the description of the object
        
        Used in the 'look at' command
        """
        
        return self.description

    def take(self):
        """
        Adds the object to the current players inventory
        
        The objects <location> attribute remains unchanged until the
        object is dropped
        
        Returns a message that the object was successfully taken
        """
        
        current_player.inventory.append(self.name)
        
        return "You took the {}.".format(self.name.upper())
    
    def drop(self):
        """
        Removes the object from players inventory
        
        Adds it to the players location at the point when he drops
        the object
        
        Returns a message that the object was successfully dropped
        """
        
        self.delete()
        self.location = current_player.location
        self.reveal()
        
        return "You dropped {}.".format(self.name.upper())
    
    
class Event(object):
    
    def __init__(self, x, y, z, trigger, reward = 0, message = "", verb = "use", 
                 visible = True, reveal_list = None, delete_list = None, receive_list = None,
                 move_list = None, exit_change_list = None, message_list = None,
                 description_list = None):
        """
        <trigger>: The object "used" or "given" by the player in order to activate this event
        
        <reward>: The amount of money awarded to the player for activating this event
        
        <message>: The message displayed when the event is activated
        
        <verb>: Which word is used to activate this eent
        
        <trigger_list>: The object that must be used to trigger the event
        
        <reveal_list>: List of instances that will be revealed when the event is activated
        
        <delete_list>: List of instances that will be deleted when the event is activated
        
        <recieve_list>: List of instances added to the players inventory when the event is activated
        
        <move_list>: List of tuples containing the instance and the coordinates to move to.
        Example - (instance, new_x, new_y, new_z)
        
        <exit_list>: List of tuples containing the location and the exit index to change
        Example - (x, y, z, exit_index)
        
        <message_list>: List of tuples containing the instance, the location of the message
        and the message to add/edit
        Example - (instance, x, y, z, new_message)
        """

        self.location = str(x) + str(y) + str(z)
        self.trigger = trigger
        self.reward = reward
        self.message = message
        self.verb = verb
        self.visible = visible
        self.reveal_list = get_list_default(reveal_list)
        self.delete_list = get_list_default(delete_list)
        self.receive_list = get_list_default(receive_list)
        self.move_list = get_list_default(move_list)
        self.exit_change_list = get_list_default(exit_change_list)
        self.message_list = get_list_default(message_list)
        self.description_list = get_list_default(description_list)
        
        if self.visible:
            self.reveal()
            
    def reveal(self):
        """
        Makes the event visible to the rest of the environment
        
        Adds the event to the dictionary <event_triggers> which stores the event which
        can be referenced by the object used to trigger it.
        """

        if self.trigger.name in event_triggers.keys():
            event_triggers[self.trigger.name].append(self)
        else:
            event_triggers[self.trigger.name] = [self]
            
        self.visible = True
    
    def delete(self):
        """
        Removes the event from the rest of the environment by taking it out of 
        the <event_triggers> dictionary.
        
        If there are no other events triggered by the same object, remove the 
        object's name from the keys of <event_triggers>
        """
        
        event_triggers[self.trigger.name].remove(self)
        if not event_triggers[self.trigger.name]:
            event_triggers.pop(self.trigger.name)
    
        self.visible = False
    
    def add_reveal(self, *args):
        """
        User friendly command to add an instance to the reveal list
        """
        
        for arg in args:
            self.reveal_list.append(arg)

    def add_delete(self, *args):
        """
        User friendly command to add an instance to the delete list
        """
        
        for arg in args:
            self.delete_list.append(arg)

    def add_receive(self, *args):
        """
        User friendly command to add an instance to the receive list
        """
        
        for arg in args:
            self.receive_list.append(arg)
    
    def add_move(self, instance, new_x, new_y, new_z):
        """
        User friendly command to add an instance to the move list
        
        A tuple is added with the instance to be moved and the location to be moved to
        """
        
        self.move_list.append((instance, new_x, new_y, new_z))
    
    def add_exit_change(self, instance, exits):
        """
        User friendly command to add an instance to the exit change list
        
        A tuple is added with the instance to change the exits and the new exits list
        """
        
        self.exit_change_list.append((instance, exits))
    
    def add_message(self, instance, x, y, z, message):
        """
        User friendly command to add an instance to the message list
        
        A tuple is added with the instance to change the message, the location of the message
        and the new message
        """
    
        self.message_list.append((instance, x, y, z, message))
    
    def add_description(self, instance, description):
        """
        User friendly command to add an instance to the description list
        
        A tuple is added with the instance to change the description and the description
        """
    
        self.description_list.append((instance, description))
    
    def activate(self):
        """
        Activate the event
        
        Adds objects in <recieve> to player's inventory
        
        Deletes objects in <delete>
        
        Reveals objects in <reveal>
        """
        
        current_player.money += self.reward
        
        for instance in self.delete_list:
            instance.delete()
                
        for instance in self.reveal_list:
            instance.reveal()

        for instance in self.receive_list:
            instance.take()
 
        for coordinate_tuple in self.move_list:
            coordinate_tuple[0].move(coordinate_tuple[1], coordinate_tuple[2], coordinate_tuple[3])
        
        for coordinate_tuple in self.exit_change_list:
            coordinate_tuple[0].exits = coordinate_tuple[1]
        
        for coordinate_tuple in self.message_list:
            coordinate_tuple[0].edit_message(coordinate_tuple[1], coordinate_tuple[2], coordinate_tuple[3], coordinate_tuple[4])
            
        for coordinate_tuple in self.description_list:
            coordinate_tuple[0].description = coordinate_tuple[1]
            
        return self.message


class Creature(object):
    
    def __init__(self, name, x, y, z, visible, room_location = None, description = None,
                 messages = None):
        """
        <messages>: Dictionary with the location of the message as the key and the 
        message as the value
        """
        
        self.name = name.lower()
        self.location = str(x) + str(y) + str(z)
        self.visible = visible
        self.room_location = room_location
        self.description = description
        
        if messages is None:
            self.messages = {}
        else:
            self.messages = messages
        
        #Add name to the list whether it is visible or not, see explanation in object class
        creature_names[self.name] = self
        
        if self.visible:
            self.reveal()
    
    def reveal(self):
        """
        Makes the creature visible to the rest of the environment by adding
        it to the specified location
        
        Adds the creature to the dictionary <creature_locations>
        """
        
        if self.location in creature_locations.keys():
            creature_locations[self.location].append(self)
        else:
            creature_locations[self.location] = [self]
    
        self.visible = True
    
    def delete(self):
        """
        Removes the creature from the rest of the environment by taking it out of 
        the <event_locations> dictionary.
        
        If there are no other creatures in the same location, remove the 
        creature's location from the keys of <event_triggers>
        """
        
        creature_locations[self.location].remove(self)
        
        if not creature_locations[self.location]:
            creature_locations.pop(self.location)
            
        self.visible = False

    def move(self, new_x, new_y, new_z):
        """
        Move creature to new location specified by coordinates
        """
        
        self.delete()
        self.location = str(new_x) + str(new_y) + str(new_z)
        self.reveal()
    
    def edit_message(self, x, y, z, message):
        """
        Add/change a message in the messages list with the specified location as the key
        and the message as the value
        """
        
        message_location = str(x) + str(y) + str(z)
        self.messages[message_location] = message
    
    def describe(self):
        """
        Returns the description provided for the object
        """
        
        return self.description
    
    def talk(self):
        """
        Returns the message specified for this creature in the creatures current location
        """

        return self.messages[self.location]
        

def get_user_input(user_input):
    """
    Returns the users input parsed into a list with one word each item
    """

    parsed_user_input = user_input.split()
    
    return parsed_user_input

def get_command(user_input):
    """
    Takes the list containing the parsed user input
    
    Returns the function which stores the 
    command used by the user based on a list of valid
    commands <valid_commands>
    
    Returns the string name of the command
    """
    
    valid_commands = {"go" : command_go, 
                      "talk to" : command_talk_to,
                      "look at" : command_look_at,
                      "take" : command_take,
                      "drop" : command_drop,
                      "use" : command_use_give,
                      "give" : command_use_give,
                      "buy" : command_buy}
    
    for command in valid_commands:
        command_words = command.split()
        for index in range(len(command_words)):
            is_last_word = index == len(command_words) - 1
            if command_words[index] not in user_input:
                break
            elif is_last_word:
                return valid_commands[command], command

def get_direct_object(user_input, user_command):
    """
    Takes the list containing the parsed user input and the command
    used by the user
    
    Returns the name of the direct object in the user input
    """
    
    command_words = user_command.split()
    for word in command_words:
        user_input.remove(word)
    direct_object = " ".join(user_input)
    return direct_object

def get_adjacent_location(delta_x, delta_y, delta_z, reference_location):
    """
    Gets the location adjacent to the <reference_location> in the
    direction specified by the <delta> parameters
    
    Returns the location in "XYZ" format
    
    The try-except clauses are to deal with the fact that negative signs count as there own
    character, so if you want to join the negative sign to a number, it has to be in a try loop,
    otherwise the int() function returns a ValueError
    """
    
    location_index = 0
    
    try:
        adjacent_x = int(reference_location[location_index]) + delta_x
        location_index += 1
    except ValueError:
        adjacent_x = int(reference_location[location_index] + reference_location[location_index + 1]) + delta_x
        location_index += 2
    
    try:
        adjacent_y = int(reference_location[location_index]) + delta_y
        location_index += 1
    except ValueError:
        adjacent_y = int(reference_location[location_index] + reference_location[location_index + 1]) + delta_y
        location_index += 2
    
    try:
        adjacent_z = int(reference_location[location_index]) + delta_z
        location_index += 1
    except ValueError:
        adjacent_z = int(reference_location[location_index] + reference_location[location_index + 1]) + delta_z
        location_index += 2
    
    adjacent_location = str(adjacent_x) + str(adjacent_y) + str(adjacent_z)

    return adjacent_location

def command_go(user_direct_object):
    """
    Takes the direction the user wants to move as input <user_direct_object>

    Returns a description of the players new location
    
    Executes:
        -If the user wants to go in a valid direction in the dictionary <directions>
        -If the users current location has an exit in the desired direction
    
    Executes the commands to move the player and describe the new location
    """
    
    if user_direct_object in directions.keys():
        direction = directions[user_direct_object]
        current_location = current_player.get_location()
        if current_location.check_exit(direction[0], direction[1], direction[2], direction[3]):
            adjacent_location = get_adjacent_location(direction[0], direction[1], direction[2], current_player.location)
            current_player.move_player(adjacent_location)
            return current_player.get_location().describe()
    
    return "You can't go that way."

def command_take(user_direct_object):
    """
    Takes the object the user wants to take as input <user_direct_object>
    
    Returns the message from taking the object
    
    Executes:
        -If the the user wants to take a valid object
        -If the valid object the user wants to take is visible
        -If the the user has not already taken the valid object
        -If the user is in the same location as the object
        -If the object can be taken
        -If the user has enough space in their inventory to hold the object
    
    Executes the commands to delete the object and take the object to add it to the
    players inventory
    """

    if user_direct_object in object_names.keys():
        direct_object = object_names[user_direct_object]
        if direct_object.visible:
            if direct_object.name not in current_player.inventory:
                if direct_object.location == current_player.location:    
                    if direct_object.takeable:
                        if len(current_player.inventory) < current_player.inventory_capacity:
                            direct_object.delete()
                            return direct_object.take()
                    
                        return "You don't have space for that in your inventory."
                    
                    return "You can't take that."
                
                return "There is no such object here"
            
            return "You already have that"
    
    return "There is no such object here."

def command_drop(user_direct_object):
    """
    Takes the object the user wants to drop as input <user_direct_object>
    
    Returns the message for dropping an object
    
    Executes:
        -If the user wants to drop a valid object
        -If the object the user wants to drop
    
    Executes the commands to drop an object
    """
    
    if user_direct_object in object_names.keys():
        direct_object = object_names[user_direct_object]
        if direct_object.name in current_player.inventory:
            return direct_object.drop()
    
    return "There is no such object in your inventory"
    
def command_use_give(command, user_direct_object):
    """
    Takes the object the user wants to give/use as input <user_direct_object> and the
    command the user uses as input <command>
    
    Returns the message associated with the event tied to the given direct object
    through the dictioinary <event_triggers>
    
    Executes:
        -If the user is using an object that is in their inventory
        -If the object being used actually triggers and event soecified in the
        dictionary <event_triggers>
        -If any of the events triggered by the object occur in the same location
        as the player is in currently
        -If the verb used by the user matches the verb necessary to trigger the event
    
    Executes the command to activate the event tied with the given direct object
    through the dictionary <event_triggers>
    """

    if user_direct_object in current_player.inventory:
        if user_direct_object in event_triggers.keys():
            for i in range(0, len(event_triggers[user_direct_object])):
                instance = event_triggers[user_direct_object][i]
                if instance.location == current_player.location:
                    if instance.verb == command:
                        return instance.activate()
                    if i == len(event_triggers[user_direct_object]) - 1:
                        return "There is no use for that here" if instance.verb == "give" else "There is no point in giving that to anyone here."
        
        return "There is no use for that here."
    
    return "There is no such object in your inventory"
            
def command_talk_to(user_direct_object):
    """
    Takes the creature the user wants to talk to as input <user_direct_object>
    
    Returns the message of the creature that is specified for the given location
    
    Executes:
        -If the user wants to talk to a valid creature
        -If the creature the user wants to talk to is visible
        -If the creature is in the same location as the player
        -If the creature has a message specified in the creature class attribute
        <messages> to say something in the players location
    
    Executes the command to display the message of the creature
    """
    
    if user_direct_object in creature_names.keys():
        direct_object = creature_names[user_direct_object]
        if direct_object.visible:
            if direct_object.location == current_player.location:
                if current_player.location in direct_object.messages.keys():
                    return direct_object.talk()
                
                return "There is nothing to talk about."
            
    return "There is no such creature to talk to here."
                

def command_look_at(user_direct_object):
    """
    Takes the creature or object the user wants to look at as input <user_direct_object>
    
    Returns the description of the creature or object desired
    
    Executes:
        -If the user wants to look at a valid object or creature
        -If the object or creature is visible
        -If the object or creature is in the same location as the player or in the players inventory
        -If the object or creature has a description specified by the creator of the text adventure
    
    Executes the command to display the description of the creature or object
    """
    
    if user_direct_object in creature_names.keys() or user_direct_object in object_names.keys():
        direct_object = creature_names[user_direct_object] if user_direct_object in creature_names.keys() else object_names[user_direct_object]
        if direct_object.visible:
            if direct_object.location == current_player.location or user_direct_object in current_player.inventory:
                if direct_object.description:
                    return direct_object.describe()
                
                return "There is nothing particularly interesting about that"
            
    return "There is no such thing here to look at"

def command_buy(user_direct_object):
    """
    """
    pass

def get_start_description():
    """
    Returns the description of the starting location of the game for
    convenience purposes
    """
    
    return current_player.get_location().describe() + "\n"

def get_list_default(value):
    """
    Takes an attribute from an object as a parameter
    If this attribute is still set to the default value "None," return an empty list
    Otherwise, just return its value
    
    I have to do this instead of just defining an attribute as [] in the object __init__
    function because of mutability issues
    
    See: https://stackoverflow.com/questions/1011431/common-pitfalls-in-python/1321061#1321061
    """

    if value is None:
        return []
    else:
        return value

def get_inventory():
    """
    Returns the current players inventory formatted so that it fits well in the
    gui's textedit box
    """
    
    return "\n".join(current_player.inventory)

def get_player_stats():
    """
    Returns the current players stats to the gui so it can be printed in the stats
    tab
    """
    
    stats = "Money - {} \nMax Inventory Capacity - {}".format(current_player.money, 
                                                              current_player.inventory_capacity)
    return stats

def run_text_adventure_engine(gui_input):
    """
    Main engine of the text adventure
    
    Takes the user input from the GUI
    
    Returns the statement to be printed to the GUI
    
    If the user did not submit a valid command, returns 'You can't do that'
    """
    
    try:
        user_input = get_user_input(gui_input.lower())    
        user_command, command_word = get_command(user_input)
        user_direct_object = get_direct_object(user_input, command_word)
        
        #Check how many parameters need to be provided to the given command's function
        number_of_parameters = len(signature(user_command).parameters)
        if number_of_parameters == 2:
            get_response = user_command(command_word, user_direct_object)
        elif number_of_parameters == 1:
            get_response = user_command(user_direct_object)

        return "\n> {}\n{}\n".format(gui_input, get_response)
    
    except TypeError:
        return "\n> {}\nYou can't do that.\n".format(gui_input)