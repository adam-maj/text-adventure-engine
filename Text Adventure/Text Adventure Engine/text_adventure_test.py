#========================================
#Title: Test Run 

#Creator: Adam Majmudar

#Date Created: Saturday, July 14th, 2018
#========================================

import text_adventure_engine as txt
import text_adventure_gui as gui

main_player = txt.Player(0, 0, 0)

town_square = txt.Location("The Town Square", 0, 0, 0, True, [True, False, False, False, False, False])
town_square.initial_description = "The sunset is beautiful and you watch with all of the other townspeople"
town_square.description = "There are people hustling and bustling all around you"

bar = txt.Location("The Bar", 0, 1, 0, True, [True, False, True, False, True, False])
bar.description = "It is loud and crowded as people bustle around you."
bar.initial_description = "This bar looks nice, you make a note to come back here soon."

construction = txt.Location("Construction Area", 0, 2, 0, True, [False, False, True, False, False, False])

bar_party_room = txt.Location("Party Room", 0, 2, 0, False, [False, False, True, False, False, False])

armory = txt.Location("The Armory", 0, 1, 1, True, [False, False, False, False, False, True])

key = txt.Object("Key", 0, 0, 0, True)
key.room_location = "a {} on the table"
key.description = "The key is made of heavy bronze."

paper = txt.Object("Paper", 0, 2, 0, False)
paper.room_location = "a piece of {} on the floor"

beer = txt.Object("Beer", 0, 1, 0, True)
beer.room_location = "a keg of {} on a table"

heaven = txt.Location("Heaven", 0, 1, 2, True, [False, False, False, False, False, True])

bb = txt.Creature("Bunzulus balloon", 0, 1, 2, True)
bb.edit_message(0, 1, 2, "hillew wrld")
bb.room_location = "a {} in the corner"

my_event = txt.Event(0, 1, 0, key)
my_event.message = "you used the key, a paper appeared."
my_event.reward = 100
my_event.add_delete(my_event, key)
my_event.add_reveal(bar_party_room, paper)
my_event.add_move(bb, 0, 1, 1)
my_event.add_exit_change(armory, 4, True)
my_event.add_message(bb, 0, 1, 1, "success!")

other_event = txt.Event(0, 1, 0, paper)
other_event.message = "you used the paper"
other_event.add_delete(other_event, paper)

gui.start_engine()
