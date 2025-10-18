import regex as re
import string
from src.jelib.preprocess.text.base_text_preprocessor import BaseTextPreprocessor


class CharPreprocessor(BaseTextPreprocessor):
    def __init__(
            self,
            lowercase: bool = True,
            remove_spaces: bool = False,
            remove_punct: bool = False,
            remove_special_chars: bool = False,
            add_sent_boundaries: bool = False
    ):
        self.lowercase = lowercase
        self.remove_spaces = remove_spaces
        self.remove_punct = remove_punct
        self.remove_special_chars = remove_special_chars
        self.add_sent_boundaries = add_sent_boundaries

    def preprocess(self, doc: str) -> list[str]:
        if self.lowercase:
            doc = doc.lower()
        if self.remove_spaces:
            doc = doc.replace(" ", "")
        if self.remove_special_chars:
            doc = re.sub(r"[^\p{L}\p{N}\p{P}\s]", "", doc)
        if self.remove_punct:
            doc = ''.join(c for c in doc if c not in string.punctuation)
        chars = list(doc)
        if self.add_sent_boundaries:
            chars = ["<s>"] + chars + ["</s>"]
        return chars
