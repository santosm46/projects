'''
This program simulates decision making with different strategies of 
ways to play the Cookie Clicker game, and displays the results of the 
total Cookies made by each one.

Link to the game: https://orteil.dashnet.org/cookieclicker/
'''

class Game:
    def __init__(self):
        # constants
        

        #variables
        self.cookiesInBank = 0
        self.cookiesBaked = 0
        self.buyer = Buyer(self)

class Buyer:
    def __init__(self, game):
        self.PRICE_INCREASE_RATE = 1.15 # increases 15% the building price after it's bought
        self.game = game
    
    # returns True if it bought, and False otherwise
    def buyBuilding(self, building):
        if(building.price > game.cookiesInBank):
            return False
        if(not building.unlocked):
            return False
        
        building.amount += 1
        game.cookiesInBank -= building.price
        building.price *= self.PRICE_INCREASE_RATE
        return True
        


class Building:
    def __init__(self, game, initialPrice, cookiePerSecond):
        self.game = game
        self.price = initialPrice
        self.cookiePerSecond = cookiePerSecond

        self.amount = 0
        self.unlocked = False #unlocks when cookies baked reaches the building price

