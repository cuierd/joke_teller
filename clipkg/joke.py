import time
from typing import List, Tuple
import re
import random
import csv
from pkg_resources import resource_filename


class Joke:
    """The Joke object contains the joke, and some metadata on that joke. One can compare the jokes by upvotes"""
    def __init__(self, raw_joke):
        self.raw_joke = raw_joke
        self.author = self.raw_joke[0]
        self.link = self.raw_joke[1]
        self.joke = self.raw_joke[2]
        self.rating = int(self.raw_joke[3])
        self.time = self.raw_joke[4]

        self.sentences_joke = self.split_into_sentences()
        self.tokenized_joke = self._tokenize()
        self.filtered_joke = self.filter_profanity()[0]
        self.num_profanities = self.filter_profanity()[1]

    def split_into_sentences(self) -> List[str]:
        """Split text into sentences"""
        output = re.findall(r' ?([^.!?\n]+[.?!]*|\n)', self.joke)
        return output

    def _tokenize(self) -> List[List[str]]:
        """Tokenize all the words in the sentences"""
        output = []
        for sentence in self.sentences_joke:
            tokenized_sentence = re.findall(r'([\w\']+|\?|\.|\n|,|!)', sentence)
            output.append(tokenized_sentence)
        return output

    def filter_profanity(self, filename=resource_filename('clipkg', 'data/profanities.txt')) -> Tuple[List[List[str]], int]:
        """Filter out all the profanity"""

        output = []

        # Count number of profanities
        num_profanities = 0

        # Read in profanity file
        with open(filename, "r")as file:
            profanities = file.read().split("\n")

        for sentence in self.tokenized_joke:
            no_profanity = True
            text_sentence = " ".join(sentence)
            for profanity in profanities:

                # Check if there is profanity in the sentence
                if profanity in text_sentence:
                    profanity_in_text = True
                else:
                    profanity_in_text = False

                while profanity_in_text:
                    num_profanities += 1
                    no_profanity = False

                    # Find the index of the profanity
                    index = text_sentence.index(profanity)
                    front = text_sentence[:index - 1]

                    # Find the words that need to be replaced
                    num_words_before_profanity = len(front.split(" "))
                    num_profanity_words = len(profanity.split(" "))
                    profanity_in_sentence = sentence[num_words_before_profanity: num_words_before_profanity + num_profanity_words]

                    # Replace the profanity with '#'
                    replacement = ["#" * len(word) for word in profanity_in_sentence]

                    # Construct new sentence composed of the parts with and without profanity
                    new_sent = []
                    new_sent.extend(sentence[:num_words_before_profanity])
                    new_sent.extend(replacement)
                    new_sent.extend(sentence[num_words_before_profanity + len(replacement):])
                    text_sentence = " ".join(new_sent)
                    sentence = new_sent

                    # Check if there is still profanity in the sentence
                    if profanity in text_sentence:
                        profanity_in_text = True

                    else:
                        profanity_in_text = False
                        output.append(new_sent)

            # Add sentence immediately if there are no profanities in the sentence
            if no_profanity:
                output.append(sentence)
        return output, num_profanities

    def tell_joke(self):
        if len(self.filtered_joke) > 1:
            build_up = self.filtered_joke[:-1]
            punch_line = self.filtered_joke[-1:]

            print(self.pretty_print(build_up))
            time.sleep(1)
            print(self.pretty_print(punch_line))
        else:
            print(self.pretty_print(self.filtered_joke))

    @staticmethod
    def pretty_print(joke) -> str:
        """Print in a humanly readable way"""
        output = ""
        for sentence in joke:
            output += " ".join(sentence) + " "
        return output

    def __repr__(self):
        """Allows for printing"""
        return self.pretty_print(self.filtered_joke)

    def __eq__(self, other):
        """Equal rating"""
        return self.rating == other.rating

    def __lt__(self, other):
        """less than rating"""
        return self.rating > other.rating

    def __gt__(self, other):
        """greater than rating"""
        return self.rating < other.rating

    def __le__(self, other):
        """less than or equal rating"""
        return self.rating >= other.rating

    def __ge__(self, other):
        """greater than or equal rating"""
        return self.rating <= other.rating


class JokeGenerator:
    def __init__(self, filename=resource_filename('clipkg', 'data/reddit_dadjokes.csv')):
        self.filename = filename
        self.jokes = self.make_jokes_objects()

    def make_jokes_objects(self):
        with open(self.filename, "r", encoding='UTF-8') as lines:
            lines = csv.reader(lines, delimiter=',')
            jokes = [Joke(row) for row in lines]
            return jokes

    def generate_jokes(self):
        for joke in self.jokes:
            if len(joke.filtered_joke) > 1:
                joke.tell_joke()
            time.sleep(10)

    def random_joke(self):
        joke = random.sample(self.jokes, 1)[0]
        joke.tell_joke()


if __name__ == "__main__":
    gen = JokeGenerator(resource_filename('clipkg', 'data/reddit_dadjokes.csv'))
    x = gen.jokes[0] == gen.jokes[77]
    print(x)
    print(len(gen.jokes))



#TODO test file

#TODO find funniest joke