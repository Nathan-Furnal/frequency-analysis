from pathlib import Path
from cipher import Cipherer
from collections import Counter

# See https://fr.wikipedia.org/wiki/Fr%C3%A9quence_d%27apparition_des_lettres_en_fran%C3%A7ais
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


class FrequencyAnalyzer:
    # See https://en.wikipedia.org/wiki/Index_of_coincidence

    def __init__(self, path_to_file: Path):
        self._cipherer = Cipherer(path_to_file, True)
        self._best_split = 0
        self._keyword = ''

    @property
    def cipherer(self):
        return self._cipherer

    @property
    def best_split(self):
        return self._best_split

    @property
    def keyword(self):
        return self._keyword

    def compute_ic(self, txt: str):
        counts = Counter(txt)
        return sum(map(lambda x: x * (x - 1), counts.values())) / (
            len(txt) * (len(txt) - 1)
        )

    def guess_length_kw(self, guess: int):
        # Ref : https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC-Len.html
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

    def compute_chisq(self, txt: str):
        counts = Counter(txt)
        total = 0.0
        for k, v in counts.items():
            total += (((v / len(txt)) - LETTER_FREQ_FR[k]) ** 2) / LETTER_FREQ_FR[k]
        return total

    def guess_kw(self):
        # Ref https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Recover.html
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
                    )
                )
                if curr_chisq < smallest_chisq:
                    smallest_chisq = curr_chisq
                    smallest_idx = j
            keyword += Cipherer.LETTERS[smallest_idx]

        self._keyword = keyword
        return keyword
