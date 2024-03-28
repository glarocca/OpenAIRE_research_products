# OpenAIRE_research_products
This repository use the APIs to extract **Research Products** from the EGI's OpenAIRE dashboard.

Available **Research Products** are: 
- Publications,
- Research data,
- Research software, and
- Other research products.

For more details, please check the online OpenAIRE APIs [documentation](https://egi.openaire.eu/develop).

## Pre-requisites
* `Python 3.10.12+` installed on your local compute

## Access all the Publications research product

## Edit the environmental settings

Edit the `openrc.sh` file and configure the settings.

```bash
# EGI's OpenAIRE dashboard settings
export OPENAIRE_API_SERVER_URL="https://api.openaire.eu/"
export OPENAIRE_COMMUNITY="egi"

**export OPENAIRE_RESEARCH_PRODUCT="publications"**

# Data format: YYYY-MM-DD
export OPENAIRE_FROM_DATE_OF_ACCEPTANCE="2023-01-01"
export OPENAIRE_TO_DATE_OF_ACCEPTANCE="2023-12-31"

export OPENAIRE_PAGE_SIZE="10"

export FILENAME="OA_research_products.xml"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
export LOG="DEBUG"
```
