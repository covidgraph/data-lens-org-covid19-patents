// Create fulltext for all titles, abstracts, description and claims
return "Ensuring fulltext index";
call db.index.fulltext.createNodeIndex("patents",["PatentTitle","PatentAbstract","PatentDescription","PatentClaim"],["text"]);

// create fulltext for all fragments
return "Ensuring fragment index";
call db.index.fulltext.createNodeIndex("fragments",["Fragment"],["text"]);

