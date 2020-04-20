#!/bin/bash

# Importer for CSV data from Lens.org
# Written by Darko Krizic (darko@krizic.net)


CSVS="https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-broad-keywords-based-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-patents-SARS-MERS.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-patents-SARS-MERS-TAC.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-limited-keywords-based-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-CPC-based-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-declared-patseq-organism.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-SARS-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-MERS-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-SARS-diagnosis-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-MERS-diagnosis-patents.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-SARS-treatment.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Coronavirus-MERS-treatment.csv.zip https://lens-public.s3.us-west-2.amazonaws.com/coronavirus/patent/export/Ventilators.csv.zip"
test ! -d csv && mkdir csv
cd csv
path=$(pwd)
echo "Create indexes"
cat ../create_indexes.cypher | cypher-shell -a $GC_NEO4J_URL
set -e
for csv in $CSVS 
do
	zipfile=$(basename $csv)
	echo "Downloading $csv to $zipfile"
	wget -q $csv
    if [ ! -f $zipfile ]
	then
		echo "ERROR: Downloaded file $zipfile not found"
		break
	fi
	echo "Unzipping file $zipfile"
	unzip -o $zipfile
	file="${zipfile%.*}"
	
    echo "Prepareing file $file for import"
	sed -e '1s/"\#"/ID/' -e '1s/[\(\) ]//g' $file > patents.csv
	echo "Upload patents.csv"
	link=$(curl -F "file=@patents.csv" https://file.io | jq '.link')
	echo "Importing file patents.csv via $link"
	param="FILEURL=>$link"
    cat ../merge.cypher | cypher-shell -a $GC_NEO4J_URL -P $param --format verbose
	echo "Removing import file"
    rm patents.csv
    echo "Removing downloaded file $file"
    rm $file
done

echo "Running cleanups"
cat ../cleanup.cypher | cypher-shell -a $GC_NEO4J_URL
cd ..
rm -rf csv
