# RISE Rheinschifffahrt Showcase

Sample data set for didactic purposes.

## Creator

This data set was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in February 2022. It is based on the digital collection `Basler Rheinschifffahrt-Aktiengesellschaft, insbesondere über die Veräusserung des Dieselmotorbootes 'Rheinfelden' und die Gewährung eines Darlehens zur Finanzierung der Erstellung des Dieselmotorbootes 'Rhyblitz' an diese Firma` (shelf mark: `CH SWA HS 191 V 10`, persistent link: http://dx.doi.org/10.7891/e-manuscripta-54917, referred to as "the collection" in what follows) of the Schweizer Wirtschaftsarchiv.

## File structure and data overview

```
Rheinschifffahrt Showcase/
├── docs/
│   ├── 
│   ├── 
│   └── 
├── files/
│   ├── analysis/
│   ├── images/
│   │   ├── 0001.jpg
│   │   ├── ...
│   │   ├── 0137.jpg
│   │   ├── transkribus_metadata.xml
│   │   ├── transkribus_mets.xml
│   │   └── tropy_metadata.json
│   └── transcriptions/
│       ├── alto/
│       │   ├── 0001.xml
│       │   ├── ...
│       │   └── 0137.xml
│       ├── page/
│       │   ├── 0001.xml
│       │   ├── ...
│       │   ├── 0137.xml
│       │   └── full_transcript.xml
│       ├── tei/
│       │   └── full_transcript.xml
│       └── txt/
│           ├── 0001.txt
│           ├── ...
│           ├── 0137.txt
│           └── full_transcript.txt
├── LICENSE.md
└── README.md
```

## Data processing

- Images were extracted from the collection by importing the collection into Transkribus (Expert Client v.1.17.0) and then exporting its 137 images as JPEGs `files/images`. The sequence of the images by name (`0001.jpg` to `0137.jpg`) is the sequence of the images in the collection; note that image `0001.jpg` is a cover page (this metadata on the collection in Transkribus is provided by `transkribus_metadata.xml` and `transkribus_mets.xml`). 
- Images in the `files/images` were then grouped into semantic items using Tropy (v1.11.1) following the inscribed item numbers provided by the collection: a red penciled number in the right upper corner of an image indicates a new item. There are 68 such items consisting of 1 to 8 images. All items are letters (with enclosures where appropriate) with the exception of item number 44 which is a journal article. Each item was assigned metadata using the `Tropy Correspondence` template (see https://docs.tropy.org/before-you-begin/metadata#tropy-correspondence). Two transriptions rules were employed: 1. `purl.org/dc/elements/1.1/title` is interpreted as document inscribed number and written as `Dokument nn` where 0 ≤ n ≤ 9, and 2. `purl.org/dc/elements/1.1/creator` and `purl.org/dc/terms/audience` were interpreted as sender and receiver respectively and transcribed as is without normalization; inferred sender or receiver metadata is indicated with square brackets. The so generated metadata is available in `tropy_metadata.json`.
- Each image in `files/images` was automatically segmented with CITlab Advanced and transcribed with PyLaia Transkribus print 0.3 using Transkribus (Expert Client v.1.17.0). The transcriptions were exported to the `files/transcriptions` which contains transcriptions in four different formats: ALTO XML in `files/transcriptions/alto`, PAGE XML in the folder `files/transcriptions/page`, TEI XML in the folder `files/transcriptions/tei`, and plain text in folder `files/transcriptions/txt`. The folders `files/transcriptions/alto`, `files/transcriptions/page` and `files/transcriptions/txt` contain a transcription for each image in `files/images` (e.g., `0002.xml` in `files/transcriptions/alto` is the transcription of `0002.jpg` in `files/images`; see the `images/transkribus_metadata.xml` for the full details). In addition, `files/transcriptions/page`, `files/transcriptions/tei` and `files/transcriptions/txt` contain the files `full_transcription.xml` and `full_transcription.txt` respectively with full transcriptions of all the images in `files/images`.

## Data analysis

- `files/transcriptions/txt/full_transcript.txt` was used to do a basic named entity recognition in RStudio using spaCy. The German module for spaCy works quite well and can recognize locations, which was used for this showcase. Since the transcription was used as is, i.e. without any corrections, I assume that there are many locations that spaCy did not pick up, but it is sufficient for the purpose of this showcase. The entities classified as `location` were extracted and saved in a new data frame, for the purpose of later mapping the places mentioned in the correspondence.
Some keyword-in-context searches were carried out. The conditions are not ideal, seeing as the text is, for the moment, strictly divided in lines, not in complete letters, which would make more sense. In the absence of an ideal solution, I collapsed all rows into one to look for keywords. kwic is a useful function to count occurrences of words or phrases and to evaluate their context.
Lastly, I used Wikidata and the associated R-package to disambiguate some locations. The package WikidataR has a useful function that allows for automatic and manual disambiguation. Upon successful identification of a location, a so-called Q-ID can be added to the data frame containing the different locations. This ID can then be used to acquire further metadata down the line, like for example coordinates.

## Reusing this data set

- blah

## License

- CC BY 4.0 https://creativecommons.org/licenses/by/4.0/
