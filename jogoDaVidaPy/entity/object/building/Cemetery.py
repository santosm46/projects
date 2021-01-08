
from game.Board import Board
from utils.common import MOCK_ID
from game.DataStructure import DataStructure
from entity.object.building.Building import Building

class Cemetery(Building):
    
    def new_concrete_thing(self):

        cemetery = super().new_concrete_thing()
        self.update_concrete(cemetery)
        board : Board = self.get("Board")
        cemetery["id"] = MOCK_ID
        cemetery[self.attr_name] = "Cemitério"
        cemetery[self.attr_money] = 100
        # cemetery[self.attr_owner] = 10000000
        cemetery[self.attr_coord] = board.alphanum_to_coord("L15")
        self.update_subscriber(self.reference(cemetery["id"]))

        return cemetery

    def bury_being(self, being_ref):

        data : DataStructure = self.get("DataStructure")

        being = self.get_concrete_thing_by_ref(being_ref).copy()

        cemetery = self.get_concrete_thing(MOCK_ID)

        inv = 'inventory'
        if inv not in cemetery:
            cemetery[inv] = {}

        category = being_ref["category"]
        if category not in cemetery[inv]:
            cemetery[inv][category] = {}

        cemetery[inv][category][being_ref['id']] = being

        data.delete_concrete_thing(being_ref)

        

