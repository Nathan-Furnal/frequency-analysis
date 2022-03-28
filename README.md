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
