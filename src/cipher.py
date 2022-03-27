import pathlib
import string
from preprocessing import to_alpha
from pathlib import Path


class Cipherer:
    L_DICT = {l: i for i, l in enumerate(string.ascii_lowercase)}
    LETTERS = string.ascii_lowercase
    N_LETTERS = 26

    def __init__(self, path_to_file: Path, is_file_encrypted: bool):
        self._path: Path = path_to_file
        self._plain_text: str = ""
        self._encrypted: str = ""
        self._read_file(is_file_encrypted)

    def _read_file(self, is_enc: bool) -> None:
        if is_enc:
            self._encrypted = to_alpha(self._path.read_text())
        else:
            self._plain_text = to_alpha(self._path.read_text())

    @property
    def path(self) -> Path:
        return self._path

    @property
    def plain_text(self) -> str:
        if self._plain_text == "":
            raise ValueError(
                f"The file '{pathlib.Path(self._path).name}' is encrypted, call 'decrypt' to get plain text."
            )
        return self._plain_text

    @property
    def encrypted(self) -> str:
        if self._encrypted == "":
            raise ValueError(
                f"The file '{pathlib.Path(self._path).name}' is not encrypted, call 'encrypt' first."
            )
        return self._encrypted

    def encrypt(self, key: str):
        key = to_alpha(key)
        for idx, letter in enumerate(self.plain_text):
            # (letter index + letter index of the key at the current letter) modulo 26 letters
            enc_idx = (
                self.L_DICT[letter] + self.L_DICT[key[idx % len(key)]]
            ) % self.N_LETTERS
            self._encrypted += self.LETTERS[enc_idx]

    def decrypt(self, key: str):
        key = to_alpha(key)
        for idx, letter in enumerate(self.encrypted):
            dec_idx = (
                self.L_DICT[letter] - self.L_DICT[key[idx % len(key)]]
            ) % self.N_LETTERS
            self._plain_text += self.LETTERS[dec_idx]

    def to_file(self, out_path: Path, encrypted: bool) -> None:
        if encrypted:
            out_path.write_text(self.encrypted)
        else:
            out_path.write_text(self.plain_text)
