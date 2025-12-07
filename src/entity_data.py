# This dictionary maps item IDs to their respective names, descriptions, sprite, and other metadata.

FOOD_DATA = {
    0: {"name": "Croissant", "description": "fr*nch", "sprite": "croissant.png", "cost": 3, "nutrition_value": 15, "is_bouncy": False},
    1: {"name": "Energy Drink", "description": "monter...", "sprite": "energy_drink.png", "cost": 4, "nutrition_value": 5, "is_bouncy": False},
    2: {"name": "Cup Noodles", "description": "they put noodles in a cup this is unbelievaaable.", "sprite": "cup_noodles.png", "cost": 2, "nutrition_value": 20, "is_bouncy": False},
    3: {"name": "Worm", "description": "webfishing whaoaoahh", "sprite": "worm.png", "cost": 5, "nutrition_value": 10, "is_bouncy": False},
}

TOY_DATA = {
    4: {"name": "Bouncy Ball", "description": "i got this sprite from google images lol", "sprite": "bouncyball.png", "cost": 10, "fun_value": 25, "is_bouncy": True},
}

INVENTORY_DATA = { #Not yet in use
    "food": {0:0, 1:0, 2:0, 3:0},  # Dictionary of food item IDs and their quantities
    "toy": {4:0}          # Dictionary of toy item IDs and their quantities
}