# Introduction

Frequency analysis project, Nathan FURNAL 55803. 

# Usage

To use this, you'll need a recent Python install, at least `>= 3.8` because of
the use of the `:=` operator in `frequential_analysis.py`. It can be easily
removed but the use of f-strings require at least python `>= 3.6`. 

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
`freq` command takes an input file and a guess for the length of the
keyword. For example, a guess of 8 will try to find a best keyword from the
length 1 to 7. Once a key is found, the `freq` command outputs the result to the
standard output.

There is a text file in the `data/` folder, so this is a possible workflow: 

```sh
# Encryption
python src/main.py encrypt -f data/la-sagesse-et-la-destinee-extract.txt 
-k porte -o data/out-key-porte.txt 
# Decryption
python src/main.py encrypt -f data/out-key-porte.txt -k porte -o data/out-key-porte-deciphered.txt
# Frequency analysis
python src/main.py -f data/out-key-porte.txt -g 10
```


