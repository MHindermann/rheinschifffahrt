# Data analysis

## NER with Python and spaCy

See [/files/analysis/ner_python](https://github.com/MHindermann/rheinschifffahrt/tree/master/files/analysis/ner_python)

### 2022-02-18

- run `App.entities_per_document` to generate `/files/analaysis/ner_python/
  ner_per_item.csv`
- manual control of `PER` entities (with deletion of non-persons labeled `PER`) in Google Sheets, exported to `/files/analaysis/ner_python/ner_per_item_controlled.csv`

### 2022-02-22

- create ontology (inspired by https://d-nb.info/standards/elementset/gnd) for name normalization on with Protegé (v.
  5.5.0), exported to `/files/analysis/pnd` 
 
### 2022-02-23
- normalize names in `/files/analaysis/ner_python/ner_per_item_controlled.csv` in Google Sheets based on `/files/analysis/pnd`, exported to  
  `/files/analaysis/ner_python/ner_per_item_normalized.csv`. Note that `dc:source`, `spacy:ent.start_char`, and 
  `spacy:ent.end_char` jointly constitute `pnd:source`, and that `spacy:ent.text` is equivalent to `pnd:hasText` in 
  this context.
  
### 2022-02-25 
- manually individualize persons, exported to `/files/analaysis/ner_python/ner_individualized.csv`