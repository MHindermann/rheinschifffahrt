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
    """

    def __init__(self,
                 title: str = None,
                 transcript: List[str] = None,
                 entities: Doc.ents = None) -> None:
        self.title = title
        self.transcript = transcript
        self.entities = entities

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

        metadata = _Utility.load_json(DIR + "/images/tropy_metadata.json")
        documents = []
        for item in metadata["@graph"]:
            transcripts = []
            for photo in item["photo"]:
                with open(DIR + f"/transcriptions/txt/{photo['title']}.txt", "r", encoding='UTF8') as file:
                    transcripts.append(file.read())
            documents.append(Document(title=item["title"],
                                      transcript=transcripts))
        return documents

    def serialize_entities(self) -> List[List]:
        """ Serialize entities for export. """

        return [[self.title, x.text.replace('\n', ''), x.label_, x.start_char, x.end_char] for x in self.entities]


class App:
    """ A collection of scripts. """

    @staticmethod
    def entities_per_document(file_path: str = DIR + "/analysis/ner_per_item.csv") -> None:
        """ Export entities per document as CSV.

        :param file_path: complete path to file including filename and extension
        """

        documents = Document.transcripts2documents()
        nlp = spacy.load("de_core_news_lg")

        export = []
        for document in documents:
            document.transcript2entities(nlp=nlp)
            export.extend(document.serialize_entities())

        _Utility.save_csv(header=["dc:source",
                                  "spacy:ent.text",
                                  "spacy:ent.label_",
                                  "spacy:ent.start_char",
                                  "spacy:ent.end_char"],
                          data=export,
                          file_path=file_path)
