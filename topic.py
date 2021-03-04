import pickle as pickle

class TopicClassifier():
    def __init__(self):
        self.dictionary = self.set_dictionary()

    def set_dictionary(self):
        with open('creation_of_dictionary/ordbokdata/ordbok/ordbok.pickle', 'rb') as handle:
            dictionary = pickle.load(handle)
        return dictionary

    def classify_topic(self, string):
        words = string.split(" ")
        match_count = dict(zip(self.dictionary.keys(), [0]*len(self.dictionary.keys())))
        for key, dictionary in self.dictionary.items():
            for word in words:
                if word in dictionary:
                    match_count[key] += 1
            match_count[key] /= len(dictionary)
        result = max(match_count, key=match_count.get)
        if match_count[result] == 0:
            result = "No class"
        return result
