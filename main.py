import spacy
from collections import Counter

nlp = spacy.load("de_core_news_lg") # python -m spacy download de_core_news_lg

with open("full_transcription.txt", "r") as file:
    raw_text = file.read()#.replace('\n', '') use both options

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

#todo: map texts to document; map characters to document so that entities can be attributed to document