from dataclasses import dataclass
from typing import List, Union


@dataclass
class KorpusData:
    description: str
    texts: List[str]

    def __len__(self):
        return len(self.texts)

    def __getitem__(self):
        raise NotImplementedError('Implement __getitem__')

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def get_all_texts(self):
        """
        If Some KorpusDataClass has two or more text attributes, modify this function.

            class SentencePairData(KorpusData):
                pairs: List[str]

                def get_all_texts(self):
                    return self.texts + self.pairs

        """
        return self.texts

    def __str__(self):
        classname = self.__class__.__name__
        spec = ""
        for name, var in self.__dict__.items():
            if name not in {'description', 'self'}:
                spec += f'  {classname}.{name} (list[{var[0].__class__.__name__}]) : size={len(var)}\n'
        s = f"""{classname}\n{self.description}\n\nAttributes:\n{spec}\n"""
        return s


@dataclass
class SentencePair:
    text: str
    pair: str


class SentencePairKorpusData(KorpusData):
    pairs: List[str]

    def __init__(self, description, texts, pairs):
        if not (len(texts) == len(pairs)):
            raise ValueError('All two arguments must be same length')
        super().__init__(description, texts)
        self.pairs = pairs

    def __getitem__(self, index):
        return SentencePair(self.texts[index], self.pairs[index])

    def get_all_pairs(self):
        return [SentencePair(s, p) for s, p in zip(self.texts, self.pairs)]


@dataclass
class LabeledSentencePair:
    text: str
    pair: str
    label: Union[str, int, float, bool]


class LabeledSentencePairKorpusData(KorpusData):
    pairs: List[str]
    labels: List

    def __init__(self, description, texts, pairs, labels):
        if not (len(texts) == len(pairs) == len(labels)):
            raise ValueError('All three arguments must be same length')
        super().__init__(description, texts)
        self.pairs = pairs
        self.labels = labels

    def __getitem__(self, index):
        return LabeledSentencePair(self.texts[index], self.pairs[index], self.labels[index])

    def get_all_pairs(self):
        return [SentencePair(s, p) for s, p in zip(self.texts, self.pairs)]

    def get_all_labels(self):
        return self.labels


class Korpus:
    description: str
    license: str

    def __str__(self):
        classname = self.__class__.__name__
        s = f"{classname}\n{self.description}\n\nAttributes\n"
        for name, var in self.__dict__.items():
            if name not in {'description', 'license', 'self'}:
                s += f' {classname}.{name} : size={len(var)}\n'
        return s

    def cleaning(self, raw_documents: List[str], **kargs):
        """`raw_data` to `sentences`"""
        raise NotImplementedError('Implement this function')

    def get_all_texts(self):
        raise NotImplementedError('Implement this function')

    def save(self, root_dir):
        """save prorce` to `sentences`"""
        raise NotImplementedError('Implement this function')
