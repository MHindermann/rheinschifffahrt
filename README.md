# RISE Rheinschifffahrt Showcase

Sample data set for didactic purposes.

## Creator

This data set was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in February 2022. It is based on the digital collection "Basler Rheinschifffahrt-Aktiengesellschaft, insbesondere über die Veräusserung des Dieselmotorbootes 'Rheinfelden' und die Gewährung eines Darlehens zur Finanzierung der Erstellung des Dieselmotorbootes 'Rhyblitz' an diese Firma" (shelf mark: `CH SWA HS 191 V 10`, persistent link: http://dx.doi.org/10.7891/e-manuscripta-54917, referred to as "the collection" in what follows) of the Schweizer Wirtschaftsarchiv.

## File structure and data overview

Documentation of work in progress in [/docs](https://github.com/MHindermann/rheinschifffahrt/tree/master/docs)

Data in [/files](https://github.com/MHindermann/rheinschifffahrt/tree/master/files) with
- images and corresponding metadata in [/files/images](https://github.com/MHindermann/rheinschifffahrt/tree/master/files/images)
- transcriptions and corresponding metadata in [/files/transcriptions](https://github.com/MHindermann/rheinschifffahrt/tree/master/files/transcriptions)
- analysis of images and transcriptions in [/files/analysis](https://github.com/MHindermann/rheinschifffahrt/tree/master/files/analysis)

## Data processing

- Images were extracted from the collection by importing the collection into Transkribus (Expert Client v.1.17.0) and then exporting its 137 images as JPEGs `/files/images`. The sequence of the images by name (`0001.jpg` to `0137.jpg`) is the sequence of the images in the collection; note that image `0001.jpg` is a cover page (this metadata on the collection in Transkribus is provided by `transkribus_metadata.xml` and `transkribus_mets.xml`). 
- Images in the `/files/images` were then grouped into semantic items using Tropy (v1.11.1) following the inscribed item numbers provided by the collection: a red penciled number in the right upper corner of an image indicates a new item. There are 68 such items consisting of 1 to 8 images. All items are letters (with enclosures where appropriate) with the exception of item number 44 which is a journal article. Each item was assigned metadata using the "Tropy Correspondence" template (see https://docs.tropy.org/before-you-begin/metadata#tropy-correspondence). Two transriptions rules were employed: 1. `purl.org/dc/elements/1.1/title` is interpreted as document inscribed number and written as `Dokument nn` where 0 ≤ n ≤ 9, and 2. `purl.org/dc/elements/1.1/creator` and `purl.org/dc/terms/audience` were interpreted as sender and receiver respectively and transcribed as is without normalization; inferred sender or receiver metadata is indicated with square brackets. The so generated metadata is available in `tropy_metadata.json`.
- Each image in `/files/images` was automatically segmented with CITlab Advanced and transcribed with PyLaia Transkribus print 0.3 using Transkribus (Expert Client v.1.17.0). The transcriptions were exported to the `/files/transcriptions` which contains transcriptions in four different formats: ALTO XML in `/files/transcriptions/alto`, PAGE XML in the folder `/files/transcriptions/page`, TEI XML in the folder `/files/transcriptions/tei`, and plain text in folder `/files/transcriptions/txt`. The folders `/files/transcriptions/alto`, `/files/transcriptions/page` and `/files/transcriptions/txt` contain a transcription for each image in `/files/images` (e.g., `0002.xml` in `files/transcriptions/alto` is the transcription of `0002.jpg` in `/files/images`; see the `/images/transkribus_metadata.xml` for the full details). In addition, `/files/transcriptions/page`, `/files/transcriptions/tei` and `/files/transcriptions/txt` contain the files `full_transcription.xml` and `full_transcription.txt` respectively with full transcriptions of all the images in `files/images`.

## Data analysis

- The first step was to read each .txt-file into RStudio using R Version 4.1.1 to process the text and to have a basic identifier that can link any named entities back to the page they appeared on. This was done by listing all .txt-files and then reading them using the readtext() function (see https://cran.r-project.org/web/packages/readtext/readtext.pdf). The "doc-id" variable copies the file-name (e.g. `0001.txt`) and since this mirrors the image names (`0001.jpg`), the doc-id was used as a basis to create a variable named "image" which links back to the relevant .jpg-file. The script `spacy_update.R`documenting all these processes can be found in the /files folder.
- spaCy/spacyr: the "de_core_news_sm" model is used to parse all the texts and perform a named entity recognition. Every entity tagged as **PER**, named persons, will be used for further processing in OpenRefine. Since the linking variable unfortunately disappers when the text is parsed and a new document identifier is created (*text1*, *text2* etc.), the original link (`0001.jpg`) was recreated using an ifelse()-chain. The resulting data frame was saved as "persons.csv", with the column *link* providing the name of the respective .jpg-file.
- In OpenRefine, a text facet was added to *entity_type* to only include entities labelled **PER**. On the basis of the column named *entity*, a new column called *no.title* was created where titles were droppen (*Dr.* and *Herrn*). Clustering was not an option for this new column, so it was further edited by hand: different spellings of the same name were normalized and entities that were labelled as **PER** but did not refer to a person were dropped. The resulting data frame - now only consisting of entities labelled **PER** was then saved as `20220222persons_openrefine.csv`in `/files/analysis/ner_openrefine`. All the changes made in OpenRefine are documented in`OpenRefine_changelog.json` in `/files/analysis/ner_openrefine`.

## Data presentation
 - Some of the created data is presented the University of Bern's Omeka S instance: https://omeka.unibe.ch/s/rheinschifffahrt

## License

- CC BY 4.0 https://creativecommons.org/licenses/by/4.0/
