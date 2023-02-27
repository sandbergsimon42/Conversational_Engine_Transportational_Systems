import json
import random

class Data():
    def __init__(self, filepath):
        self.train = []
        self.validation = []
        self.test = []

        # retrieve the data from a file.
        self.full_data = None
        self.get_data(filepath)
        self._example = None

    @property
    def example(self):
        """
        Get a random training sample form the training set
        """
        if self._example == None:
            indx = random.randint(0, len(self.training_set) - 1)
            self._example = self.training_set[indx]
            
        return self._example
    
    @property
    def training_set(self):
        return self.full_data[:int(len(self.full_data)*0.7)]
        
    @property
    def validation_set(self):
        return self.full_data[int(len(self.full_data)*0.7):int(len(self.full_data)*0.85)]
    
    @property
    def test_set(self):
        return self.full_data[int(len(self.full_data)*0.85):]

    def get_data(self, filepath):
        dialogues = []
        with open(filepath, "r") as f:
            for line in f:
                temp_dialogue = json.loads(line)
                sentence = temp_dialogue['dialogue'].lower()
                entities = list(map(lambda x: tuple(x), temp_dialogue['entities']))

                topics = {key: int(value) for (key, value) in temp_dialogue['cats']}
                dialogues.append((sentence, {"entities" : entities}, {"cats": topics}))
        
        self.full_data = dialogues