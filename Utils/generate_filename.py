import random
from typing import Union

# _funny_nouns = [ # AI generated examples
#     "Pickle", "Bubble", "Waffle", "Goblin", "Noodle", "Toaster", "Gargoyle", "Squid",
#     "Blob", "Doodle", "Hobgoblin", "Cupcake", "Llama", "Meatball", "Donut", "Turnip",
#     "Sprout", "Unicorn", "Taco", "Sloth", "Gnome", "Cheeseburger", "Whisker", "Omelet",
#     "Giraffe", "Popsicle", "Marshmallow", "Penguin", "Slipper", "Butterscotch", "Lobster",
#     "Squirt", "Cupboard", "Gumbo", "Squeegee", "Spatula", "Muffin", "Toothpick", "Yeti",
#     "Narwhal", "Snorkel", "Rutabaga", "Jellybean", "Sausage", "Hobbit", "Banana", "Monkey",
#     "Biscuit", "Mongoose", "Cactus", "Crumpet", "Dingbat", "Moose", "Squirrel", "Rascal",
#     "Whippersnapper", "Stinkbug", "Zebra", "Badger", "Hippo", "Chewbacca", "Blubber", 
#     "Skunk", "Beetle", "Pickleball", "Octopus", "Jellyfish", "Eggplant", "Wombat", 
#     "Marmalade", "Squash", "Snowflake", "Snicker", "Fluff", "Dumpling", "Chinchilla", 
#     "Cabbage", "Grapefruit", "Gummy", "Chuckle", "Rasberry", "Cuddle", "Booger", "Fart", 
#     "Mongoose", "Cupcake", "Troll", "Slinky", "Nugget", "Bloop", "Munchkin", "Sprinkle", 
#     "Crouton", "Kumquat", "Goober", "Whisk", "Zucchini", "Raspberry", "Bumblebee", 
#     "Fiddle", "Glitter", "Gloop", "Hodgepodge", "Doodle", "Spork", "Nugget", "Giblet"
# ]

# _funny_adjectives = [ # AI-generated examples
#     "Weird", "Wobbling", "Jiggling", "Sneezing", "Burping", "Hopping", "Scooting", 
#     "Sputtering", "Slurping", "Snorting", "Squirming", "Hiccuping", "Doodling", "Fumbling", 
#     "Giggling", "Yodeling", "Flapping", "Gobbling", "Squawking", "Guzzling", "Whistling", 
#     "Cackling", "Flopping", "Chomping", "Gurgling", "Skittering", "Slinking", "Clucking", 
#     "Puffing", "Twisting", "Twitching", "Mumbling", "Muttering", "Sniffling", "Grumbling", 
#     "Drooling", "Lurking", "Flickering", "Shrieking", "Prancing", "Squeaking", "Yawning", 
#     "Stumbling", "Snuggling", "Chirping", "Quacking", "Rambling", "Zooming", "Hobbling", 
#     "Buzzing", "Tickling", "Munching", "Galloping", "Scrambling", "Squabbling", "Bumbling", 
#     "Scurrying", "Sputtering", "Blubbering", "Rumbling", "Putty", "Clambering", "Dabbing", 
#     "Swooning", "Scampering", "Prattling", "Skedaddling", "Flailing", "Sputtering", 
#     "Whisking", "Babbling", "Cavorting", "Distinct", "Hollering", "Gallivanting", 
#     "Waddling", "Wheezy", "Annoying", "Preppy", "Chirpy", "Twisty", "Slinky", 
#     "Frolicsome", "Shimmery", "Glimmery", "Jiggly", "Quivery", "Swooshy", "Crawly", 
#     "Floppy", "Gurgly", "Grumbly", "Bumbly", "Stumbly", "Yodely", "Blithering", 
#     "Quacky", "Fluttery", "Whirly", "Zoomy", "Skittery", "Hooty", "Bumbly", "Glittery"
# ]

_funny_nouns = [
    "Person", "Weirdo", "Doggy", "Cat", "Cactus", "Worm", "Appendage", "Gumbo", 
    "Gnome", "Goblin", "Gremlin", "Ghoul", "Vato", "Sticker", "Gobbldeygook",
    "Bozo", "Girlfriend", "Testimony", "Lawyer", "Accountant", "Charizard", 
    "Monster", "Critter", "Creature", "Primo", "Bufanda", "Empanada", "Sellout",
    "Salesperson", "Spokesman", "Impala", "Pigeon"
]

_funny_adjectives = [
    "Sweating", "Worrying", "Weird", "Extreme", "Lying", "Snorting", "Snoring",
    "Snotty", "Obnoxious", "Anxious", "Ambitious", "Greedy", "Sweaty", "Unwashed", 
    "Rich", "Wild", "Tame", "QR"
]

def generate_fun_filename(extension: Union[str, None]) -> str:
    """Generates a funny file name. NOTE: 'extension' should not include the '.'
    For example, 'pdf' is accetable, but not '.pdf'
    """
    noun = _funny_nouns[random.randrange(len(_funny_nouns))]
    gerund = _funny_adjectives[random.randrange(len(_funny_adjectives))]
    if extension:
        return f'{gerund}{noun}.{extension}'
    return f'{gerund}{noun}'
