import riddles
import protocols
import asyncio
#import lobby
# Peut-être pas
#import json

class Game:
       
    def __init__(self):
        self.players = [
             {'nickname': "Pomme", 'role': "past", 'current_room': 1},
             {'nickname': "DeTerre", 'role': "futur", 'current_room': 1}
        ]
        self.riddles = { 'water_riddle': WaterRiddle(),
                        'light_riddle': LightRiddle(),
                        'bomb_riddle': BombRiddle(),
                        'music_riddle': MusicRiddle(),
                        'clozetest_riddle': ClozeTestRiddle(),
                        'battle_race': BattleRace()
                        }
        # Constant and limit for gameplay
        self.NUMBER_OF_ROOMS = 5
        
    async def run_game(self, game_id, players):
         await self.riddles['water_riddle'].start(game_id, self)
         # If one player has room_validated True, current_room+1


    class WaterRiddle:
          
        def __init__(self):
                # Get the players and the number of rooms
                super().__init__()
                self.valve_closed = False
                self.water_evaporated = False
                self.door_opened_up = False
                self.door_opened_right = False
                self.door_opened_down = False

        
        async def start(self, game_id, game):
               pass
        
        
              


        

        