#========================================
#Title: The Fate of Ashborne 

#Creator: Adam Majmudar

#Date Created: Friday, January 11th, 2019
#========================================

import text_adventure_engine as txt
import text_adventure_gui as gui

"""
Add intial phrase that establishes goal to 'find out what happened'

Can make it so that the names of objects don't reveal much but the descriptions 
when looking at them give hints

Add events which result from incorrect actions (ie. using the harpoon on the dog,
axe to open chest)

Events that are hidden, and you can only activate them once other events are completed
(events reveal other events)
- This can apply to conversations
"""

#Ease of Use for True and False
T = True
F = False

towering_cliffs = txt.Location("The Towering Cliffs", -1, 0, 0, T, [T, T, F, F, F, F])
towering_cliffs.initial_description = "A few hundred feet below, a river rushes by and beats the side of the precipitous cliff. You look out in the distance and can see what looks to be a large town burning with embers. Smoke rises from the ruins. You worry as you try to think what could have caused this..."
towering_cliffs.description = "A few hundred feet below, a river rushes by and beats the side of the precipitous cliff. You can see a burning town in the distance."

river_bank = txt.Location("The River Bank", -1, 1, 0, T, [F, T, T, F, F, F])
river_bank.description = "A river rushes by rapidly in front of you, crashing into rocks and causing the icy water to splash up against you."

deepest_forest = txt.Location("The Forest", 0, -3, 0, T, [T, T, F, F, F, F])
deepest_forest.initial_description = "This is the farthest point in the forest you should go. The forest ahead is full of sharp tree trunks and toppled trees. It would be unsafe to continue farther. For now at least..."
deepest_forest.description = "This is the farthest point in the forest you should go. The forest ahead is full of sharp tree trunks and toppled trees. It would be unsafe to continue farther."

forest_heart = txt.Location("The Heart of the Forest", 0, -2, 0, T, [T, T, T, F, F, F])
forest_heart.description = "The vast swathes of pine trees extend in all directions."

forest = txt.Location("The Forest", 0, -1, 0, T, [T, T, T, F, F, F])
forest.description = "There is very little light coming through the tree tops. Thick mist gathers around the trunks of the towering oak trees."

forest_clearing = txt.Location("A Clearing in the Forest", 0, 0, 0, T, [T, F, T, T, F, F])
forest_clearing.description = "Dim light shines through the thick canopy of oak trees above. The earth is ominously scorched and there is burnt tree bark strewn across the ground. There are large gates to the EAST with a padlock chaining them shut."

wheat_field = txt.Location("A Wheat Field", 0, 1, 0, T, [F, F, T, T, F, F])
wheat_field.initial_description = "Bent over stalks of wheat are all over and there is ash on the ground. What could have done this..."
wheat_field.description = "Bent over stalks of wheat are all over and there is ash on the ground. There is a shed at the NORTH end of the field, but the door appears to be locked."

shed = txt.Location("The Shed", 0, 2, 0, T, [F, F, T, F, F, F])
shed.description = "It is dark inside. There are cobwebs all across the walls. There are improvised shelves made of wood planks which hold up various tools and trinkets."

forest_cave = txt.Location("A Cave in the Middle of the Forest", 1, -3, 0, T, [T, F, F, T, F, F])
forest_cave.description = "The cave is pitch black and you cannot see anything. You hear the steady dripping of water from the ceiling of the cave to the floor"

ruined_forest = txt.Location("The Forest", 1, -2, 0, T, [T, F, T, T, F, F])
ruined_forest.description = "The trees in this area are all carelessly cut to the stumps. Ash lines the ground all around and the smell of burnt wood permeates through the air."

deep_forest = txt.Location("The Deep Forest", 1, -1, 0, T, [F, F, T, T, F, F])
deep_forest.description = "Trees are densely packed all around you. There is an eerie silence that denotes the absence of much wildlife in this area."

courtyard = txt.Location("The Courtyard", 1, 0, 0, T, [T, F, F, T, F, F])
courtyard.initial_description = "The ground is unkempt and scorched all around. In front of you is a dilapidated house. You notice some firewood lying on the porch, newly chopped. Someone - or something - has been here recently..."
courtyard.description = "The ground is unkempt and scorched all around. In front of you is a dilapidated house. The door is boarded shut with wood."

lake = txt.Location("The Lake", 1, 1, 0, T, [F, T, T, F, F, F])
lake.description = "The water is dark and dirty. The lake extends for a few hundred feet, no more."

house = txt.Location("The Dilapidated House", 2, 0, 0, T, [F, F, F, T, F, F])
house.description = "The house is messy. Food is lying around everywhere. A layer of dust covers every surface."

basement = txt.Location("The Basement", 2, 1, -1, T, [F, F, F, F, T, F])
basement.description = "It is dark and difficult to see. Cobwebs line the wooden ceilings."

garden = txt.Location("The Garden Behind the House", 2, 1, 0, T, [F, F, F, T, F, F])
garden.description = "There might once have been flowers and plants here but the only things that remain are ashes and wilted stems. The back of the house and an entrance to its basement lies before you."

bucket = txt.Object("Bucket", -1, 0, 0, T)
bucket.room_location = "a toppled {} next to some rocks"
bucket.description = "The pail is sturdy and is made of some metal, probably iron judging by the patches of rust on the inside."

full_bucket = txt.Object("Full Bucket", -1, 1, 0, F)
full_bucket.description = "The bucket is filled to the brim with water from the river."

axe = txt.Object("Axe", 0, -3, 0, T)
axe.room_location = "an {} wedged in a tree stump"
axe.description = "Just a normal old axe... for chopping things..."

grain = txt.Object("Grain", 0, 1, 0, T)
grain.room_location = "some {} on the ground"
grain.description = "Its just regular old grain. Probably wheat or something of that kind."

#Can edit last line of urns description to change difficulty
clay_urn = txt.Object("Clay Urn", 0, 2, 0, T, takeable = F)
clay_urn.room_location = "a {} on the shelf"
clay_urn.description = "The urn has faded patterns on it. There is an IRON KEY at the bottom but the hole on top is too small to reach through with your hand. There must be some way to get the key to the top..."

iron_key = txt.Object("Iron Key", 0, 2, 0, F)
iron_key.description = "Its just a rusted iron key. Its unusually large."

harpoon = txt.Object("Harpoon", 1, -3, 0, F)
harpoon.room_location = "a {} laying against a large rock"
harpoon.description = "It is sharpened to a point. It would be perfect to stab through something."

#Can edit last line of birds description to change difficulty
bird = txt.Object("Bird", 1, -1, 0, T, takeable = F)
bird.room_location = "a single {} high in the trees"
bird.description = "It appears to be a raven. There is something shiny around the birds foot, possibly a key. If only there were some way to make it come down from the trees..." 

wooden_key = txt.Object("Wooden Key", 1, -1, 0, F)
wooden_key.room_location = "a {} on the ground"
wooden_key.description = "It is a rather poorly made key. It seems to be made by someone with little experience in craftsmanship"

fish = txt.Object("Fish", 1, 1, 0, T, takeable = F)
fish.room_location = "a single {} visible in the lake"
fish.description = "The fish is a muted brownish color and is around a foot in length. It is the only fish you can see in the lake. Something terrible must have happened to the others..."

dead_fish = txt.Object("Dead Fish", 1, 1, 0, F)
dead_fish.description = "The dead fish is a muted brownish color and is around a foot in length. It reeks of rotting carcas and salt water."

torch = txt.Object("Torch", 1, 0, 0, T)
torch.room_location = "a {} mounted on front of the house"
torch.description = "The light emanating from the torch is bright."

chest = txt.Object("Chest", 2, 0, 0, T, takeable = F)
chest.room_location = "a {} in the corner"
chest.description = "The chest is sturdy and rectangular. It is made of iron and is locked. It has a gold lock hole."

golden_key = txt.Object("Golden Key", 2, 1, -1, T)
golden_key.description = "The key is clean and unblemished."
golden_key.room_location = "a {} lying on a shelf mounted to the wall"

hound = txt.Object("Hound", 2, 1, 0, T, takeable = F)
hound.room_location = "a {} barking at you fiercely and guarding the entrance to the basement angrily. You won't be able to get past him until he calms down."
hound.description = "The beast's ribs are visible through his skin. He looks starved."

sleeping_hound = txt.Object("Sleeping Hound", 2, 1, 0, F, takeable = F)
sleeping_hound.room_location = "a {} lying by the entrance to the basement"
sleeping_hound.description = "The hound is sleeping soundly. He must have enjoyed that meal."

bucket_event = txt.Event(-1, 1, 0, bucket)
bucket_event.message = "You dip the bucket in the river and the rushing water quickly fills it to the brim. You now have a FULL BUCKET."
bucket_event.add_delete(bucket)
bucket_event.add_receive(full_bucket)

iron_key_event = txt.Event(0, 0, 0, iron_key)
iron_key_event.message = "You walk up to the gates and try the iron key. It fits perfectly into the padlock and the gates are now open. You can now go EAST."
iron_key_event.add_delete(iron_key)
iron_key_event.add_exit_change(forest_clearing, [T, T, T, T, F, F])
iron_key_event.add_description(forest_clearing, "Dim light shines through the thick canopy of oak trees above. The earth is ominously scorched and there is burnt tree bark strewn across the ground. The gates to the EAST are now swung open and the padlock is on the ground.")

wooden_key_event = txt.Event(0, 1, 0, wooden_key)
wooden_key_event.message = "You walk toward the shed at the north end of the field pull out the key. It fits nicely into the keyhole in the shed door and you hear a click as the shed opens. You can now go NORTH."
wooden_key_event.add_delete(wooden_key)
wooden_key_event.add_exit_change(wheat_field, [T, F, T, T, F, F])
wooden_key_event.add_description(wheat_field, "Bent over stalks of wheat are all over and there is ash on the ground.")

full_bucket_event = txt.Event(0, 2, 0, full_bucket)
full_bucket_event.message = "You pour the water into the urn and watch as the IRON KEY inside rises with the water to the top and is now in your reach."
full_bucket_event.add_reveal(iron_key)
full_bucket_event.add_delete(full_bucket)
full_bucket_event.add_description(clay_urn, "The urn has faded patterns on it. It is a normal old urn.")

torch_event = txt.Event(1, -3, 0, torch)
torch_event.message = "You mount the torch on the wall and it illuminates the cave fully. You can now see the vastness of the underground cavern that extends below you. You also see a HARPOON lying against the cave walls."
torch_event.add_description(forest_cave, "The cave is illuminated with the torch. You can see the vastness of the underground cavern that extends below you and hear the steady dripping of water from the ceiling of the cave to the floor.")
torch_event.add_reveal(harpoon)
torch_event.add_delete(torch)

grain_event = txt.Event(1, -1, 0, grain)
grain_event.message = "A BIRD swoops down from the trees to nibble at the grain, dropping a WOODEN KEY on the ground. After quickly finishing its meal, the BIRD flies off."
grain_event.add_delete(grain, bird)
grain_event.add_reveal(wooden_key)

axe_event = txt.Event(1, 0, 0, axe)
axe_event.message = "You chop the boards blocking the door to the house. The doorway is now open so you can go EAST."
axe_event.add_exit_change(courtyard, [T, T, F, T, F, F])
axe_event.add_description(courtyard, "The ground is unkempt and scorched all around. In front of you is a dilapidated house.")

harpoon_event = txt.Event(1, 1, 0, harpoon)
harpoon_event.message = "You stand still as the fish swims its way toward you. Then, in one quick motion, you jab the harpoon into the water, piercing right through its flesh. You now have a DEAD FISH."
harpoon_event.add_receive(dead_fish)
harpoon_event.add_delete(fish)

golden_key_event = txt.Event(2, 0, 0, golden_key)
golden_key_event.message = "There is a book inside. You lift it up and open. It consists of numerous handwritten messages. You turn to the last page of the notebook with writing and read on: 'Add some message here about the dragon but it can't be cringe.'"
golden_key_event.add_delete(golden_key)

dead_fish_event = txt.Event(2, 1, 0, dead_fish)
dead_fish_event.message = "You drop the dead fish at the feet of the HOUND. He devours it ravenously and seemingly gives you a look of thankfullness. Finally, he gives a grunt and falls soundly asleep. The basement entrance is now unguarded and you can now go DOWN"
dead_fish_event.add_delete(dead_fish, hound)
dead_fish_event.add_reveal(sleeping_hound)
dead_fish_event.add_exit_change(garden, [F, F, F, T, F, T])

player = txt.Player(0, 0, 0)

#========================================
gui.start_engine()