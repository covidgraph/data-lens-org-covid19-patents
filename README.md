docker build data-covidpatents .

docker run -it --rm --name data-covidpatents -e GC_NEO4J_URL=bolt://\${HOSTNAME}:7687 data-covidpatents

docker run -it --rm --name data-covidpatents -e GC_NEO4J_URL=bolt://\${HOSTNAME} data-covidpatents /bin/bash
