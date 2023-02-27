import spacy
import random
from spacy.util import minibatch
from spacy.training import Example
from pathlib import Path
import copy

from ..abstraction import Model

class NER_Classifier(Model):
    def __init__(self):
        self.model = spacy.load('en_core_web_md')

    def predict(self, sequence):
        return self.model(sequence)

    def add_entities(self, entities):
        ner = self.model.get_pipe("ner")

        for _, annotations, _ in entities:
            for ent in annotations.get("entities"):
                ner.add_label(ent[3])
        
    def train(self, dataset, validation, show_loss=False, show_graph=False, save=False):
        # Disable pipeline components which dont need to change
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        unaffected_pipes = [pipe for pipe in self.model.pipe_names if pipe not in pipe_exceptions]
        
        # Keep track of the best accuracies on the validationscore
        best_model = (None, -1)
        training_loss = []
        validation_loss = []
        stop_training = False

        ner = self.model.get_pipe("ner")
            
        with self.model.disable_pipes(*unaffected_pipes):
            for _ in range(30):
                if stop_training:
                    break

                # List of trainingexamples
                random.shuffle(dataset)

                training_examples = []
                for text, annotation, _ in dataset:
                    doc = self.model.make_doc(text)
                    try:
                        annotations = {"entities": list(map(lambda x: tuple(x[1:]), annotation['entities']))}
                        training_examples.append(Example.from_dict(doc, annotations))
                    except ValueError:
                        continue

                # shuffling examples before every iteration
                losses = {}

                # batch up the examples 
                batches = minibatch(training_examples, size=8)
                dataset_batches = list(minibatch(dataset, size=8))

                for indx, batch in enumerate(batches):
                    self.model.update(
                                batch,
                                drop=0.5,  # dropout - make it harder to memorise data
                                losses=losses,
                            )

                    
                    # If score is wanted for each batch
                    batch_score = self.evaluate(self.model.tokenizer, ner, [val[0] for val in dataset_batches[indx]], 
                                                                    [val[1] for val in dataset_batches[indx] ], "entities")
                    
                    scores = self.evaluate(self.model.tokenizer, ner, [val[0] for val in validation], 
                                                                    [val[1] for val in validation ], "entities")

                    prec = scores['f_score']
                    if prec > best_model[1]:
                        if save:
                            best_model = [copy.deepcopy(self.model), prec]
                        else:
                            best_model = [None, prec]

                    training_loss.append(batch_score['f_score'])
                    validation_loss.append(scores['f_score'])

                    if self.has_stagnated(training_loss) and self.has_stagnated(validation_loss):
                        stop_training = True
                        break

                if show_loss:
                    print("Loss in iteration", batch_score['f_score'])

                print(" Best accuracy on the validationset was: ", best_model[1])

        if save:
            self.save_model(best_model[0])

        if show_graph:
            self.show_training_graph(training_loss, validation_loss, best_model[1])

    def save_model(self, model):
        model.to_disk('./Models/NER_classification/NER_Models/model')

    def load_model(self, path):
        self.model = spacy.load(path)