# OpenAIRE_research_products
This repository use the APIs to extract **Research Products** from the EGI's OpenAIRE dashboard.

Available **Research Products** are: 
- Publications,
- Research data,
- Research software, and
- Other research products.

For more details, please check the [OpenAIRE APIs for developers](https://egi.openaire.eu/develop).

## Pre-requisites
* `Python 3.10.12+` installed on your local compute

## Access all the Publications research product

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

## Configure the Research Products to query

Depending by the Research Products interested to query from the EGI's OpenAIRE dashboard, configure the additional environmental variable:

### Research Products (publications)

To access all the **publications**

```bash
Edit the `openrc.sh` file and add the settings:
export OPENAIRE_RESEARCH_PRODUCT="publications"
```

## Retrieve the Publications from the OpenAIRE's dashboard (in the specific period)

```bash
$ source openrc.sh && python3 get_research_products.py

Verbose Level = DEBUG

[INFO] 	Environment settings
{
    "OPENAIRE_API_SERVER_URL": "https://api.openaire.eu/",
    "OPENAIRE_COMMUNITY": "egi",
    "OPENAIRE_OPEN_ACCESS": "false",
    "OPENAIRE_RESEARCH_PRODUCT": "publications",
    "OPENAIRE_FROM_DATE_OF_ACCEPTANCE": "2023-01-01",
    "OPENAIRE_TO_DATE_OF_ACCEPTANCE": "2023-12-31",
    "OPENAIRE_PAGE_SIZE": "10",
    "LOG": "DEBUG",
    "FILENAME": "OA_research_products.xml"
}

[INFO] 	Download the list of *PUBLICATIONS* from the EGI's OpenAIRE dashboard in progress..
	This operation may take few minutes. Please wait!
[INFO] 	List of the first [10] Publications
[..]

[SUMMARY REPORT]
- OpenAIRE Research Products
[INFO] PUBLICATIONS
  |--> Total = 2875
[REPORTING PERIOD]
  |--> From = 2023-01-01
  |--> To = 2023-12-31

