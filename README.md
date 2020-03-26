Requirements

* A locally running Neo4j
* cypher-shell is installed
* Access to the internet, all source data is downloaded directly
* About 2GB of available disk space

Run

```
./import_patents
```

to import all patents. This runs a few minutes. The result is that about 16K patents are imported, but only core data.


Run

```
./import_fulltext
```

to add abstracts, claims and descriptions as fulltext to the existing patents.
