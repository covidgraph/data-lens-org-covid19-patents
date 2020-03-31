Requirements

* A locally running Neo4j
* Command line tool "cypher-shell" is installed
* Command line tool "jq" (for handling JSON)
* Environment variable "CYPHER_SHELL_PARAM" is defined (e.g. "-a bolt://username:password@localhost:7687")
* Access to the internet, all source data is downloaded directly
* About 3GB of available disk space

Run

```
./import_fulltext
```

to import all patents. This runs a few minutes. The result is that about 16K patents are imported, but only core data.


Run

```
./import_fulltext
```

to add abstracts, claims and descriptions as fulltext to the existing patents.

Using

```
call db.index.fulltext.queryNodes("patents","Corona") yield node,score match (node)--(p:Patent)--(pt:PatentTitle) return distinct(p.id) as id, collect(pt.text) as titles, labels(node)[0] as found_type, node.lang as found_in_lang ,score order by score desc limit 10
```

Returns all patents where in the title, abstract, claim or description the term "Corona" was found. Result contains the Patent LensID, the title, the part where the word was found, the language of that part and the score.
