Requirements

- A locally running Neo4j
- cypher-shell is installed
- Access to the internet, all source data is downloaded directly
- About 2GB of available disk space

Run

```
./import_patents.sh
```

to import all patents. This runs a few minutes. The result is that about 16K patents are imported, but only core data.

Run

```
./import_fulltext.sh
```

to add abstracts, claims and descriptions as fulltext to the existing patents.

Using

```
call db.index.fulltext.queryNodes("patents","covid and disease and infection") yield node,score match (node)--(p:Patent) return distinct(p.LensID),p.Title,labels(node)[0],node.lang,score order by score desc limit 10
```

Returns all patents where in the title, abstract, claim or description the term "Corona" was found. Result contains the Patent LensID, the title, the part where the word was found, the language of that part and the score.

```
call db.index.fulltext.queryNodes("patents","corona and protection and infection") yield node,score match (node)--(p:Patent)--(pt:PatentTitle),(p)--(pa:PatentAbstract) return distinct(p.LensID) as patent_id,collect(pt.text) as titles,collect(pa.text) as abstracts, labels(node)[0] as location ,node.lang as language ,score as score order by score desc limit 10
```
