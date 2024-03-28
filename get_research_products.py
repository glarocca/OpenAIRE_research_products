#!/usr/bin/env python3
#
#  Copyright 2024 EGI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import os
import requests
import xml.etree.ElementTree as ET
from utils import colourise, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.4"
__date__      = "$Date: 27/03/2024 18:23:17"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_OpenAIRE_Research_Products(env): 
    ''' Get the full list of Open Access Research Products from the OpenAIRE dashboard '''
  
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "publications":
          url = env['OPENAIRE_API_SERVER_URL'] \
              + "search/" + env['OPENAIRE_RESEARCH_PRODUCT'] +"?community=" + env['OPENAIRE_COMMUNITY'] \
              + "&fromDateAccepted=" + env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'] \
              + "&toDateAccepted=" + env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'] \
              + "&size=" + env['OPENAIRE_PAGE_SIZE'] \
              + "&OA=" + env['OPENAIRE_OPEN_ACCESS'] \
              + "&sortBy=resultdateofacceptance,descending"
    else:
        url = env['OPENAIRE_API_SERVER_URL'] \
              + "search/" + env['OPENAIRE_RESEARCH_PRODUCT'] +"?community=" + env['OPENAIRE_COMMUNITY'] \
              + "&fromDateAccepted=" + env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'] \
              + "&toDateAccepted=" + env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'] \
              + "&size=" + env['OPENAIRE_PAGE_SIZE'] \
              + "&sortBy=resultdateofacceptance,descending"

    #print(url)
    resp = requests.get(url) 

    # Saving the list of OpenAIRE Research Products in the XML file 
    with open(os.getcwd() + "/" + env['FILENAME'], 'wb') as f: 
        f.write(resp.content)


def parseXML(env):
    ''' Parsing the XML file and return a list[] of OpenAIRE Research Products '''

    # Create element tree object
    tree = ET.parse(os.getcwd() + "/" + env['FILENAME'])
    # Get root element
    root = tree.getroot()

    # Initialize the variables
    title = acceptance = creator = subject = publisher = ""
    size = page = tot_publications = 0
    publication = {}
    publications = []

    for child in root:
        if child.tag == "header":
           for entry in child:
               #print("[.] %s, %s" %(entry.text, entry.tag))
               if entry.tag == "size":
                   size = entry.text
               if entry.tag == "page":
                   page = entry.text
               if entry.tag == "total":
                   tot_publications = entry.text
    
    for results in root.findall('./results/result/metadata/'):
        for child in results:
            if child.tag == "{http://namespace.openaire.eu/oaf}result":
               for entry in child:
                   #print("[LOG] %s, %s" %(entry.tag, entry.text))
                   if entry.tag == "title":
                      title = entry.text
                   if entry.tag == "creator":
                      creator = entry.text
                   if entry.tag == "subject":
                      subject = entry.text
                   if entry.tag == "publisher":
                      publisher = entry.text
                   if entry.tag == "dateofacceptance":
                      acceptance = entry.text

                   publication = {
                     "Title": title,
                     "Creator(s)": creator,
                     "Subject": subject,
                     "Publisher": publisher,
                     "DateOfAcceptance" : acceptance
                   }

               publications.append(publication)

    return(tot_publications, publications)



def main():

    # Initialise the environment settings
    research_products = []
    tot_research_products = 0

    env = get_env_settings()
    verbose = env['LOG']
    print("\nVerbose Level = %s" %colourise("cyan", verbose))

    print(colourise("cyan", "\n[INFO]"), "\tEnvironment settings")
    if verbose == "DEBUG":
       print(json.dumps(env, indent=4))

    # Download the full list of the OpenAIRE Research Products
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "publications":
       print(colourise("cyan", "\n[INFO]"), \
               "\tDownload the list of *PUBLICATIONS* from the EGI's OpenAIRE dashboard in progress..")
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "datasets":
       print(colourise("cyan", "\n[INFO]"), \
               "\tDownload the list of *DATASETS* from the EGI's OpenAIRE dashboard in progress..")
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "sotfware":
       print(colourise("cyan", "\n[INFO]"), \
               "\tDownload the list of *SOFTWARE* from the EGI's OpenAIRE dashboard in progress..")
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "other":
       print(colourise("cyan", "\n[INFO]"), \
               "\tDownload the *OTHER research products* from the EGI's OpenAIRE dashboard in progress..")
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "researchProducts":
       print(colourise("cyan", "\n[INFO]"), \
               "\tDownload the list of *RESEARCH PRODUCTS* from the EGI's OpenAIRE dashboard in progress..")
    
    print("\tThis operation may take few minutes. Please wait!")
    get_OpenAIRE_Research_Products(env)

    # Parse the XML file
    tot_research_products, research_products = parseXML(env)

    if env['OPENAIRE_OPEN_ACCESS'] == 'true':
       print(colourise("cyan", "\n[INFO]"), \
            "\tList of the first [%s] Open Access Publications" %env['OPENAIRE_PAGE_SIZE'])
    else:
       print(colourise("cyan", "\n[INFO]"), \
            "\tList of the first [%s] Publications" %env['OPENAIRE_PAGE_SIZE'])

    for research_product in research_products:
        print(json.dumps(research_product, indent=4))
    
    print(colourise("green", "\n[SUMMARY REPORT]"))
    print("- OpenAIRE Research Products")
    if env['OPENAIRE_RESEARCH_PRODUCT'] == "publications":
       if env['OPENAIRE_OPEN_ACCESS'] == "false":
          print(colourise("green", "[INFO]"), env['OPENAIRE_RESEARCH_PRODUCT'].upper())
       else:   
          print("  |--> Type = Open Access Publications")
    else:      
          print(colourise("green", "[INFO]"), env['OPENAIRE_RESEARCH_PRODUCT'].upper())

    print("  |--> Total = %s" %tot_research_products)
    print(colourise("green", "[REPORTING PERIOD]"))
    print("  |--> From = %s" %env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'])
    print("  |--> To = %s" %env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'])
    

if __name__ == "__main__":
        main()

