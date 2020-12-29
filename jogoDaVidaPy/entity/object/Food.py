
from entity.object.Object import Object


class Food(Object):


    def __init__(self):
        super().__init__()


    food_info = {
        "Hamburger": {
            "image": '🍔',
            "energy": 10,
            "price": 50,
            "health": -3
            
        },
        "Pizza": {
            "image": '🍕',
            "energy": 7,
            "price": 45,
            "health": -2
        },
        "Chicken": {
            "image": '🍗',
            "energy": 5,
            "price": 40,
            "health": -1
        },
        "Apple": {
            "image": '🍎',
            "energy": 2,
            "price": 25,
            "health": 1
        },
        "Mango": {
            "image": '🥭',
            "energy": 3,
            "price": 25,
            "health": 1
        },
        "Bone": {
            "image": '🦴',
            "energy": 0,
            "price": 10,
            "health": 0
        },
        "Avocado": {
            "image": '🥑',
            "energy": 3,
            "price": 30,
            "health": 4
        },
        "Cake": {
            "image": '🍰',
            "energy": 4,
            "price": 40,
            "health": -1
        },
    }
