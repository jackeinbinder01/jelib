from nltk import word_tokenize, pos_tag, sent_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import regex as re
import string
from src.jelib.preprocess.text.base_text_preprocessor import BaseTextPreprocessor


class WordPreprocessor(BaseTextPreprocessor):
    def __init__(
            self,
            lowercase: bool = True,
            remove_punct: bool = False,
            remove_stopwords: bool = False,
            remove_special_chars: bool = False,
            add_sent_boundaries: bool = False,
            flatten: bool = False,
            tokenizer=None,
            sent_tokenizer=None,
            lemmatizer=None
    ):
        self.lowercase = lowercase
        self.remove_punct = remove_punct
        self.remove_stopwords = remove_stopwords
        self.remove_special_chars = remove_special_chars
        self.add_sent_boundaries = add_sent_boundaries
        self.flatten = flatten
        self.tokenizer = tokenizer or word_tokenize
        self.sent_tokenizer = sent_tokenizer or sent_tokenize
        self.lemmatizer = lemmatizer or WordNetLemmatizer()

        self.stopwords_set = set(stopwords.words("english")) if remove_stopwords else set()

    @staticmethod
    def get_wordnet_pos(treebank_tag: str) -> str:
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        else:
            return wordnet.NOUN

    def preprocess(self, doc: str) -> list[list[str]] | list[str]:
        if self.lowercase:
            doc = doc.lower()
        if self.remove_special_chars:
            doc = re.sub(r"[^\p{L}\p{N}\p{P}\s]", "", doc)

        sentences = self.sent_tokenizer(doc)
        preprocessed_tokens = []

        for sentence in sentences:
            tokens = self.tokenizer(sentence)

            if self.remove_punct:
                tokens = [t for t in tokens if t not in string.punctuation]
            if self.remove_stopwords:
                tokens = [t for t in tokens if t.lower() not in self.stopwords_set]

            if self.lemmatizer:
                pos_tags = pos_tag(tokens)
                tokens = [
                    self.lemmatizer.lemmatize(token, self.get_wordnet_pos(tag))
                    for token, tag in pos_tags
                ]
            if tokens:
                if self.add_sent_boundaries:
                    tokens = ["<s>"] + tokens + ["</s>"]
                preprocessed_tokens.append(tokens)

        return [token for sent in preprocessed_tokens for token in sent] if self.flatten else preprocessed_tokens
