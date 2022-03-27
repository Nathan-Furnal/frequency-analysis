from pathlib import Path
from frequency_analysis import FrequencyAnalyzer
from cipher import Cipherer
import argparse

parser = argparse.ArgumentParser(
    description="Encrypt and decrypt data with a Caesar or Vigenère cipher."
)

subparser = parser.add_subparsers(help="sub-command help", dest="cmd")

sub_encrypt = subparser.add_parser(
    "encrypt",
    help="Encrypts an input file with a given key and saves it to the output file.",
)
sub_encrypt.add_argument(
    "-f", "--file", type=Path, required=True, help="the input file."
)
sub_encrypt.add_argument(
    "-k", "--key", type=str, required=True, help="The key to encode the file."
)
sub_encrypt.add_argument(
    "-o", "--output_file", type=Path, required=True, help="the output file."
)

sub_decrypt = subparser.add_parser(
    "decrypt",
    help="Decrypts an input file with a given key and saves it to the output file.",
)
sub_decrypt.add_argument(
    "-f", "--file", type=Path, required=True, help="the input file."
)
sub_decrypt.add_argument(
    "-k", "--key", type=str, required=True, help="the key to decode the file."
)
sub_decrypt.add_argument(
    "-o", "--output_file", type=Path, required=True, help="the output file."
)

sub_freq = subparser.add_parser(
    "freq",
    help="Uses frequency analysis to decrypt a file encoded with a Caesar or Vigenère cipher. A guess is required for the length of the keyword.",
)
sub_freq.add_argument("-f", "--file", type=Path, required=True, help="the input file.")
sub_freq.add_argument(
    "-g",
    "--guess",
    type=int,
    required=True,
    help="Range of values to try for the length of the keyword. A value of 5 will attempt to find the length from 1 to 4.",
)


def main():
    args = parser.parse_args()
    if args.cmd == "encrypt":
        encryptor = Cipherer(Path(args.file), False)
        encryptor.encrypt(args.key)
        encryptor.to_file(Path(args.output_file), True)
    elif args.cmd == "decrypt":
        decryptor = Cipherer(Path(args.file), True)
        decryptor.decrypt(args.key)
        decryptor.to_file(Path(args.output_file), False)
    elif args.cmd == "freq":
        freq_analyzer = FrequencyAnalyzer(Path(args.file))
        freq_analyzer.guess_length_kw(args.guess)
        freq_analyzer.guess_kw()
        print(f"The guessed key is: {freq_analyzer.keyword}")
    else:
        print("Use one of [encrypt|decrypt|freq]")


if __name__ == '__main__':
    main()
