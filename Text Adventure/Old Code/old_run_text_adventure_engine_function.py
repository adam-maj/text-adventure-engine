# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 16:38:43 2018

@author: AdamMaj
"""

run_game_engine = True

def get_user_input():
    """
    Returns the users input parsed into a list with one word each item
    """
    
    user_input = input("> ").lower()
    parsed_user_input = user_input.split()
    
    return parsed_user_input
    
def run_text_adventure_engine(win_condition = None):
    """
    Main engine of the text adventure
    
    The engine can be terminated in two ways
    
    First, a scenario can set <run_game_engine> to False ending the loop
    
    Second, the user can create their own function which is inputed
    into <win_condition>. If this function becomes true throughout the
    engine, the engine will terminate
    """
    
    run_game_engine = True
    
    while run_game_engine:
        user_input = get_user_input()
        user_command, command_word = get_command(user_input)
        user_direct_object = get_direct_object(user_input, command_word)
        get_response = user_command(user_direct_object) if len(signature(user_command).parameters) > 0 else user_command()
    
        #Test if the game is over
        if win_condition != None and win_condition():
            run_game_engine = False
    
        #Only print statement in the entire engine
        print(get_response)