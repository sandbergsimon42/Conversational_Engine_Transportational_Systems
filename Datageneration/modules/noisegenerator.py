import os
import random

class NoiseGenerator():
    def __init__(self, alike_word_probability=0.1, full_random_probability=0.05):
        self.alike_probability = alike_word_probability
        self.full_random_probability = full_random_probability
        self.noise_choices = {}
        self.read_corpus()

    def add_noise(self, sentence, show_changes=False):
        # Default probability that a word is wrong: 5% of the words will be changed.
        sentence_split = sentence.split(" ")
        for indx, word in enumerate(sentence_split):
            # Check that the word is available in the noise dicitonary
            if self.noise_choices.get(word, None) == None:
                continue
            
            if random.randint(0, 100) <= self.full_random_probability * 100:
                random_word_indx = random.randint(0, len(self.noise_choices) - 1)
                random_word = list(self.noise_choices.keys())[random_word_indx]
                if show_changes:
                    print(f"FULLY RANDOMIZED NEW WORD, CHANGED {sentence_split[indx]} TO {random_word}")
                    
                sentence_split[indx] = random_word
        

            # Randomize based on the probability
            elif random.randint(0, 100) <= self.alike_probability * 100:
                # replace the word in the sentence
                random_word_indx = random.randint(0, len(self.noise_choices[word]) - 1)
                if show_changes:
                    print(f"ALIKE RANDOMIZED NEW WORD, CHANGED {sentence_split[indx]} TO {self.noise_choices[word][random_word_indx]}")

                sentence_split[indx] = self.noise_choices[word][random_word_indx]
        
        return " ".join(sentence_split)

    def read_corpus(self):
        # Move into the coca corpus map
        path = os.getcwd().split("/")
        if "EWT" not in path:
            path.append("EWT")
        
        os.chdir("/".join(path))
        files = os.listdir()

        # Add all the different words to the word_set
        word_set = []
        for f in files:
            with open(f, "r") as open_file:
                for line in open_file:
                    if not line.startswith('#'):  # Skip lines with comments
                        line = line.rstrip()
                        if line:
                            columns = line.split('\t')
                            if columns[0].isdigit():  # Skip range tokens
                                # Only adding the word
                                if columns[1].lower().isalpha():
                                    word_set.append(columns[1].lower())
        
        word_set = list(set(word_set))
        
        # Find alike words which are grammatically similar, as only one character will be different
        # This will mostly favor short words as it's less probability they differ by more than 1 char.

        count = 0
        alike_words = {}
        for indx, word in enumerate(word_set):
            if len(word) == 1:
                continue

            for compare_index in range(len(word_set)):
                if len(word) != len(word_set[compare_index]):
                    continue
                
                difference_count = 0
                for char_indx, _ in enumerate(word):
                    if word_set[compare_index][char_indx] != word[char_indx]:
                        difference_count += 1
                
                    if difference_count > 1:
                        break
                
                if difference_count == 1:
                    if alike_words.get(word, None) == None:
                        alike_words[word] = [word_set[compare_index]]
                    else:
                        alike_words[word].append(word_set[compare_index])
                    
                    # Count how many times this occur over the dataset
                    count += 1
        
        # Return to original map
        os.chdir("/".join(path[:-1]))

        self.noise_choices = alike_words
        return alike_words