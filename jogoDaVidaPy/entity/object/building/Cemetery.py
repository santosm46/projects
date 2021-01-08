
from game.DataStructure import DataStructure
from entity.object.building.Building import Building

class Cemetery(Building):
    

    def bury_being(self, being_ref):

        data : DataStructure = self.get("DataStructure")

        being = self.get_concrete_thing_by_ref(being_ref).copy()

        graves = self.get_dict_list()

        category = being_ref["category"]
        if category not in graves:
            graves[category] = {}

        graves[category][being_ref['id']] = being

        data.delete_concrete_thing(being_ref)

        

