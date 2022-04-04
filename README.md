# Introduction

Frequency analysis project. This project implements a [Vigenère
cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher) with the possibility
of ciphering and deciphering text files.

A frequency analysis attack is also implemented, based on a guess of keyword
length. In short, it breaks down ciphered text into chunks based on the keyword
length. The length providing the highest [index of
coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence) becomes the
candidate length to find the keyword. Then, each letter of the alphabet is
compared against a ciphered chunk of text with a measure of proximity using
letters' frequencies. This step can be seen as a repeatedly trying to find the
answer to a Caesar cipher, for each chunk. Then, all the best letter guesses are
concatenated to give the keyword.

Note that this method is not foolproof for two reasons: it's weak against short
texts which tend to deviate from expected letter frequencies and long keywords
make the checking process prohibitive as well.

N.B: A Vigenère cipher with one letter is a [Caesar
cipher](https://en.wikipedia.org/wiki/Caesar_cipher).

See [the high-level overview](#High-level-overview) for a quick rundown.

# Usage

To use this, you'll need a recent Python install, at least `>= 3.8` because of
the use of the `:=` operator in `frequential_analysis.py`. It can be easily
removed but the use of f-strings requires at least python `>= 3.6`.

You will also need to install `unidecode`, this can be done with:

```sh
pip3 install -r requirements.txt
```

There are 3 main commands, to be launched from the root directory
(`frequential-analysis`).

To know what each command does, you can use:

```sh
python src/main.py -h
```

Using the `-h` with any of the sub-command will trigger the help as well:

```sh
python src/main.py {encrypt, decrypt, freq} -h
```

The `encrypt` command takes an input file, a key and an output file. The
`decrypt` command takes an input file, a key and an output file as well. The
`freq` command takes an input file and a guess for the length of the keyword. It
also takes a language argument, both French and English are supported. For
example, a guess of 8 will try to find a best keyword from the length 1
to 7. Once a key is found, the `freq` command outputs the result to the standard
output.

There is a text file in the `data/` folder, so this is a possible workflow:

```sh
# Encryption
python src/main.py encrypt -f data/la-sagesse-et-la-destinee-extract.txt
-k porte -o data/out-key-porte.txt
# Decryption
python src/main.py encrypt -f data/out-key-porte.txt -k porte -o data/out-key-porte-deciphered.txt
# Frequency analysis
python src/main.py freq -f data/out-key-porte.txt -g 10 -l fr # language is French
```

# High-level overview

The goal of this project is to provide a way to cipher plain text files based on
a key and then automatically find the key back to decipher the text.

Some trade-offs were made for simplicity: only the basic 26 letters alphabet was
allowed and any spaces or punctuation was removed as well. In that sense, it's a
good introduction to implement ciphering but not a real-world tool!

More information about what a cipher is and how they're implemented can be found
in the documentation of the code. Let's get started.

We can start with the most simple example, a *Caesar* cipher which is a one
letter shift.

For example, the sentence `Hello World!`, shifted by the letter `K` ("a" is 0
and "k" is 10), will become :

    | H | E | L | L | O |  | W | O | R | L | D |  plain text
    | K | K | K | K | K |  | K | K | K | K | K |   key
    | R | O | V | V | Y |  | G | Y | B | V | N |  ciphered text

This kind of cipher is very susceptible to be cracked because the letters are
all shifted by the same key (a unique letter). Since that's the case, one can
try to count the frequencies of each letter, plug back in the usual letter
frequencies for each letter and it's done.

A Vigenère cipher is more elaborate, the key is a word or a sentence and not
one letter. Because of this, the same letters can be shifted by a different
amount and the resulting ciphered text is not susceptible to the deciphering
explained above.

For example, The sentence `Hello World!`, encrypted with the word `key` (with
letters indexed from 0 to 25), becomes:

    | H | E | L | L | O |  | W | O | R | L | D |  plain text
    | K | E | Y | K | E |  | Y | K | E | Y | K |   key
    | R | I | J | V | S |  | U | Y | V | J | N |  ciphered text

You'll find that where the key from this cipher matches the key from the
previous one, the ciphered text matches! This is one of the basic building
blocks used to attack this ciphering scheme, it's a bit more elaborate but you
can find the references and examples in the documentation of the code.
