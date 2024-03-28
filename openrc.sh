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
#export OPENAIRE_RESEARCH_PRODUCT="researchProducts"
export OPENAIRE_RESEARCH_PRODUCT="publications"
#export OPENAIRE_RESEARCH_PRODUCT="datasets"
#export OPENAIRE_RESEARCH_PRODUCT="software"
#export OPENAIRE_RESEARCH_PRODUCT="other"

# Data format: YYYY-MM-DD
export OPENAIRE_FROM_DATE_OF_ACCEPTANCE="2023-01-01"
export OPENAIRE_TO_DATE_OF_ACCEPTANCE="2023-12-31"   
export OPENAIRE_OPEN_ACCESS="false"
export OPENAIRE_PAGE_SIZE="10"

# Full list of the OpenAIRE paramenters:
# -openairePublicationID, 
# -fos, 
# -hasWTFunding, 
# -title, 
# -influence, 
# -OA, 
# -fundingStream, 
# -peerReviewed, 
# -popularity, 
# -instancetype, 
# -model, 
# -projectID, 
# -openaireProviderID, 
# -publiclyFunded, 
# -citationCount, 
# -diamondJournal, 
# -green, 
# -author, 
# -FP7ProjectID, 
# -orcid, 
# -hasProject, 
# -community, 
# -hasECFunding, 
# -version, 
# -openAccessColor, 
# -fromDateAccepted, 
# -FP7scientificArea, 
# -sdg, 
# -impulse, 
# -originalId, 
# -doi, 
# -size, 
# -format, 
# -sortBy, 
# -page

export FILENAME="OA_research_products.xml"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"
