// create fragments for all PatentTitle
return "Creating fragments for titles";
match (p:Patent)--(pa:PatentTitle) with p,pa,split(pa.text, ". ") as frags with p,pa,frags,range(0,size(frags)-1) as r with p,pa,frags,r foreach ( entry in r | merge (f:Fragment {id:pa.id+"-f-"+entry}) set f.text = frags[entry], f.sequence = entry, f.kind = labels(pa)[0] merge (pa)-[:HAS_FRAGMENT]->(f) ) with p,pa match (pa)--(f:Fragment) return distinct(p.id);

// create fragments for all PatentAbstract
return "Creating fragments for abstracts";
match (p:Patent)--(pa:PatentAbstract) with p,pa,split(pa.text, ". ") as frags with p,pa,frags,range(0,size(frags)-1) as r with p,pa,frags,r foreach ( entry in r | merge (f:Fragment {id:pa.id+"-f-"+entry}) set f.text = frags[entry], f.sequence = entry, f.kind = labels(pa)[0] merge (pa)-[:HAS_FRAGMENT]->(f) ) with p,pa match (pa)--(f:Fragment) return distinct(p.id);

// create fragments for all PatentDescription
return "Creating fragments for description";
match (p:Patent)--(pa:PatentDescription) with p,pa,split(pa.text, ". ") as frags with p,pa,frags,range(0,size(frags)-1) as r with p,pa,frags,r foreach ( entry in r | merge (f:Fragment {id:pa.id+"-f-"+entry}) set f.text = frags[entry], f.sequence = entry, f.kind = labels(pa)[0] merge (pa)-[:HAS_FRAGMENT]->(f) ) with p,pa match (pa)--(f:Fragment) return distinct(p.id);

// create fragments for all PatentClaim
return "Creating fragments for claim";
match (p:Patent)--(pa:PatentClaim) with p,pa,split(pa.text, ". ") as frags with p,pa,frags,range(0,size(frags)-1) as r with p,pa,frags,r foreach ( entry in r | merge (f:Fragment {id:pa.id+"-f-"+entry}) set f.text = frags[entry], f.sequence = entry, f.kind = labels(pa)[0] merge (pa)-[:HAS_FRAGMENT]->(f) ) with p,pa match (pa)--(f:Fragment) return distinct(p.id);

// create linked list of all fragments
return "Creating linked list of all fragments";
match (f:Fragment) where f.sequence > 0 match (f)<--(n)-->(f2:Fragment) where f2.sequence = f.sequence - 1 merge (f2)-[:NEXT]->(f);
