"""A cipher class to encrypt and decrypt files with a Vigenère cipher, using a
one-letter keyword is equivalent to a Caesar cipher."""

import pathlib
import string
from preprocessing import to_alpha
from pathlib import Path


class Cipherer:
    """Cipherer class which provides ciphering and deciphering of text files."""

    L_DICT = {l: i for i, l in enumerate(string.ascii_lowercase)}
    LETTERS = string.ascii_lowercase
    N_LETTERS = 26

    def __init__(self, path_to_file: Path, is_file_encrypted: bool):
        self._path: Path = path_to_file
        self._plain_text: str = ""
        self._encrypted: str = ""
        self._read_file(is_file_encrypted)

    def _read_file(self, is_enc: bool) -> None:
        """Reads a file to a string and stores it.

        Parameters
        ----------
        is_enc : bool
            true if the file is ciphered and false otherwise, mainly a quality
            of life argument.
        """

        if is_enc:
            self._encrypted = to_alpha(self._path.read_text())
        else:
            self._plain_text = to_alpha(self._path.read_text())

    @property
    def path(self) -> Path:
        """Gets the path of the file to (de)cipher.

        Returns
        -------
        Path
            path of the currently held file.
        """

        return self._path

    @property
    def plain_text(self) -> str:
        """Returns the plain text version of the file.

        Returns
        -------
        str
            the plain text file content as a string.

        Raises
        ------
        ValueError
            Raises a value error in case there is no plain text.
        """

        if self._plain_text == "":
            raise ValueError(
                f"The file '{pathlib.Path(self._path).name}' is encrypted, call 'decrypt' to get plain text."
            )
        return self._plain_text

    @property
    def encrypted(self) -> str:
        """Returns the ciphered version of the file.

        Returns
        -------
        str
            the ciphered file.

        Raises
        ------
        ValueError
            Raises a value error if the file was not ciphered.
        """

        if self._encrypted == "":
            raise ValueError(
                f"The file '{pathlib.Path(self._path).name}' is not encrypted, call 'encrypt' first."
            )
        return self._encrypted

    def encrypt(self, key: str) -> None:
        """Encrypts a file based on an arbitrary key. The ciphering shifts
        letter based on a dictionary of the letter positions in the alphabet and
        a rotation on the key.

        Parameters
        ----------
        key : str
            the key to cipher the file.
        """

        key = to_alpha(key)
        for idx, letter in enumerate(self.plain_text):
            # (letter index + letter index of the key at the current letter) modulo 26 letters
            enc_idx = (
                self.L_DICT[letter] + self.L_DICT[key[idx % len(key)]]
            ) % self.N_LETTERS
            self._encrypted += self.LETTERS[enc_idx]

    def decrypt(self, key: str) -> None:
        """Decrypts a file based on an arbitrary key. The deciphering shifts
        letter based on a dictionary of the letter positions in the alphabet and
        a rotation on the key.

        Parameters
        ----------
        key : str
            the key to decipher the file.
        """

        key = to_alpha(key)
        for idx, letter in enumerate(self.encrypted):
            dec_idx = (
                self.L_DICT[letter] - self.L_DICT[key[idx % len(key)]]
            ) % self.N_LETTERS
            self._plain_text += self.LETTERS[dec_idx]

    def to_file(self, out_path: Path, encrypted: bool) -> None:
        """Writes the file content to a file.

        Parameters
        ----------
        out_path : Path
            the output path.
        encrypted : bool
            true if the file is ciphered and false otherwise. A helper argument
            to pick the proper file to output.
        """

        if encrypted:
            out_path.write_text(self.encrypted)
        else:
            out_path.write_text(self.plain_text)
