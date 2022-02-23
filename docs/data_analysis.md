# Data analysis

## NER with Python and spaCy

See [/files/analysis/ner_python](https://github.com/MHindermann/rheinschifffahrt/tree/master/files/analysis/ner_python)

### 2022-02-18

- run `App.entities_per_document` to generate `/files/analaysis/ner_python/
  ner_per_item.csv`
- manual control of `PER` entities (with deletion of non-persons labeled `PER`) in Google Sheets, exported to `/files/analaysis/ner_python/ner_per_item_controlled.csv`

### 2022-02-22

- create ontology for name normalization on with Protegé (v.5.5.0), available at [/files/analysis/pnd](https://github.com/MHindermann/rheinschifffahrt/tree/master/files/analysis/pnd/) (inspired by https://d-nb.info/standards/elementset/gnd)
 