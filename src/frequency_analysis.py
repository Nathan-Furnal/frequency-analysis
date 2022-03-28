"""Frequency analysis module."""

from pathlib import Path
from cipher import Cipherer
from collections import Counter

# See https://fr.wikipedia.org/wiki/Fr%C3%A9quence_d%27apparition_des_lettres_en_fran%C3%A7ais
# Letter frequencies for the french language with diacritics grouped by ASCII letter.
LETTER_FREQ_FR = {
    "e": 0.1446,
    "a": 0.0744,
    "i": 0.0663,
    "s": 0.0651,
    "n": 0.0639,
    "r": 0.0607,
    "t": 0.0592,
    "o": 0.0502,
    "l": 0.0496,
    "u": 0.0454,
    "d": 0.0367,
    "c": 0.0324,
    "m": 0.0262,
    "p": 0.0249,
    "g": 0.0123,
    "b": 0.0114,
    "v": 0.0111,
    "h": 0.0111,
    "f": 0.0111,
    "q": 0.0065,
    "y": 0.0046,
    "x": 0.0038,
    "j": 0.0034,
    "k": 0.0029,
    "w": 0.0017,
    "z": 0.0015,
}

# See https://norvig.com/mayzner.html for reference
# Letter frequencies for the english language
LETTER_FREQ_EN = {
    "e": 0.1249,
    "t": 0.0928,
    "a": 0.0804,
    "o": 0.0764,
    "i": 0.0757,
    "n": 0.0723,
    "s": 0.0651,
    "r": 0.0628,
    "h": 0.0505,
    "l": 0.0407,
    "d": 0.0382,
    "c": 0.0334,
    "u": 0.0273,
    "m": 0.0251,
    "f": 0.0240,
    "p": 0.0214,
    "g": 0.0187,
    "w": 0.0168,
    "y": 0.0166,
    "b": 0.0148,
    "v": 0.0105,
    "k": 0.0054,
    "x": 0.0023,
    "j": 0.0016,
    "q": 0.0012,
    "z": 0.0009,
}


class FrequencyAnalyzer:
    """Provides a frequency analysis attack on a file ciphered with the Vigenère cipher.
    See: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Frequency_analysis for reference.
    """

    def __init__(self, path_to_file: Path):
        self._cipherer: Cipherer = Cipherer(path_to_file, True)
        self._best_split: int = 0
        self._keyword: str = ''

    @property
    def cipherer(self) -> Cipherer:
        return self._cipherer

    @property
    def best_split(self) -> int:
        return self._best_split

    @property
    def keyword(self) -> str:
        return self._keyword

    def compute_ic(self, txt: str) -> float:
        """Computes the index of coincidence for a given string.
        See: https://en.wikipedia.org/wiki/Index_of_coincidence for reference.

        Parameters
        ----------
        txt : str
            the string to compute the IC on.

        Returns
        -------
        float
            the index of coincidence.
        """

        counts = Counter(txt)
        return sum(map(lambda x: x * (x - 1), counts.values())) / (
            len(txt) * (len(txt) - 1)
        )

    def guess_length_kw(self, guess: int) -> None:
        """Guesses the length of a Vigenère keyword by taking the largest
        average index of coincidence among a ciphered text cosets.

        See: https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC-Len.html for reference.

        Parameters
        ----------
        guess : int
            the guess for the length of the keyword.

        Raises
        ------
        ValueError
            Raises a value error if the guess is not a positive number.
        """
        if guess < 1:
            raise ValueError(
                f"The guessed key length should be larger than 1 but got: {guess}"
            )
        if guess > (txt_len := len(self.cipherer.encrypted)):
            raise ValueError(
                f"Guessing a key of size {guess} with a text of length {txt_len} is not possible."
            )
        best_ic = 0
        best_split = 0

        for split in range(1, guess):
            avg_ic = 0.0
            for step in range(split):
                avg_ic += self.compute_ic(self.cipherer.encrypted[step::split])
            avg_ic /= split
            if avg_ic > best_ic:
                best_ic = avg_ic
                best_split = split

        self._best_split = best_split

    def compute_chisq(self, txt: str, lang: str = "fr"):
        """Computes the chi square value of a string. Basically an error measure
        between the theoretical and empirical frequencies of a letter. It also
        means that this measure requires a language specific frequency table.

        See: https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Recover.html for reference.

        Parameters
        ----------
        txt : str
            the text to compute the chi square value for.

        lang: str
            the language to pick for the analysis. {fr, en} are available. Default is french.

        Raises
        ------
        ValueError
            Raises a value error if the selected language is not among the possible values.
        """
        if lang not in {"fr", "en"}:
            raise ValueError(
                f"The language argument should be either `fr` or `en` but got: {lang}"
            )
        counts = Counter(txt)
        total = 0.0
        lang_freqs = {"fr": LETTER_FREQ_FR, "en": LETTER_FREQ_EN}
        for k, v in counts.items():
            total += (((v / len(txt)) - lang_freqs[lang][k]) ** 2) / lang_freqs[lang][k]
        return total

    def guess_kw(self, lang: str = "fr"):
        """Attempts to retrieve the key of a Vigenère cipher by using the
        chi-square measure. Takes the best value of the keyword length estimate
        and loops over every coset to find the smallest chi-square (the smallest
        error coset).

        See: https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Recover.html for reference.

        Parameters
        ----------
        lang: str
            the language to pick for the analysis. {fr, en} are available. Default is french.

        Raises
        ------
        ValueError
            Raises a value error if there is no estimate for the length of the
            keyword.

            Raises a value error is the selected language is not among the possible values.
        """

        if lang not in {"fr", "en"}:
            raise ValueError(
                f"The language argument should be either `fr` or `en` but got: {lang}"
            )

        if self.best_split == 0:
            raise ValueError(
                f"Insert a range of guesses for the number of letters in the keyword."
            )
        keyword = ""
        for i in range(self.best_split):
            smallest_chisq = 1_000_000  # large value to make sure minimum is picked
            smallest_idx = 100  # idx of letter with the smallest chisq
            for j in range(Cipherer.N_LETTERS):
                curr_chisq = self.compute_chisq(
                    ''.join(
                        map(
                            lambda x: Cipherer.LETTERS[
                                (Cipherer.L_DICT[x] - j) % Cipherer.N_LETTERS
                            ],
                            self.cipherer.encrypted[i :: self.best_split],
                        )
                    ),
                    lang,
                )
                if curr_chisq < smallest_chisq:
                    smallest_chisq = curr_chisq
                    smallest_idx = j
            keyword += Cipherer.LETTERS[smallest_idx]

        self._keyword = keyword
        return keyword
