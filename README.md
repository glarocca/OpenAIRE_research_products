# OpenAIRE_research_products
This repository use the OpenAIRE APIs to extract **Research Products** from the [EGI's OpenAIRE community dashboard](https://egi.openaire.eu/)

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

## Creating a Google Service Account

In order to read from and write data to Google Sheets in Python,
we will have to create a **Google Service Account**.

**Instructions** to create a Google Service Account are the following:

* Head over to [Google developer console](https://console.cloud.google.com/)
* Click on **Create Project** to create a new project
* Fill in the required fields and click on **Create**
* From the APIs & Services menu, click on **Enable API and Services**
* Search for "Google Drive API" and click on **Enable**
* Search for the "Google Sheets API" and click on **Enable**
* From the APIs & Services menu, click on **Credentials**
* From the "Credentials" menu, click on **Create Credentials** to create a new credentials account
* From the Credentials account, select **Service Account**
* Fill in the web form providing the name of the Service account name and click on "Create" and Continue
* Skip the step 3 to grant users access to this service account
* Click on **Done**
* Once the Service Account has been created, click on **Keys** and click on "Add new Keys" and select JSON
* The credentials will be created and downloaded as a JSON file
* Copy the JSON file to your code directory and rename it to `credentials.json`
* Grant **Edit** rights to the **Service Account** in the Google Spread-sheet

## Configure the general settings
Edit the `openrc.sh` file and configure the settings.

```bash
#!/bin/bash

# Settings of the OpenAIRE EGI Dashboard
export OPENAIRE_API_SERVER_URL="https://api.openaire.eu/"
export OPENAIRE_COMMUNITY="egi"

# Possible OPENAIRE_RESEARCH_PRODUCT = researchProducts, publications, datasets, software, other
# - researchProducts = access all the Publications, Research data, Research software, Other research products
# - publications = access all the Publications
# - datasets = access all the Datasets
# - sowtware = access all the Software
# - other = access all the Other research products
export OPENAIRE_RESEARCH_PRODUCT="publications"

# Data format: YYYY-MM-DD
export OPENAIRE_FROM_DATE_OF_ACCEPTANCE="2023-01-01"
export OPENAIRE_TO_DATE_OF_ACCEPTANCE="2023-12-31"   
export OPENAIRE_OPEN_ACCESS="false"
export OPENAIRE_PAGE_SIZE="100"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="EGI numbers"
export GOOGLE_PUBLICATIONS_WORKSHEET="Publications 2024"

export FILENAME="OA_research_products.xml"
export DUPLICATES="duplicates.txt"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"
```

## Retrieve the list of publications from the EGI's OpenAIRE dashboard
```bash
Verbose Level = DEBUG

[DEBUG] Environmental settings
{
    "OPENAIRE_API_SERVER_URL": "https://api.openaire.eu/",
    "OPENAIRE_COMMUNITY": "egi",
    "OPENAIRE_OPEN_ACCESS": "true",
    "OPENAIRE_FROM_DATE_OF_ACCEPTANCE": "2024-01-01",
    "OPENAIRE_TO_DATE_OF_ACCEPTANCE": "2024-12-31",
    "OPENAIRE_PAGE_SIZE": "100",
    "OPENAIRE_RESEARCH_OBJECT": "publications",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/modules/APIs/OpenAIRE/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/modules/APIs/OpenAIRE/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "EGI numbers",
    "GOOGLE_PUBLICATIONS_WORKSHEET": "Publications 2024",
    "LOG": "DEBUG",
    "FILENAME": "OA_research_products.xml",
    "DUPLICATES": "duplicates.txt"
}

[DEBUG] Initialise the headers of the GWorkSheet 'EGI numbers' in progress...
	This operation may take few minutes to complete. Please wait!

[DEBUG] Downloading *Research Products* from the EGI's OpenAIRE dashboard in progress
	This operation may take few minutes to complete. Please wait!

  Downloading (software) in progress... 0:00:02
  Downloading (other) in progress... 0:00:01
  Downloading (datasets) in progress... 0:00:01
  Downloading (publications) in progress... 0:00:01

[INFO] Breakdown of the OpenAIRE Research Products [publications] in the reporting period
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ OpenAIRE Research Products     ┃ Total ┃ From       ┃ To         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ -software                      │    11 │ 2024-01-01 │ 2024-12-31 │
│ -other                         │   275 │ 2024-01-01 │ 2024-12-31 │
│ -datasets                      │  3808 │ 2024-01-01 │ 2024-12-31 │
│ -publications                  │  1798 │ 2024-01-01 │ 2024-12-31 │
└────────────────────────────────┴───────┴────────────┴────────────┘
[INFO] Total research objects = 1798, Max pages = 18, Page Size = 100

[INFO] Downloading [RO: publications] *100* from page [1] in progress...
https://api.openaire.eu/search/publications?community=egi&fromDateAccepted=2024-01-01&toDateAccepted=2024-12-31&page=1&size=100&sortBy=resultdateofacceptance,descending
[INFO] 1) [Title]: Fusion innovation: Multi-scale dilated collaborative model of ConvNeXt and MSDA for fault diagnosis [..], [Authors]: Fulei Chu, [Publisher]: Elsevier BV, [Date]: 2024-12-01
[INFO] 2) [Title]: Light-favor particle production in high-multiplicity pp collisions at √s = 13 TeV as a function of transverse spherocity [..], [Authors]: Virta, Maxim Mikael Olavi, [Publisher]: Springer, [Date]: 2024-11-08
[INFO] 3) [Title]: Nonresonant central exclusive production of charged-hadron pairs in proton-proton collisions at √ = 13  TeV [..], [Authors]: Petrow, H., [Publisher]: American Physical Society (APS), [Date]: 2024-11-08
[INFO] 4) [Title]: Search for long-lived particles decaying to final states with a pair of muons in proton-proton collisions at √s = 13.6 TeV [..], [Authors]: Petrow, H., [Publisher]: Springer, [Date]: 2024-11-08
[INFO] 5) [Title]: Combination of Measurements of the Top Quark Mass from Data Collected by the ATLAS and CMS Experiments at √=7 and 8 TeV [..], [Authors]: Tuuva, T., [Publisher]: American Physical Society (APS), [Date]: 2024-11-07
[INFO] 6) [Title]: Search for heavy neutral leptons in fnal states with electrons, muons, and hadronically decaying tau leptons in proton-proton collisions at √s = 13 Te [..], [Authors]: Petrow, H., [Publisher]: Springer, [Date]: 2024-11-06
[INFO] 7) [Title]: Search for Baryon Number Violation in Top Quark Production and Decay Using Proton-Proton Collisions at √=13  TeV [..], [Authors]: Petrow, H., [Publisher]: American Physical Society (APS), [Date]: 2024-11-06
[..]
```

The full list of publications are updated in the Google worksheet (tab `Publications 2024`)

Duplicates are stored in the `DUPLICATES` file.

## References

* [OpenAIRE APIs for developers](https://egi.openaire.eu/develop)
* [Zenodo Community dump](https://zenodo.org/records/10521976)
  

