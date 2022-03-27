import pathlib
import string
from preprocessing import to_alpha
from pathlib import Path


class Cipherer:
    L_DICT = {l: i for i, l in enumerate(string.ascii_lowercase)}
    N_LETTERS = 26

    def __init__(self, path_to_file: Path):
        self._path: Path = path_to_file
        self._text: str = ""
        self._encrypted: str = ""
        self._read_file()

    def _read_file(self) -> None:
        self._text = to_alpha(self._path.read_text())

    @property
    def path(self) -> Path:
        return self._path

    @property
    def text(self) -> str:
        return self._text

    @property
    def encrypted(self) -> str:
        if self._encrypted == "":
            raise ValueError(
                f"The file '{pathlib.Path(self._path).name}' is not encrypted, call 'encrypt' first."
            )
        return self._encrypted

    def encrypt(self, key: str):
        for idx, letter in enumerate(self.text):
            # (letter index + letter index of the key at the current letter) modulo 26 letters
            enc_idx = (
                self.L_DICT[letter] + self.L_DICT[key[idx % len(key)]]
            ) % self.N_LETTERS
            self._encrypted += string.ascii_lowercase[enc_idx]

    def decrypt(self, key: str):
        pass

    def to_text(self, out_path: Path) -> None:
        out_path.write_text(self._encrypted)
