class DataContainer():
    def __init__(self, operator):

        self.start_of_sentence = [
            "request",
            "question"
        ]

        self.after_moving_entity = [
            "outbound",
            "inbound"
        ]

        self.end_of_sentence = []
        self.directions = ["south ", "north ", "west ", "east ", "sea ", "southeast ", "southwest ", "northeast", "northwest"]

        # Add alongside?
        self.moving_entity_intents = ["anchor away outbound ", "inbound "]
        self.filler_direction = ["for ", "to ", "towards ", "via ", "through ", " heading to ", "with direction for "]

        # Grammattiska regler som säger att en location_dependent måste ha en fast entity efter och en moving entitiy innan 
        self.location_dependent = [
            "at", 
            "near", 
            "approaching",
            "alongside",
            "close of",
            "passed",
            "passing",
            "around",
            "nearby",
            "close by",
            "in close proximity",
            "side by side"
        ]

        self.operator = operator

        # Dessa bör troligen vara dictionaries så går det hålla information om entities etc. (BÖR EJ VARA FOKUS JUST NU)
        self.moving_entities = ["svarte", "steel mover", "white horse queen", "fina båten", "fula båten"]
        self.moving_entities += self.get_data("./webscraped_entities/boat_names.txt")
        self.fixed_entities = self.get_data("./webscraped_entities/cities.txt")

        self.in_port_locations = ["fina fyren", "SAAB", "steel factory", "ABB", "fula fyren", "kränkan"]

    def get_data(self, filepath):
        res = None
        with open(filepath, "r") as f:
            for line in f:
                res = line.split(",")
                
        return res