
from Object import Object


class Weapon(Object):

    info = {
        "Bow": {
            "attack"
            "image": '🏹'
        }
    }

    def __init__(self):
        super().__init__()

    def get_info(self, reference):
        return self.info[reference["category"]]

    def get_image(self, reference):
        
        return self.get_info(reference)["image"]







