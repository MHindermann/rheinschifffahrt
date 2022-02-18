from __future__ import annotations
from typing import List, Optional, Dict, Union, Tuple
from json import load, dump
import os.path
import csv
import spacy
from spacy.tokens import Doc

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

    @staticmethod
    def save_csv(header: List,
                 data: List,
                 file_path: str) -> None:
        """ Save data as CSV file.

        :param header: the header
        :param data: the data to be saved
        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)


class Document:
    """ A representation of a Document.

    :param title: the title, defaults to None
    :param transcript: the transcript(s), defaults to None
    :param char_range:
    """

    def __init__(self,
                 title: str = None,
                 transcript: List[str] = None,
                 entities: Doc.ents = None,
                 char_range: (int, int) = None) -> None:
        self.title = title
        self.transcript = transcript
        self.entities = entities
        self.char_range = char_range

    def transcript2entities(self,
                            nlp: spacy.language = spacy.load("de_core_news_lg")) -> None:
        """ Add Spacy entities given the transcript.

        :param nlp: the Spacy language model, defaults to de_core_news_lg
        """

        try:
            assert(self.transcript is not None)
        except AssertionError:
            print(f"Error: No transcript in {self.title}!")

        transcript = "".join(self.transcript)
        self.entities = nlp(transcript).ents

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
                with open(DIR + f"/transcriptions/txt/{photo['title']}.txt", "r") as file:
                    transcripts.append(file.read())
            documents.append(Document(title=item["title"],
                                      transcript=transcripts))
        return documents

    @staticmethod
    def transcripts2characters(documents: List[Document] = None) -> List[Document]:
        """ blah

        :param documents: the documents, defaults to None
        """

        if documents is None:
            documents = Document.transcripts2documents()

        char_sum = []

        for document in documents:
            char_start = len("".join(char_sum)) + 1
            char_sum.extend(document.transcript)
            char_end = len("".join(char_sum))
            document.char_range = (char_start, char_end)

        return documents

    def serialize_entities(self) -> List[List]:
        """ Serialize entities for export. """

        return [[self.title, x.text.replace('\n', ''), x.label_] for x in self.entities]


def app():
    """ Test app. """

    documents = Document.transcripts2documents()
    nlp = spacy.load("de_core_news_lg")
    export = []
    for document in documents:
        document.transcript2entities(nlp=nlp)
        export.extend(document.serialize_entities())
    _Utility.save_csv(header=["dc:title", "ent.text", "ent.label_"],
                      data=export,
                      file_path=DIR + "/test.csv")


app()
