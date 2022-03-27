from pathlib import Path
from frequency_analysis import FrequencyAnalyzer
from cipher import Cipherer
import argparse

parser = argparse.ArgumentParser(
    description="Encrypt and decrypt data with a Caesar or Vigenère cipher."
)

subparser = parser.add_subparsers(help="sub-command help", dest="cmd")

sub_encrypt = subparser.add_parser("encrypt", help="encrypt help")
sub_encrypt.add_argument("-f", "--file", type=Path, required=True)
sub_encrypt.add_argument("-k", "--key", type=str, required=True)
sub_encrypt.add_argument("-o", "--output_file", type=Path, required=True)

sub_decrypt = subparser.add_parser("decrypt", help="decrypt help")
sub_decrypt.add_argument("-f", "--file", type=Path, required=True)
sub_decrypt.add_argument("-k", "--key", type=str, required=True)
sub_decrypt.add_argument("-o", "--output_file", type=Path, required=True)

sub_freq = subparser.add_parser("freq", help="freq help")
sub_freq.add_argument("-f", "--file", type=Path, required=True)
sub_freq.add_argument("-g", "--guess", type=int, required=True)


def main():
    args = parser.parse_args()
    if args.cmd == "encrypt":
        enc_args = sub_encrypt.parse_args()
        encryptor = Cipherer(Path(enc_args.f), False)
        encryptor.encrypt(enc_args.k)
        encryptor.to_file(Path(enc_args.o), True)
    elif args.cmd == "decrypt":
        dec_args = sub_decrypt.parse_args()
        decryptor = Cipherer(Path(dec_args.f), True)
        decryptor.decrypt(dec_args.k)
        decryptor.to_file(Path(dec_args.o), False)
    elif args.cmd == "freq":
        freq_args = sub_freq.parse_args()
        freq_analyzer = FrequencyAnalyzer(Path(freq_args.f))
        freq_analyzer.guess_length_kw(freq_args.g)
        freq_analyzer()
    else:
        print("Use one of [encrypt|decrypt|freq]")


if __name__ == '__main__':
    main()
