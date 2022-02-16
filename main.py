from __future__ import annotations
from typing import List, Optional, Dict, Union, Tuple
from json import load, dump
import os.path
import spacy

DIR = os.path.dirname(__file__)


class _Utility:
    """ A collection of utility functions. """

    @staticmethod
    def load_json(file_path: str) -> list:
        """ Load a JSON object from file.

        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, encoding="utf-8") as file:
            loaded = load(file)

            return loaded

    @staticmethod
    def save_json(data: Union[List, Dict],
                  file_path: str) -> None:
        """ Save data as JSON file.

        :param data: the data to be saved
        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, "w") as file:
            dump(data, file)


# named entity recognition with spacy:
def ner():
    nlp = spacy.load("de_core_news_lg")  # python -m spacy download de_core_news_lg

    with open(DIR + "/txt/full_transcription.txt", "r") as file:
        raw_text = file.read().replace('\n', '')  # use both options

    doc = nlp(raw_text)
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
    print(len(doc.ents))

    for attribute in ["PER", "LOC", "ORG", "MISC"]:
        unique = [(x.text, x.label_) for x in doc.ents if x.label_ == attribute]
        norm = set((x.text, x.label_) for x in doc.ents if x.label_ == attribute)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"{attribute} unique {len(unique)}")
        print(f"{attribute} norm {len(norm)}")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for x in norm:
            print(x)

# todo: map texts to document; map characters to document so that entities can be attributed to document


class Document:
    """ A representation of a Document.

    :param title: the title, defaults to None
    :param transcript: the transcript(s), defaults to None
    :param char_range:
    """

    def __init__(self,
                 title: str = None,
                 transcript: [str] = None,
                 char_range: (int, int) = None) -> None:
        self.title = title
        self.transcript = transcript
        self.char_range = char_range

    @staticmethod
    def transcripts2documents() -> List[Document]:
        """ Match Transkribus plain text transcripts to Tropy items.

        Requires a correspondence between the names of Transkribus plain text transcripts and Tropy images
        (e.g., 0001.txt is the transcript of 0001.jpeg).
        """

        metadata = _Utility.load_json(DIR + "/images/items_metadata.json")
        documents = []
        for item in metadata["@graph"]:
            transcripts = []
            for photo in item["photo"]:
                with open(DIR + f"/txt/{photo['title']}.txt", "r") as file:
                    transcripts.append(file.read())
            documents.append(Document(title=item["title"],
                                      transcript=transcripts))
        return documents

    @staticmethod
    def transcripts2characters(documents: List[Document] = None) -> List[Document]:
        """ blah

        :param documents: blah"""

        if documents is None:
            documents = Document.transcripts2documents()

        char_sum = []

        for document in documents:
            char_start = len("".join(char_sum)) + 1
            char_sum.extend(document.transcript)
            char_end = len("".join(char_sum))
            document.char_range = (char_start, char_end)

        return documents

ner()

for doc in Document.transcripts2characters():
    print(doc.title, doc.char_range) # Dokument 68 (172898, 173195)
    # Zuordnung stimmt nicht, ner pro dokument machen