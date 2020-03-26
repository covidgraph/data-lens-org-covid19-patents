return "Externalizing kinds";
match (p:Patent) merge (k:Kind {id:p.Kind}) merge (p)-[:IS_KIND]->(k);

return "Externalizing years";
match (p:Patent) where not p.PublicationYear is null merge (y:Year {id:p.PublicationYear}) merge (p)-[:PUBLISHED]->(y);

return "Externalizing types";
match (p:Patent) merge (t:Type {id:p.Type}) merge (p)-[:IS_TYPE]->(t);

return "Externalizing inventors";
match (p:Patent) where not p.Inventors is null foreach (inventor in p.Inventors | merge (e:Entity {id:inventor}) merge (p)-[:INVENTOR]->(e) );

return "Externalizing applicants";
match (p:Patent) where not p.Applicants is null foreach (applicant in p.Applicants | merge (e:Entity {id:applicant}) merge (p)-[:APPLICANT]->(e) );

return "Connecting referencing patents";
match (p0:Patent) where size(p0.NPLResolvedLensIDs) > 0 match (p1:Patent) where p1.LensID in p0.NPLResolvedLensIDs merge (p0)-[:REFERENCES]->(p1);
