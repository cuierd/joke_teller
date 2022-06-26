import sys
from argparse import ArgumentParser, FileType
from pkg_resources import resource_filename
from clipkg import joke


class TxtJokeGenerator(joke.JokeGenerator):
    """The TxtJokeGenerator objects, inherited from JokeGenerator in the joke module. It deals with TXT file."""
    def __init__(self, filename="junk_test.txt"):
        super().__init__(filename="./data/reddit_dadjokes.csv")
        self.jokes = self.make_jokes_objects_txt()
        self.filename = filename

    def make_jokes_objects_txt(self):
        """Make joke objects out of a txt file."""
        with open(self.filename, "r", encoding="UTF-8") as infile:
            jokes = [joke.Joke(["author", "link"] + [line.strip()] + [1, "date"]) for line in infile]
            return jokes


class JokePrinter:
    """JokePrinter object, which can print joke according to variate requirements."""
    def __init__(self, joke_object, print_statement, outfile, profanity):
        self.outfile = outfile
        self.joke = joke_object
        self.print = print_statement
        self.profanity = profanity

    def __print_joke(self, sentence):
        """print joke out to the CL or write it out in a file."""
        if self.outfile == sys.stdout or self.print:
            print(sentence)
        elif self.outfile != sys.stdout:
            self.outfile.write(f"{sentence}\n")
        else:
            return None

    def __pretty_print(self):
        if self.print:
            print("-"*30)

    def print_origin_sent(self):
        """print the joke content in the raw joke."""
        self.__pretty_print()
        sentence = self.joke.joke
        self.__print_joke(sentence)
        return sentence

    def print_splitted_sent(self):
        """print the joke which has been split into sentences."""
        self.__pretty_print()
        sentence_list = self.joke.sentences_joke
        for sentence in sentence_list:
            self.__print_joke(sentence)
        return sentence_list

    def print_token_sent(self):
        """print the joke which has been split into sentences and tokens."""
        self.__pretty_print()
        sentence_list = self.joke.tokenized_joke
        for sentence in sentence_list:
            token_sent = " / ".join(sentence)
            self.__print_joke(token_sent)
        return sentence_list

    def print_filter_sent(self):
        """print the joke which has been split into sentences and tokens and profanities filtered """
        self.__pretty_print()
        sentence_list = self.joke.filter_profanity(self.profanity)[0]
        for sentence in sentence_list:
            token_sent = " // ".join(sentence)
            self.__print_joke(token_sent)
        return sentence_list


DEFAULT_PROFANITY_FILE = resource_filename('clipkg', 'data/profanities.txt')
DEFAULT_IN_FILE = resource_filename('clipkg', 'data/reddit_dadjokes.csv')


def get_cli() -> ArgumentParser:
    parser = ArgumentParser("joke", description="Process a joke or some jokes in a file.")
    parser.add_argument('--infile', default=DEFAULT_IN_FILE, metavar='FILE', help="The file contain jokes.")
    parser.add_argument('--joke', type=str, help="A single joke text.")
    parser.add_argument('--author', type=str, help="Information of the author.")
    parser.add_argument('--link', type=str, help="Information of the url.")
    parser.add_argument('--rating', type=int, help="Information of the rating.")
    parser.add_argument('--time', type=str, help="Information for publishing time.")
    parser.add_argument('--output_file', type=FileType('w', encoding='UTF-8'), default=sys.stdout, metavar='FILE',
                        help="Save the processed jokes.")
    parser.add_argument('--print', action='store_true', help="Print jokes to command line.")
    parser.add_argument('--split_sent', action='store_true', help="Split a post of joke into sentences.")
    parser.add_argument('--tokenize', action='store_true', help="Split jokes into sentences and tokens")
    parser.add_argument('--filter', action='store_true', help="Filter profanities.")
    parser.add_argument('--profanity_file', default=DEFAULT_PROFANITY_FILE, help="file with profanity words.")
    return parser


def main():
    parser = get_cli()
    args = parser.parse_args()
    print(args)
    if args.joke:
        print(args.joke)
    else:
        joke_file = args.infile
        if joke_file.endswith(".csv"):
            gen = joke.JokeGenerator(joke_file)
        elif joke_file.endswith(".txt"):
            gen = TxtJokeGenerator(joke_file)
        else:
            raise IOError("Only .csv and .txt file are allowed.")
        for joke_object in gen.jokes:
            printer = JokePrinter(joke_object, args.print, args.output_file, args.profanity_file)
            if args.split_sent:
                printer.print_splitted_sent()
            elif args.tokenize:
                printer.print_token_sent()
            elif args.filter or (args.profanity_file != DEFAULT_PROFANITY_FILE):
                printer.print_filter_sent()
            else:
                printer.print_origin_sent()


if __name__ == "__main__":
    main()
