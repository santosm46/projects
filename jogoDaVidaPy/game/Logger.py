
from utils.common import MOCK_ID
from game.Event import Event
from game.Game import Game
from utils.beauty_print import bcolors


# logs messages of events before printing board

class Logger(Game):

    def __init__(self):
        super().__init__()
        self.messages_buffer = []
    
    def set_factory(self, factory):
        super().set_factory(factory)
        e : Event = self.get("Event")
        # e.subscribe("building_board_print", self.reference(MOCK_ID), "dump")
    

    def dump(self, interested=None, event_causer=None, additional=None):
        for m in self.messages_buffer:
            print(m)
        self.messages_buffer.clear()
        
    
    def add(self, message, color=bcolors.ENDC):
        message = f"{color}{message}{bcolors.ENDC}"
        self.messages_buffer.append(message)


