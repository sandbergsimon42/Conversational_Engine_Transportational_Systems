from ..abstraction import Model
from spacy.training import Example
from spacy.util import minibatch
import spacy
import random
import copy

class Topic_Classification(Model):
    def __init__(self, labels):
        self.model = spacy.blank('en')
        self.model.add_pipe("textcat_multilabel")
        
        textcat = self.model.get_pipe("textcat_multilabel")
        # Initialize the labes which are available
        for label in labels:
            textcat.add_label(label)

    def predict(self, sequence):
        textcat_multilabel = self.model.get_pipe("textcat_multilabel")
        test = list(self.model.pipe([sequence]))
        return textcat_multilabel.predict(test)

    def train(self, dataset, validation, show_loss=False, show_graph=False, save=False):
        
        # Keep track of the best accuracies on the validationscore
        best_model = (None, -1)

        training_examples = []
        for text, _, annotation in dataset:
            doc = self.model.make_doc(text)
            training_examples.append(Example.from_dict(doc, annotation))
            
        # Initialize the text categorizer
        textcat = self.model.get_pipe("textcat_multilabel")
        optimizer = self.model.initialize(lambda: training_examples)

        training_loss = []
        validation_loss = []
        stop_training = False
        
        epochs = 10
        for _ in range(epochs):

            if stop_training:
                break

            # shuffling examples before every iteration
            random.shuffle(dataset)

            # List of trainingexamples
            training_examples = []
            for text, _, annotation in dataset:
                doc = self.model.make_doc(text)
                training_examples.append(Example.from_dict(doc, annotation))
            
            # batch up the examples 
            batches = minibatch(training_examples, size=8)
            dataset_batches = list(minibatch(dataset, size=8))

            for bc, batch in enumerate(batches):
                self.model.update(
                            batch,
                            drop=0.5,  # dropout - make it harder to memorise data
                            sgd=optimizer
                        )
                
                scores = self.evaluate(self.model.tokenizer, textcat, [val[0] for val in validation], 
                                                                        [val[2] for val in validation ], "cats")

                batch_score = self.evaluate(self.model.tokenizer, textcat, [val[0] for val in dataset_batches[bc]],
                                                                [val[2] for val in dataset_batches[bc] ], "cats")

                training_loss.append(batch_score['f_score'])
                validation_loss.append(scores["f_score"])

                if show_loss:
                    print("Trainingloss: ", batch_score['f_score'], " Validationloss: ", scores['f_score'])

                # If it's the best performing model until now, save the model to use the best one.
                if scores["f_score"] >= best_model[1]:
                    best_model = [copy.deepcopy(self.model), scores["f_score"]]
                
                if self.has_stagnated(training_loss) and self.has_stagnated(validation_loss):
                    stop_training = True
                    break
            
        print(" Best accuracy on the validationset was: ", best_model[1])

        if save:
            self.save_model(best_model[0])

        if show_graph:
            self.show_training_graph(list(map(lambda el: el, training_loss)), validation_loss, best_model[1])

    def save_model(self, model):
        model.to_disk('./Models/Topic_classification/Topic_Models/model')
    
    def load_model(self, path):
        self.model = spacy.load(path)