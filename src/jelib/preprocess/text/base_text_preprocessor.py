from abc import ABC, abstractmethod


class BaseTextPreprocessor(ABC):
    @abstractmethod
    def preprocess(self, doc: str) -> list[str]:
        """
        Preprocess a single document and return a list of tokens

        :param doc: A string representing a document
        :return: A list of tokens
        """
        pass

    def preprocess_corpus(self, corpus: list[str]) -> list[list[str]]:
        """
        Preprocess a whole corpus

        :param corpus: A list of unprocessed documents
        :return: A preprocessed corpus
        """
        return [self.preprocess(doc) for doc in corpus]

    def __call__(self, doc: str) -> list[str]:
        """
        Make the preprocessor callable: preprocessor(doc) → tokens

        :param doc: A string representing a document
        :return: A list of tokens
        """
        return self.preprocess(doc)
