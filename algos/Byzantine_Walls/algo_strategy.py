import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replcement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    """
    def starter_strategy(self, game_state):
        """
        The triple staged build up of our walls.
        """
        self.the_walls(game_state)
        """
        Finally deploy our information units to attack.
        """
        self.deploy_attackers(game_state)

    def the_walls(self, game_state):
        """
        Stage 1: A basic tunnel with four open gates is created.
        """
        firewall_locations = [[0,13],[1,13],[2,13],[4,13],[9,13],[10,13],[11,13],[16,13],[17,13],[18,13],[23,13],[15,13],[27,13]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
                
        destructor_locations = [[3,13],[10,12],[17,12],[24,13]]
        for location in destructor_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        """
        Stage 2: The destructor count is stocked up in order to prevent multi emp attack.
        """

        destructor_locations = [[9,12],[18,12],[4,12],[23,12]]
        for location in destructor_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
				
        firewall_locations = [[26,13],[8,13],[19,13],[5,12],[22,12]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
				
        """
        Stage 3: The walls get extended in order to keep Ping-thunelling strategies out.
        """
				
        destructor_locations = [[11,12],[16,12]]
        for location in destructor_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
				
        firewall_locations = [[12,13],[15,13],[19,12],[8,12],[13,11],[14,11],[6,11],[21,11],[7,10],[20,10],[9,11],[18,11],[10,10],[17,10],[8,9],[19,9],[9,8],[18,8]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

    def deploy_attackers(self, game_state):
        """
        First lets check if we have 12 bits, if we don't we lets wait for 
        a turn where we do.
        """
		
        if game_state.get_resource(game_state.BITS) >= 12:
            game_state.attempt_spawn(EMP,[17,3],4)

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
