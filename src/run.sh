#!/bin/bash
export NEO4J_USERNAME=${GC_NEO4J_USER}
export NEO4J_PASSWORD=${GC_NEO4J_PASSWORD}
# export NEO4J_DATABASE=${GC_NEO4J_URL}
# exit when any command fails
set -e

echo "Test DB Connection. To '${GC_NEO4J_URL}' with user '${NEO4J_USERNAME}' with cypher-shell version:"
echo | cypher-shell -v
cypher-shell --non-interactive --debug -a $GC_NEO4J_URL "MATCH (n) return n limit 1"

echo "Import patents.."
./import_patents.sh
echo "...imported patents."
echo "Import fulltext..."
./import_fulltext.sh
echo "...imported fulltext"