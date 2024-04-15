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
import time
import xml.etree.ElementTree as ET

from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from utils import colourise, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.6"
__date__      = "$Date: 15/04/2024 18:23:17"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_OpenAIRE_Research_Products(env, research_product): 
    ''' Get the full list of Open Access Research Products from the OpenAIRE dashboard '''
  
    url = env['OPENAIRE_API_SERVER_URL'] \
          + "search/" + research_product \
          + "?community=" + env['OPENAIRE_COMMUNITY'] \
          + "&fromDateAccepted=" + env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'] \
          + "&toDateAccepted=" + env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'] \
          + "&size=" + env['OPENAIRE_PAGE_SIZE'] \
          + "&sortBy=resultdateofacceptance,descending"

    resp = requests.get(url) 

    # Saving the list of OpenAIRE Research Products in the XML file 
    with open(os.getcwd() + "/" + env['FILENAME'], 'wb') as f: 
    
         with Progress() as progress:
              task = progress.add_task(
                      "[yellow]Downloading (" +research_product +")", 
                      total = int(env['OPENAIRE_PAGE_SIZE'])
                    )
    
              while not progress.finished:
                    progress.update(task, advance = 0.5)
                    time.sleep(0.05)
        
         f.write(resp.content)


def parseXML(env):
    ''' Parsing the XML file and return a list[] of OpenAIRE Research Products '''

    # Create element tree object
    tree = ET.parse(os.getcwd() + "/" + env['FILENAME'])
    # Get root element
    root = tree.getroot()

    # Initialize the variables
    title = acceptance = creator = subject = publisher = ""
    size = page = tot_research_products = 0
    research_product = {}
    research_products = []

    for child in root:
        if child.tag == "header":
           for entry in child:
               #print("[.] %s, %s" %(entry.text, entry.tag))
               if entry.tag == "size":
                   size = entry.text
               if entry.tag == "page":
                   page = entry.text
               if entry.tag == "total":
                   tot_research_products = entry.text
    
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

                   research_product = {
                     "Title": title,
                     "Creator(s)": creator,
                     "Subject": subject,
                     "Publisher": publisher,
                     "DateOfAcceptance" : acceptance
                   }

               research_products.append(research_product)

    return(tot_research_products, research_products)



def main():

    # Initialise the environment settings
    research_products = []
    tot_research_product = 0
    research_products = {"publications", "datasets", "software", "other", "researchProducts"}

    env = get_env_settings()
    verbose = env['LOG']
    print("\nVerbose Level = %s" %colourise("cyan", verbose))

    print(colourise("cyan", "\n[%s]" %env['LOG']), " Variables settings")
    if verbose == "DEBUG":
       print(json.dumps(env, indent=4))

    # Download the full list of the OpenAIRE Research Products
    print(colourise("cyan", "\n[%s]" %env['LOG']), \
               " Downloading *Research Products* from the EGI's OpenAIRE dashboard in progress")
    print("\t This operation may take few minutes to complete. Please wait!\n")
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("OpenAIRE Research Products", style="dim", width=30)
    table.add_column("Total", justify="right")
    table.add_column("From")
    table.add_column("To")
    
    for product in research_products:
        get_OpenAIRE_Research_Products(env, product)
        # Parse the XML file
        tot_research_product, research_products = parseXML(env)

        if "researchProducts" in product:
           table.add_row(
             "[red]-" + product + "[/red]", 
             "[bold]" + tot_research_product + "[/bold]", 
             env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'],
             env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'])

        else:
           table.add_row(
             "-" + product, 
             tot_research_product, 
             env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'],
             env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'])
    
    print(colourise("green", "\n[REPORT]"))
    console.print(table)


if __name__ == "__main__":
        main()

