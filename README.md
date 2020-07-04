# text-adventure-engine
An object-oriented text-adventure-engine to create text adventures complete with locations, objects, players, people, and events.

<h3>Main Files</h3>
<strong>Most Recent Engine:</strong> Text Adventure/Text Adventure Engine/text_adventure_engine_2.0.py <br>
<strong>GUI:</strong> Text Adventure/Text Adventure Engine/text_adventure_gui.py <br>
<strong>Example Text Adventure:</strong> Text Adventure/Text Adventure Engine/fate_of_ashborne.py <br>

If you want to look at the engine itself works, both text_adventure_engine files are fully documented.

<h3>Run Text Adventure</h3>

<h3>Create Your Own Text Adventures</h3>
Look at fate_of_ashborne.py for an example text adventure using many of the engines features.

At the start of a text adventure file, import the GUI and Engine. Create classes in the middle. At the end of the file run the gui.start_engine() command. Run the text adventure from the created file.

Everything that allows you to modify your text adventure is a class (Player, Location, Object, Event, Creature).

The attributes of each class are fully explained in the text_adventure_engine documentation. Here is a brief description of each class:
<strong>Player: </strong>The person playing the text adventure with an inventory. This is the person who moves around the entire map.
<strong>Location: </strong>Creates a new location on the X, Y, Z plane with a description. Players can walk into these locations. Locations have different exits (directions which players can exit them from). Limiting exits can be used as walls/doors. Exits can also be locked and unlocked with the Event class.
<strong>Object: </strong>Creates a new object in a specified location. If objects are takeable, then the player can pick them up. Objects can also be hidden inside other objects (the container object would need to be opened with an Event class). Objects can be moved with Events.
<strong>Creatures: </strong>Creates a creature that can talk to the player. Creatures can be moved with events.
<strong>Event: </strong>This class handles most of the interactive aspects of the text adventure. Players can use items or open things to activate an event. Events handle every other class and can effectively create and delete locations, objects, and creatures, move objects and creatures, and can open and close exits. These can be used in many different ways for various different effects.

<h3>About Project</h3>
This is an old iteration on one of my first projects ever (I made the first version in 2016, and the most recent version in 2018.
