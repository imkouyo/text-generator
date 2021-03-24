from nltk.tokenize import WhitespaceTokenizer
from nltk import bigrams
from collections import defaultdict, Counter
import re
import random


class CorpusLoad:
    def __init__(self, corpus_name):
        self.corpus = self.load(corpus_name)

    def load(self, corpus_file):
        with open(corpus_file, encoding="utf-8") as file:
            corpus_content = file.read()
        return corpus_content


class PreProcess:
    def __init__(self, corpus_content):
        self.wst = WhitespaceTokenizer()
        self.all_tokens = []
        self.unique_token = []
        self.bigrams_collection = []
        self.bigrams_dict = defaultdict(list)
        self.trigrams_collection = []
        self.trigrams_dict = defaultdict(list)
        self.tokenize(corpus_content)
        self.trigrams_collection_generator()
        self.markov_form(self.bigrams_collection, self.bigrams_dict)
        self.markov_form(self.trigrams_collection, self.trigrams_dict)

    def tokenize(self, corpus_content):
        self.all_tokens = self.wst.tokenize(corpus_content)
        self.unique_token = list(set(self.all_tokens))
        self.bigrams_collection = list(bigrams(self.all_tokens))

    def markov_form(self, collection, dictionary):
        for key, value in collection:
            dictionary[key].append(value)
        for key, value in dictionary.items():
            dictionary[key] = Counter(value)

    def trigrams_collection_generator(self):
        for i in range(len(self.all_tokens) - 2):
            self.trigrams_collection.append((" ".join([self.all_tokens[i], self.all_tokens[i + 1]]),
                                                  self.all_tokens[i + 2]))


class TextGenerator:
    def __init__(self, pre_process):
        self.pp = pre_process
        self.state = None

    def get_pseudo_sentence(self):
        while True:
            sentence = random.choice(self.pp.all_tokens)
            if re.match(r"^[A-Z]\w+$", sentence):
                self.state = 'start'
                return sentence

    def get_middle_sentnce(self, pre_word):
        while True:
            sentence = random.choices([key for key in self.pp.bigrams_dict[pre_word].keys()],
                                      weights=[value for value in self.pp.bigrams_dict[pre_word].values()])[0]
            if re.match(r"^[\w',]+$", sentence):
                self.state = 'center'
                return sentence

    def get_ending_sentence(self, pre_word):
        while True:
            sentence = random.choices([key for key in self.pp.bigrams_dict[pre_word].keys()],
                                      weights=[value for value in self.pp.bigrams_dict[pre_word].values()])[0]
            if re.match(r"^\w+[.!?]$", sentence):
                self.state = 'end'
                return sentence
            elif re.match(r"^\w+$", sentence):
                self.state = 'center'
                return sentence

    def get_tri_pseudo_sentence(self):
        while True:
            sentence = random.choice(self.pp.trigrams_collection)[0]
            if bool(re.match(r"^[A-Z]\w+\s\w+$", sentence)):
                return sentence

    def get_tri_end_sentence(self, pre_word, tmp):
        if len(self.pp.trigrams_dict[pre_word]) > 0:
            sentence = random.choices([key for key in self.pp.trigrams_dict[pre_word].keys()],
                                      weights=[value for value in self.pp.trigrams_dict[pre_word].values()])[0]
            if bool(re.match(r"^\w+[.!?]$", sentence)):
                if len(tmp) < 4:
                    tmp.pop()
                    pre_word = " ".join(tmp[-2:])
                    return self.get_tri_end_sentence(pre_word, tmp)
                else:
                    tmp.append(sentence)
                    return tmp
            elif bool(re.match(r"^[\w',]+$", sentence)):
                tmp.append(sentence)
                pre_word = " ".join([pre_word.split()[1], sentence])
                return self.get_tri_end_sentence(pre_word, tmp)
            else:
                return self.get_tri_end_sentence(pre_word, tmp)
        else:
            if len(tmp) > 2:
                tmp.pop()
                pre_word = " ".join(tmp[-2:])
                return self.get_tri_end_sentence(pre_word, tmp)
            else:
                pre_word = self.get_tri_pseudo_sentence()
                return self.get_tri_end_sentence(pre_word, pre_word.split())




def main(stage):
    # corpus = CorpusLoad('train_collection/corpus.txt')
    corpus = CorpusLoad(input())
    pre_process = PreProcess(corpus.corpus)
    text_generator = TextGenerator(pre_process)
    if stage == 1:
        print("Corpus statistics")
        print(f"All tokens: {len(pre_process.all_tokens)}")
        print(f"Unique tokens: {len(pre_process.unique_token)}")
        while True:
            command = input()
            if command == 'exit':
                break
            else:
                try:
                    print(pre_process.all_tokens[int(command)])
                except IndexError:
                    print("Index Error. Please input an integer that is in the range of the corpus.")
                except ValueError:
                    print("Type Error. Please input an integer.")
    elif stage == 2:
        print(f"Number of bigrams: {len(pre_process.bigrams_collection)}")
        while True:
            command = input()
            if command == 'exit':
                break
            else:
                try:
                    index = int(command)
                    print(f"Head: {pre_process.bigrams_collection[index][0]}  "
                          f"Tail: {pre_process.bigrams_collection[index][1]}.")
                except IndexError:
                    print("Index Error. Please input a value that is not greater than the number of all bigrams.")
                except (TypeError, ValueError):
                    print('typerror Type Error. Please input an integer.')
    elif stage == 3:
        while True:
            command = input()
            if command == 'exit':
                break
            else:
                try:
                    print(f"Head: {command}")
                    if len(pre_process.bigrams_dict[command]) > 0:
                        for key, value in pre_process.bigrams_dict[command].most_common():
                            print("Tail: {tail:<10}  Count: {count:<6}".format(tail=key, count=value))
                    else:
                        print("The requested word is not in the model. Please input another word.")
                except IndexError:
                    print("Index Error. Please input a value that is not greater than the number of all bigrams.")
                except (TypeError, ValueError):
                    print('typerror Type Error. Please input an integer.')
    elif stage == 4:
        word = random.choice(pre_process.all_tokens)
        for time_count in range(10):
            tmp = []
            for token_count in range(10):
                if len(pre_process.bigrams_dict[word]) > 0:
                    word = random.choices([key for key in pre_process.bigrams_dict[word].keys()],
                                          weights=[value for value in pre_process.bigrams_dict[word].values()])[0]
                    tmp.append(word)
            print(" ".join(tmp))
    elif stage == 5:
        for time_count in range(10):
            tmp = []
            word = text_generator.get_pseudo_sentence()
            tmp.append(word)
            for i in range(3):
                word = text_generator.get_middle_sentnce(word)
                tmp.append(word)
            while text_generator.state != 'end':
                word = text_generator.get_ending_sentence(word)
                tmp.append(word)
            print(" ".join(tmp))
    elif stage == 6:
        sentences = []
        while len(sentences) < 10:
            try:
                pre_word = text_generator.get_tri_pseudo_sentence()
                tokens = text_generator.get_tri_end_sentence(pre_word, pre_word.split())
                sentences.append(" ".join(tokens))
            except RecursionError:
                pass
        for sentence in sentences:
            print(sentence)


main(6)
