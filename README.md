# OpenAIRE_research_products
This repository use the APIs to extract **Research Products** from the [EGI's OpenAIRE dashboard](https://egi.openaire.eu/)

Available **Research Products** are: 
- Publications,
- Research data,
- Research software, and
- Other research products.

For more details, please check the [OpenAIRE APIs for developers](https://egi.openaire.eu/develop)

The selected **Research Products** downloaded from the [EGI's OpenAIRE dashboard](https://egi.openaire.eu/) will be stored in `FILENAME`

Research Products will be parsed with the [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) python library

## Pre-requisites
* `Python 3.10.12+` installed on your local compute

## Configure the general settings

Edit the `openrc.sh` file and configure the settings.

```bash
# EGI's OpenAIRE dashboard settings
export OPENAIRE_API_SERVER_URL="https://api.openaire.eu/"
export OPENAIRE_COMMUNITY="egi"

export OPENAIRE_RESEARCH_PRODUCT="publications"

# Data format: YYYY-MM-DD
export OPENAIRE_FROM_DATE_OF_ACCEPTANCE="2023-01-01"
export OPENAIRE_TO_DATE_OF_ACCEPTANCE="2023-12-31"

export OPENAIRE_PAGE_SIZE="10"

export FILENAME="OA_research_products.xml"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
export LOG="DEBUG"
```

## Retrieve the Research Products from the EGI's OpenAIRE dashboard

```bash
Verbose Level = DEBUG

[DEBUG]  Variables settings
{
    "OPENAIRE_API_SERVER_URL": "https://api.openaire.eu/",
    "OPENAIRE_COMMUNITY": "egi",
    "OPENAIRE_OPEN_ACCESS": "true",
    "OPENAIRE_FROM_DATE_OF_ACCEPTANCE": "2023-01-01",
    "OPENAIRE_TO_DATE_OF_ACCEPTANCE": "2023-12-31",
    "OPENAIRE_PAGE_SIZE": "10",
    "LOG": "DEBUG",
    "FILENAME": "OA_research_products.xml"
}

[DEBUG]  Downloading *Research Products* from the EGI's OpenAIRE dashboard in progress
	 This operation may take few minutes. Please wait!

[ SUMMARY REPORT ]
- OpenAIRE Research Products (RPs)

[TYPE] PUBLICATIONS
       |--> Total = 3,204

[TYPE] DATASETS
       |--> Total = 5,353

[TYPE] SOFTWARE
       |--> Total = 15

[TYPE] OTHER
       |--> Total = 131

[TYPE] RESEARCHPRODUCTS
       |--> Total = 8,703

[REPORTING PERIOD]
  |--> From  = 2023-01-01
  |--> To    = 2023-12-31
```

## References

* [OpenAIRE APIs for developers](https://egi.openaire.eu/develop)
* [Zenodo Community dump](https://zenodo.org/records/10521976)
  

