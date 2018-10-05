import gamelib
import random
import math
import warnings
from sys import maxsize



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

        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.build_defences(game_state)
        self.deploy_attackers(game_state)

        game_state.submit_turn()

		




    def build_defences(self, game_state):
        """
        plaziert immer destructors in den Ecken,oben wenn es geht
        """
        firewall_locations = [[3, 13], [24, 13]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        """
	am linken Rand 2 encryptors um die information zu buffen
        """
        firewall_locations = [[3, 10], [2, 11]]
        for location in firewall_locations:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        """
	all_locations beinhaltet Plaetze auf unserer Seite
        """
        all_locations = []
        for i in range(game_state.ARENA_SIZE):
            for j in range(math.floor(game_state.ARENA_SIZE / 2)):
                if (game_state.game_map.in_arena_bounds([i, j])):
                    all_locations.append([i, j])
        
        """
        possible_locations ist all_locations ohne die schon besetzten Plaetze
        """
        possible_locations = self.filter_blocked_locations(all_locations, game_state)
		
		
        """
        für ein destructor mit wall davor gedacht
        """
        possible_locations_v01prebuilt = self.filter_blocked_locations(all_locations, game_state)

        """
        baut destructors and random positionen ohne den Weg zum Angriff
        """
        while game_state.get_resource(game_state.CORES) >= game_state.type_cost(DESTRUCTOR) and len(possible_locations) > 0:
            for i in range(0,13):
                if [i,13-i] in possible_locations:
                    possible_locations.remove([i,13-i])
            for i in range(1,14):
                if [i,14-i] in possible_locations:
                    possible_locations.remove([i,14-i])
            
            location_index = random.randint(0, len(possible_locations) - 1)
            build_location = possible_locations[location_index]
            """
            Build it and remove the location since you can't place two 
            firewalls in the same location.
            """
            game_state.attempt_spawn(DESTRUCTOR, build_location)
            possible_locations.remove(build_location)

    def deploy_attackers(self, game_state):
        """
	macht nichts bis BITS > 10
        """
        if (game_state.get_resource(game_state.BITS) < 10):
            return
        
        """
        10 pings in [14,0]
        """
        if game_state.can_spawn(EMP, [14, 0], 10):
        	game_state.attempt_spawn(EMP, [14, 0], 10)

 
        """
        NOTE: the locations we used above to spawn information units may become 
        blocked by our own firewalls. We'll leave it to you to fix that issue 
        yourselves.

        Lastly lets send out Scramblers to help destroy enemy information units.
        A complex algo would predict where the enemy is going to send units and 
        develop its strategy around that. But this algo is simple so lets just 
        send out scramblers in random locations and hope for the best.

        Firstly information units can only deploy on our edges. So lets get a 
        list of those locations.
        """
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        """
        Remove locations that are blocked by our own firewalls since we can't 
        deploy units there.
        """
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
