# Usage

To use this, you'll need a recent Python install, preferably `3.10`, as of this
writing.

You will also need to install `unidecode`, the requie

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




