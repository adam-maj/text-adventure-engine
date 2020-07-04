#========================================
#Title: Test Run 

#Creator: Adam Majmudar

#Date Created: Saturday, July 14th, 2018
#========================================

import text_adventure_engine as txt
import text_adventure_gui as gui

#Ease of Use for True and False
T = True
F = False

main_player = txt.Player(0, 0, 0)

forest_glade = txt.Location("A Glade in the Forest", 0, 0, 0, T, [T, T, T, T, F, F])
forest_glade.initial_description = "As you get yourself up, your eyes slowly open and adjust to the bright light coming into the glade. You look around to find yourself in the middle of a densely packed pine wood forest. You note that it probably continues for miles around you..."
forest_glade.description = "The dense pine woodforest likely extends for miles around you. This glade is one of the few areas in the forest that allows sunlight to pierce the deep darkness of the area."

wheat_field = txt.Location("A Wheat Field, ")

gui.start_engine()