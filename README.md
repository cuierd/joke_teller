# clipkg--CLI Package

## Introduction

This entire set of cli codes is for the exercise 3 for PCL2. It tries to parse a joke along with its mata information.

By using CLI, users can specify how and where to output the parsed joke.

> **IMPORTANT:** We added a class for generate joke objects for .txt files. It is not necessary, and we did it for fun.

### To Check Our Codes

* Our implementation of the CLI interface is in ```CLI.py```
* We tried to keep the file ```joke.py``` as untouched as possible.
* Codes for formatting output is also in  ```CLI.py```

## Details
This is how the CLI could work:

```sh
$ jg
$ jg --print
$ jg --profanity_file other_profanities.txt --output_file save_my_output.txt
$ jg --joke "This is a joke. Unfortunately, it is not funny" --author Me --link www.this_is_a_url.ch --rating 1 --time "14.03.2002 03:00"
$ jg --print --split_sent
$ jg --print --tokenize
$ jg --print --filter
```

- Provide a different input file for the joke information. If the user doesn't provide one, use reddit_dadjokes.csv as default.
- Provide an output file to save the output of your implementation. If none is provided as an argument, print to standard output
- Print the jokes in an easy-to-read format for all the different variants:
    * A single joke with the information of the author, link to the joke, rating, and time specified as additional arguments over the command line
    * Print the jokes glued together from the provided file (i.e. jg)
    * Print the jokes from the provided file, each post separated by "---------" (e.g. jg --print)
    * Print the jokes from the provided file separated into sentences, each post separated by "---------" (e.g. jg --print --split_sent)
    * Print the jokes from the provided file separated into sentences and tokens, each post separated by "---------" (e.g. jg --print --tokenize)
    * Print the jokes from the provided file separated into sentences and tokens, each post separated by "---------" (e.g. jg --print --filter).

### LICENSE
We chose MIT license simply because it is short, simple, easy to use and flexible to be distributed under different teams without source codes.
We think for this exercise, MIT license is good enough.
