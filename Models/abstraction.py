from abc import abstractmethod
import matplotlib.pyplot as plt

class Model():

    @abstractmethod
    def train(self, training_set, validation_set, show_loss, show_graph, save):
        raise NotImplementedError("This is an abstract method, implement this within the intended sub-class")

    @abstractmethod
    def save_model(self, model):
        raise NotImplementedError("This is an abstract method, implement this within the intended sub-class")
        
    @abstractmethod
    def predict(self, sequence):
        raise NotImplementedError("This is an abstract method, implement this within the intended sub-class")
        
    def accuracy(self, dataset, show_loss=False):
        correct_pred = 0
        total = 0
        
        for seq in dataset:
            sequence = self.predict(seq[0])
            for entity in sequence.ents:
                entities = seq[1]["entities"]
                ent, _, _, tag = zip(*entities)
                entities = zip(ent, tag)

                if (entity.text, entity.label_) in entities:
                    correct_pred += 1

                total += 1
        
        return correct_pred/total

    def show_training_graph(self, training, validation, best_score, test=None):
        X = [i for i in range(len(training))]

        plt.plot(X, training, label = "Training loss")
        plt.plot(X, validation, label = "Validation loss")
        plt.axvline(validation.index(best_score), 0, 1, label='Choosen model', color="red")

        if test != None:
            plt.plot(X, test, label = "Test loss")
            

        plt.xlabel('Number of predictions')
        plt.ylabel('Percent accurate predictions')
        plt.title('Trainingloss and Validationloss')
        
        # show a legend on the plot
        plt.legend()
        
        # function to show the plot
        plt.show()

    def evaluate(self, tokenizer, textcat, texts, cats, type_label):
        docs = (tokenizer(text) for text in texts)
        tp = 0.0  # True positives
        fp = 1e-8  # False positives
        fn = 1e-8  # False negatives
        tn = 0.0  # True negatives

        for i, doc in enumerate(textcat.pipe(docs)):
            gold = cats[i][type_label]

            if type_label == "entities":
                pred_entities = []
                
                for ent in doc.ents:
                    item = tuple([ent.text, ent.start_char, ent.end_char, ent.label_])
                    tp, fp, fn, tn = self._eval_ner(tp, fp, fn, tn, gold, item)
                    
                    pred_entities.append(item)
                
                missed_entities = list(filter(lambda x: x not in pred_entities, gold))
                fn += len(missed_entities)

            else:
                for label, score in doc.cats.items():
                    tp, fp, fn, tn = self._eval_topic(tp, fp, fn, tn, gold, label, score)

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)

        if (precision + recall) == 0:
            f_score = 0.0
        else:
            f_score = 2 * (precision * recall) / (precision + recall)

        return {"precision": precision, "recall": recall, "f_score": f_score}

    def _eval_topic(self, tp, fp, fn, tn, gold, label, score):
        if label not in gold:
            return
        if score >= 0.5 and gold[label] >= 0.5:
            tp += 1.0
        elif score >= 0.5 and gold[label] < 0.5:
            fp += 1.0
        elif score < 0.5 and gold[label] < 0.5:
            tn += 1
        elif score < 0.5 and gold[label] >= 0.5:
            fn += 1

        return tp, fp, fn, tn

    def _eval_ner(self, tp, fp, fn, tn, gold, item):
        """
        true positive is a correctly predicted entity
        true negative will not be used as that would indicate a predicted missing entity
        false positive is predicting a non existing entity
        false negative is missing a predicted entity which are actually in the set (although not tracked here)
        """

        if item in gold:
            tp += 1.0
        else:
            fp += 1

        return tp, fp, fn, tn

    def has_stagnated(self, data):
        if len(data) < 20:
            return False

        d = data[-20:]
        return self.help_stagnated(d)
        
    def help_stagnated(self, iterator):
        """
        Mean difference is lower than 1/1000
        """
        diff = 0
        for ind, el in enumerate(iterator):
            if ind == 0:
                continue
            else:
                diff += abs(iterator[ind - 1] - el)

        # Stop training when the mean of the last 15 results have less change than 1/1000
        return (diff / len(iterator)) < 0.001