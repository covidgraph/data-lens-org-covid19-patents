# Covid-Patents Data loader

This python script helps to transform the data set from the [Lens.org Covid19 Patent Dataset](https://about.lens.org/covid-19/)
into a neo4j graph

Maintainer: [Tim](https://github.com/motey)

Version: 0.0.1

Python version: Python3

# Usage

## Docker

**Run**

`docker run -it --rm --name data-lens-org-covid19-patents -e GC_NEO4J_URL="bolt://${HOSTNAME}:7687" covidgraph/data-lens-org-covid19-patents`

**Build local image**

From the root directorie of this repo run:

`docker build -t data-lens-org-covid19-patents .`

**Run local image**

Examples (neo4j runs on the docker linux host machine)

`docker run -it --rm --name data-lens-org-covid19-patents -v ${PWD}/dataset:/app/dataset -e GC_NEO4J_URL="bolt://${HOSTNAME}:7687" data-lens-org-covid19-patents`

**Envs**

The most important Env variables are:

`ENV`: will be `PROD` or `DEV`

`GC_NEO4J_URL`: The full bolt url example 'bolt://myneo4jhostname:7687'

`GC_NEO4J_USER`: The neo4j user

`GC_NEO4J_PASSWORD`: The neo4j password

besides that you can set all variables in dataloader/config.py via env variable with a `CONFIGS_` prefix. See https://git.connect.dzd-ev.de/dzdtools/pythonmodules/-/tree/master/Configs for more details

**Volumes**

`/app/dataset`

Here is the downloaded data set located. You can mount this path with `-v /mylocal/path:/app/dataset` to prevent redownloading of the dataset.

`/app/dataloader`

Here is the python source code located. You can mount this for development or tinkering

## Local

Copy `dataloader/env/DEFAULT.env` to `dataloader/env/DEVELOPMENT.env`:

`cp dataloader/env/DEFAULT.env dataloader/env/DEVELOPMENT.env`

Enter your neo4j connection string at `dataloader/env/DEVELOPMENT.env` into the variable `CONFIGS_NEO4J_CON`:

```env
GC_NEO4J_URL='bolt://myuser:mypasswd@localhost:7687'
```

Install the requirements with

`pip3 install -r requirement.txt`

run the main.py

`python3 main.py`

# Data

## Scheme

![Datascheme](https://github.com/covidgraph/data-lens-org-covid19-patents/blob/master/docs/datascheme.png)
