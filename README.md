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
	 This operation may take few minutes to complete. Please wait!

Downloading (publications) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Downloading (software) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Downloading (other) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Downloading (datasets) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Downloading (researchProducts) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

[INFO]  Breakdown of the OpenAIRE research products in the reporting period
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ OpenAIRE Research Products     ┃ Total ┃ From       ┃ To         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ -publications                  │  3204 │ 2023-01-01 │ 2023-12-31 │
│ -software                      │    14 │ 2023-01-01 │ 2023-12-31 │
│ -other                         │   131 │ 2023-01-01 │ 2023-12-31 │
│ -datasets                      │  5353 │ 2023-01-01 │ 2023-12-31 │
│ -researchProducts              │  8702 │ 2023-01-01 │ 2023-12-31 │
└────────────────────────────────┴───────┴────────────┴────────────┘
[INFO]  List of scientific publications produced in the reporting period
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ #      ┃ Title                                                                            ┃ Creator(s)           ┃ DateOfAccepta… ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 1      │ Blue-Cloud 2026 - D2.2 New Blue Data Infrastructures – Service Analysis Report   │ Schaap, Dick         │ 2023-12-28     │
│ 2      │ Search for flavour-changing neutral tqH interactions with H → γγ in pp           │ Yu. Volkotrub        │ 2023-12-28     │
│        │ collisions at $$ \sqrt{s} $$ = 13 TeV using the ATLAS detector                   │                      │                │
│ 3      │ Probing Small Bjorken-x Nuclear Gluonic Structure via Coherent J/ψ               │ Tuuva, T.            │ 2023-12-28     │
│        │ Photoproduction in Ultraperipheral Pb-Pb Collisions at √sNN = 5.02 TeV           │                      │                │
│ 4      │ Search for resonances in events with photon and jet final states in              │ Tcherniaev, Evgueni  │ 2023-12-28     │
│        │ proton-proton collisions at $$ \sqrt{s} $$ = 13 TeV                              │                      │                │
│ 5      │ Blue-Cloud 2026 - D2.1 Existing DD&AS and Blue Data Infrastructures – Review and │ Schaap, Dick         │ 2023-12-28     │
│        │ Specifications for Optimisation Report                                           │                      │                │
│ 6      │ EOSC-Future Test Science Project "META-COVID": Linked resources between          │ Holub, Petr          │ 2023-12-27     │
│        │ BBMRI-ERIC Directory and ECRIN Metadata Repository                               │                      │                │
│ 7      │ Search for direct production of electroweakinos in final states with one lepton, │ Zou, Wenkai          │ 2023-12-27     │
│        │ jets and missing transverse momentum in pp collisions at $$ \sqrt{s} $$ = 13 TeV │                      │                │
│        │ with the ATLAS detector                                                          │                      │                │
│ 8      │ Cascaded Bilinear Mapping Collaborative Hybrid Attention Modality Fusion Model   │ Kuizhi Mei           │ 2023-12-24     │
│ 9      │ Measurements of ${\Lambda_{\rm c}^+\rm /D^0}$ ratio as a function of             │ Sheibani, Oveis      │ 2023-12-24     │
│        │ multiplicity at midrapidity at $ \sqrt{s_{\text{NN}}} = 5.02\; \text{TeV}$       │                      │                │
│ 10     │ Multiplicity dependence of $\sigma_{\psi(2S)}/\sigma_{J/\psi}$ in $pp$           │ Colombo, T.          │ 2023-12-23     │
│        │ collisions at $\sqrt{s}=13$ TeV                                                  │                      │                │
└────────┴──────────────────────────────────────────────────────────────────────────────────┴──────────────────────┴────────────────┘```
```

## References

* [OpenAIRE APIs for developers](https://egi.openaire.eu/develop)
* [Zenodo Community dump](https://zenodo.org/records/10521976)
  

