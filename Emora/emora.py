
# CHECK THIS ONE OUT ON HOW TO INCLUDE STRUCTURES TO THE DIALOGUE GENERATION
# https://github.com/emora-chat/emora_stdm/blob/master/docs/NatexTutorial.md

from emora_stdm import NatexNLU, NatexNLG, Macro
from Models.NER_classification.spaCy_NER import NER_Classifier

model = NER_Classifier()
model.load_model("./Models/NER_classification/NER_Models/model")

doc_predictions = model.predict("HEHEHEHEHEH")

for ent in doc_predictions.ents:
    print(ent)

class EmoraBot():
    def __init__(self):
        pass

