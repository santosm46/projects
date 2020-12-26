from Entity import Entity


class LivingBeing(Entity):

    def __init__(self):
        self.MAX_HP = 5
        super().__init__()


    def new_concrete_thing(self):
        concrete = super().new_concrete_thing()

        concrete["hp"] = self.MAX_HP
        concrete["max_hp"] = self.MAX_HP
        concrete["dice_method"] = "DiceRandom"


        return concrete
    
    



