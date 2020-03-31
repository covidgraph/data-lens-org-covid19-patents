call apoc.load.json("FILE") yield value
        with value as json,value.bibliographic_data as bib
	merge (p:Patent {id:bib.lens_id}) 
	set 
		p.jurisdiction  	= bib.jurisdiction, 
                p.pub_key  		= bib.pub_key,
                p.pub_date  		= date(bib.pub_date),
                p.filing_key 		= bib.filing_key,
                p.lens_url 		= bib.lens_url,
		p.type			= bib.type,
		p.classification_cpc	= bib.classification_cpc,
		p.classification_ipc	= bib.classification_ipc,
		p.classificaiton_us	= bib.classification_us,
		p.source		= "json",
		p.type			= bib.type

	// add to family if it exists
	with json,bib,p,bib.family.simple.family_id as family_id
	call apoc.do.when( family_id is not null,
        	"merge (pf:PatentFamily {family_id:family_id})
        	merge (p)-[ppf:PATENT_FAMILY]->(pf)",
		"",
		{ p:p, family_id:family_id }
	) yield value

	// merge entity for each applicant
	foreach( applicant in bib.applicant  |
		merge (e:Entity {id:applicant} )
		merge (p)-[:APPLICANT]->(e)
	)

	// merge entity for each inventor
	foreach( inventor in bib.inventor |
		merge (e:Entity {id:inventor} )
		merge (p)-[:INVENTOR]->(e)
	)

	// merge entity for each owner
	foreach( owner in bib.owner |
		merge (e:Entity {id:owner} )
		merge (p)-[:OWNER]->(e)
	)

	// create PatentTitle for each title in each language
	foreach( title in bib.title |
		merge (pt:PatentTitle {id:bib.lens_id+"-t-"+title.lang})
		set			
			pt.lang 	= title.lang,
			pt.text		= title.text
		merge (p)-[:HAS_TITLE]->(pt)
	)

	// create PatentAbstract for each abstract in each language
	foreach( abstract in json.abstract |
		merge (pa:PatentAbstract {id:bib.lens_id+"-t-"+abstract.lang} )
		set
			pa.lang		= abstract.lang,
			pa.text		= abstract.text
		merge (p)-[:HAS_ABSTRACT]->(pa)
	)

	// create PatentDescription for each description in each language
	foreach( description in json.description |
		merge (pd:PatentDescription {id:bib.lens_id+"-d-"+description.lang} )
		set
			pd.lang		= description.lang,
			pd.text		= description.text
		merge (p)-[:HAS_DESCRIPTION]->(pd)
	)

	// create PatentClaim for each claim in each language
	foreach( claim in json.claims |
		merge (pc:PatentClaim {id:bib.lens_id+"-c-"+claim.lang} )
		set
			pc.lang		= claim.lang,
			pc.text		= claim.text
		merge (p)-[:HAS_CLAIM]->(pc)
	)

	return p;
