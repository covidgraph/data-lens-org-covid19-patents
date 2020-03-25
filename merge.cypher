return "Creading indizes";
create index on :Patent(ID);
create index on :Person(id);
create index on :Kind(id);
create index on :Type(id);

return "Loading patents";
load csv with headers from "file:import/patents.csv" as line
    merge (p:Patent {ID:toInt(line.ID)})
    set 
		p.Jurisdiction = line.Jurisdiction,
		p.Kind = line.Kind,
		p.PublicationNumber = line.PublicationNumber,
		p.LensID = line.LensID,
		p.PublicationDate = date(line.PublicationDate),
		p.PublicationYear = toInt(line.PublicationYear),
		p.ApplicationNumber = line.ApplicationNumber,
		p.ApplicationDate = date(line.ApplicationDate),
		p.PriorityNumbers = line.PriorityNumbers,
		p.EarliestPriorityDate = date(line.EarliestPriorityDate),
		p.Title = line.Title,
		p.Applicants = split(line.Applicants,";;"),
		p.Inventors = split(line.Inventors,";;"),
		p.OwnersUS = split(line.OwnersUS, ";;" ),
		p.URL = line.URL,
		p.Type = line.Type,
		p.HasFullText = (case line.HasFullText when "yes" then true else false end),
		p.CitedbyPatentCount = toInt(line.CitedbyPatentCount),
		p.SimpleFamilySize = toInt(line.SimpleFamilySize),
		p.ExtendedFamilySize = toInt(line.ExtendedFamilySize),
		p.SequenceCount = toInt(line.SequenceCount),
		p.CPCClassifications = split(line.CPCClassifications,";;"),
		p.IPCRClassifications = split(line.IPCRClassifications,";;"),
		p.USClassifications = split(line.USClassifications,";;"),
		p.NPLCitationCount = toInt(line.NPLCitationCount),
		p.NPLResolvedCitationCount = toInt(line.NPLResolvedCitationCount),
		p.NPLResolvedLensIDs = split(line.NPLResolvedLensIDs, ";;"),
		p.NPLResolvedExternalIds = line.NPLResolvedExternalIds,
		p.NPLCitations = line.NPLCitations
;
