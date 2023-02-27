import random
import re

class Generator():
    def __init__(self, datacontainer, noise_generator):
        self.container = datacontainer
        self.data = []
        self.noise_generator = noise_generator
        self.turn = None
        self.entities = set()
        
        self.topic_categories = ["traffic information", "inbound", "outbound", "pilot required"]
        self.topic = None
        self.init_topic()

    def init_topic(self):
        self.topic = [0 for i in range(len(self.topic_categories))]

    def randomizer(self, upper_bound, lower_bound=0):
        return random.randint(lower_bound, upper_bound)

    def random_entity(self, entity):
        """
        Picks a random element from a list.
        """
        indx = self.randomizer(len(entity) - 1)
        return entity[indx]

    def new_turn(self):
        """
        Handle conversation turns.
        """
        self.turn += 1
        self.turn = 0 if self.turn % 2 == 0 else self.turn

    def handshake(self, operator, entity):
        """
        A handshake is the first communication between a vessel
        and the operator.
        """
        self.add_entities([(operator, "COM")])
        entities = [operator, entity]
        start = entities[self.turn] + " " + entities[(self.turn + 1) % 2]
        
        # Some respond on initial communication with replying instead of identifying the operator
        if self.turn % 2 == 0 and self.randomizer(10) >= 8:
            response = entities[(self.turn + 1) % 2] + " replying"
        else:
            response = entities[(self.turn + 1) % 2] + " " + entities[self.turn]
        
        return [start, response]
   
    def get_labels(self, sentences, entities):
        #Handles finding the label start index and which tag it have.
        entities, tags = zip(*entities)
        labels = []

        for indx, entity in enumerate(entities):

            if entity[-1] == " ":
                entity = entity[:-1]

            for match in re.finditer(entity.lower(),sentences.lower()):
                
                # Control that the same start and end is not within the label list yet. (which would give overlapping entities)
                prev_added = len(list(filter(lambda x: match.start() == x[1] or match.end() == x[2], labels))) > 0
                
                if not prev_added:
                    labels.append(tuple((match.group(0), match.start(), match.end(), tags[indx])))

        labels = self.check_overlap(labels)
        return labels

    def check_overlap(self, labels):
        labs = []
        """
        sort the array on start items
        if the start is more than the end i can stop the search
        """
        sorted_labels = sorted(labels, key=lambda x: x[0])
        for indx, element in enumerate(sorted_labels):
            _, prim_start, prim_end, _ = element
            add = True
            for label_index in range(indx, len(sorted_labels)):

                control_start = sorted_labels[label_index][1]
                control_end = sorted_labels[label_index][2]

                if prim_start > control_end:
                    # No need to check rest since it's a sorted array
                    continue
                
                if prim_start < control_start and control_start < prim_end < control_end \
                    or prim_start < control_start < prim_end:

                    add = False
                    continue

            if add:
                labs.append(element)

        return labs

    def add_entities(self, entities):
        # entities is a list

        for entity in entities:
            self.entities.add(entity)

    def add_intent(self, entity):
        """
        Builds the initial intent sentence.
        """
        intent = ""
        origin_intent = None
        proximity = None
        pilot_required = "pilot required "

        if self.turn % 2 == 1:
            # The vessel handler have done the first request and must first declare intent
            if self.randomizer(10) >= 8:
                approximation = self.random_entity(self.container.location_dependent)
                location = self.random_entity(self.container.in_port_locations)
                origin_intent = entity + " " + approximation + " " + location + " " 
                intent = origin_intent
                self.add_entities([(location, "IPL")])
                self.topic[0] = 1

            else:
                # This builds intent from the intentlist within the datacontainer
                origin_intent = self.random_entity(self.container.moving_entity_intents) + self.random_entity(self.container.filler_direction)
                direction = self.random_entity(self.container.directions)
                origin_intent += direction
                
                if "inbound" in origin_intent:
                    self.topic[1] = 1
                else:
                    self.topic[2] = 1

                if self.randomizer(10) >= 7:
                    another_direction = self.random_entity(self.container.directions)
                    while another_direction == direction:
                        another_direction = self.random_entity(self.container.directions)
                        
                    origin_intent += " and " + self.random_entity(["then ", "then to the ", "towards ", ""]) + another_direction

                # Build the parts and randomize the parts of the sentence
                if self.randomizer(10) >= 4:
                    # Is not close to an fixed entity 4/10 times
                    approximation = self.random_entity(self.container.location_dependent)
                    location = self.random_entity(self.container.in_port_locations)

                    proximity = " " + approximation + " " + location + " "
                    self.add_entities([(location, "IPL")])

                if "outbound" in origin_intent:
                    pilot_required = "pilot onboard " 
                

                if self.randomizer(10) >= 7:
                    # 7/10 cases it needs pilot
                    pilot_required = "no " + pilot_required
                
                # Add correct label regarding pilot information
                if ("no" in pilot_required and "onboard" in pilot_required) or \
                    ("no" not in pilot_required and "required" in pilot_required):
                    self.topic[3] = 1

                        
                # Build which order the sentence will hold
                if self.randomizer(10) >= 6:
                    # 6/10 will the pilot announcment be first the rest it will be last
                    intent = pilot_required.capitalize() + origin_intent
                    intent = intent + proximity if proximity != None else intent
                else:
                    intent = origin_intent.capitalize() + proximity if proximity != None else origin_intent.capitalize()
                    intent += pilot_required

            self.add_entities([(entity, "COM")])

        else:
            start_of_sequence = self.random_entity(["I can see you ", "You are ", "", "I see you "])
            approximation = self.random_entity(self.container.location_dependent) + " "

            if self.randomizer(10) >= 5:
                location = self.random_entity(self.container.fixed_entities) + " "
                self.add_entities([(location, "GPE"), (entity, "COM")])
            else:
                location = self.random_entity(self.container.in_port_locations) + " "
                self.add_entities([(location, "IPL"), (entity, "COM")])

            origin_intent = approximation
            intent =  start_of_sequence + approximation + location
            self.topic[0] = 1

            # Ugly hack to keep the correct turn sequence as this funciton is called right after the returned value
            self.new_turn()

        return [origin_intent, intent]
    
    def info_about_vessels(self, intent, entity, nearby_entities):
        #FIRST RESPOND TO INTENT AND TO THE IDENTIFIED ENTITTY  

        # Randomize how many nearby entities there are
        add_nearby_entities = self.randomizer(lower_bound=1, upper_bound=5)
        told_entities = [entity] + nearby_entities    # This is the entity we are currently talking to.

        """
        This could be changed to hold all entities within a range 
        of the harbour but this requires further development of 
        entity class and moving entities as in setting positions
        at the start of each dialogue to see which entities are in 
        X range of the harbour.
        """
        count = len(self.container.moving_entities) - len(told_entities)
        current_entity = self.random_entity(self.container.moving_entities)

        while current_entity in told_entities:
            current_entity = self.random_entity(self.container.moving_entities)

        while current_entity not in told_entities and count > 0 and add_nearby_entities > 0:
            told_entities.append(current_entity)
            count -= 1
            add_nearby_entities -= 1

            current_entity = self.random_entity(self.container.moving_entities)
            # Find another entity which have not been reported yet
            while current_entity in told_entities and count > 0: 
                current_entity = self.random_entity(self.container.moving_entities)
        
        # Filter out the main vessel
        nearby_entities = told_entities[len(nearby_entities) + 1:]
        random.shuffle(nearby_entities)

        begining_of_sentence = ["You have ", "There is "]
        sent = self.random_entity(begining_of_sentence)
        current_sent = ""
        for indx, ent in enumerate(nearby_entities):
            if self.randomizer(1) == 1:
                if self.randomizer(1) == 1:
                    location = self.random_entity(self.container.fixed_entities)
                    self.add_entities([(location, "GPE")])
                else:
                    location = self.random_entity(self.container.directions)

                self.add_entities([(ent, "COM")])

                # 50/50 how the randomization is falling out
                current_sent += ent + " " + self.random_entity(self.container.moving_entity_intents) + \
                                self.random_entity(self.container.filler_direction) + location 
            else:
                direction = self.random_entity(self.container.after_moving_entity)
                approximation = self.random_entity(self.container.location_dependent)
                location = self.random_entity(self.container.in_port_locations)

                self.add_entities([(location, "IPL"), (ent, "COM")])

                current_sent += direction + " vessel " + ent + " " + approximation + " " + location
            
            if self.randomizer(1) == 1 and indx != len(nearby_entities) - 1:
                current_sent += self.random_entity([" and ", " also "])
                
            else:
                current_sent += ". "
                sent += current_sent
                current_sent = ""

        return [nearby_entities, sent]

    def intent_response(self, vessel_information):
        ending = ["thank you", "Repeat, ", "understood", "noted"]
        s = ""

        if self.randomizer(10) >= 4:
            outbounds = 0
            inbounds = 0
            for sentence in vessel_information.split("."):
                if "outbound" in sentence:
                    outbounds += 1
                elif "inbound" in sentence:
                    inbounds += 1
            
            if self.randomizer(10) >= 7:
                s += f"{outbounds + inbounds} {'vessel' if outbounds + inbounds == 1 else 'vessels'} nearby"
            else:
                if outbounds > 0:
                    s += f"{outbounds} {'vessel' if outbounds == 1 else 'vessels'} outbound"
                
                if inbounds > 0:
                    if len(s) != 0:
                        s += " and "
                    s += f"{inbounds} {'vessel' if inbounds == 1 else 'vessels'} inbound"

        if len(s) == 0:
            s += self.random_entity(ending[1:]) + " " + ending[0]
        else:
            end = self.random_entity(ending)
            while "Repeat" in end:
                end = self.random_entity(ending)
                
            s += " " + end  + " . "

        return s

    def format_topics(self):
        res = []
        for topic in self.topic:
            res.append(bool(topic))

        return list(zip(self.topic_categories, res))

    def generate_dialogue(self):
        """
        Generate a full dialogue sequence, from first handshake to dialogue ending.
        """
        dialogue = []

        # The entity which are the target for this dialogue sequence
        dialogue_entity = self.random_entity(self.container.moving_entities)

        # Deciding who's turn it is (assuming one part is always waiting for response)
        self.turn = self.randomizer(1)
        
        # Initial handshake 
        dialogue += self.handshake(self.container.operator, dialogue_entity)

        # Add the intent of the conversation which will be found within 
        # the response after the initial handshake
        intent, intent_sentence = self.add_intent(dialogue_entity)
        intent_sentence = self.noise_generator.add_noise(intent_sentence)
        dialogue.append(intent_sentence)
    
        self.new_turn()

        # Response regarding the information of vessels which are relevant to the
        # entity which holds the communication
        nearby, vessel_sentences = self.info_about_vessels(intent, dialogue_entity, [])
        vessel_sentences = self.noise_generator.add_noise(vessel_sentences)
        dialogue.append(vessel_sentences)

        self.new_turn()

        # Randomisering om det ska till mer informaion om nearby
        response = self.intent_response(vessel_sentences)
        response = self.noise_generator.add_noise(response)
        while "Repeat" in response:
            dialogue.append(response)
            dialogue.append(vessel_sentences)
            response = self.intent_response(vessel_sentences)
            response = self.noise_generator.add_noise(response)

        dialogue.append(response)

        self.new_turn()

        # Further information can be added if there's more moving entities than previously
        # added.
        if len(nearby) < len(self.container.moving_entities):
            if self.randomizer(10) >= 8:
                # 3/10 case add more vessel information
                new_nearby, new_vessel_sentences = self.info_about_vessels(intent, dialogue_entity, nearby)
                new_vessel_sentences = self.noise_generator.add_noise(new_vessel_sentences)
                dialogue.append(new_vessel_sentences)
                
                response = self.intent_response(vessel_sentences + new_vessel_sentences)
                response = self.noise_generator.add_noise(response)

                repeated = False
                while "Repeat" in response:
                    repeated = True
                    response = self.intent_response(vessel_sentences + new_vessel_sentences)
                    response = self.noise_generator.add_noise(response)
                    dialogue.append(response)
                
                if not repeated:
                    dialogue.append(response)

        entities = list(self.entities)
        sentences = " ".join(dialogue)
        labels = self.get_labels(sentences, entities)
        topics = self.format_topics()

        self.entities = set()
        self.init_topic()
        return (sentences, labels, topics)