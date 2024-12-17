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

import datetime
import json
import os
import requests
import time
import xml.etree.ElementTree as ET
import warnings
warnings.filterwarnings("ignore")

from gspread_formatting import *
from gspreadutils import init_GWorkSheet

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from utils import colourise, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.4"
__date__      = "$Date: 09/12/2024 18:23:17"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def configure_headers(env, worksheet):
    ''' Initialize headers of the GSpread Worksheet '''

    print(colourise("green", "\n[%s]" %env['LOG']), \
    "Initialise the headers of the GWorkSheet '%s' in progress..." %env['GOOGLE_SHEET_NAME'])
    print("\tThis operation may take few minutes to complete. Please wait!")

    # Clear all the cells of the GWorkSheet
    worksheet.batch_clear(["A1:E3000"])

    # Clearing the note of the cell
    pos_cell = worksheet.find(env['OPENAIRE_RESEARCH_OBJECT'])
    if pos_cell:
       worksheet.clear_note("B" + str(pos_cell.row))

    # Defining the headers of the GWorkSheet
    text_fmt = cellFormat(
         backgroundColor=color(1, 1, 0), # Yellow
         borders = borders(bottom = border('SOLID')),
         padding = padding(bottom = 3),
         horizontalAlignment = 'CENTER',
         textFormat = textFormat(
         bold = True,
         fontFamily = 'DM Sans',
         strikethrough = False,
         underline = False
    ))

    # Adding the headers to the GWorkSheet
    format_cell_range(worksheet, 'A1:E1', text_fmt)
    worksheet.update_acell("A1", "RO")
    worksheet.update_acell("B1", "Total")
    worksheet.update_acell("C1", "From")
    worksheet.update_acell("D1", "To")
    
    format_cell_range(worksheet, 'A8:E8', text_fmt)
    worksheet.update_acell("A8", "#")
    worksheet.update_acell("B8", "Title (of the Research Object) - " + env['OPENAIRE_RESEARCH_OBJECT'])
    worksheet.update_acell("C8", "Authors")
    worksheet.update_acell("D8", "Publisher")
    worksheet.update_acell("E8", "Date of Acceptance")


def get_OpenAIRE_Research_Products(env, research_product): 
    ''' Get the full list of Research Products from the OpenAIRE dashboard '''
  
    # Saving the list of OpenAIRE Research Products in the XML file 
    with open(os.getcwd() + "/" + env['FILENAME'], 'wb') as f: 
    
         with Progress(
                 SpinnerColumn(),
                 TextColumn("[progress.description]{task.description}"),
                 TimeElapsedColumn(),
                 transient=False,
         ) as progress:
              task = progress.add_task(
                      "[yellow]Downloading (" + research_product + ") in progress...", 
                      total = 1 
                     )

              # Do the work...
              url = env['OPENAIRE_API_SERVER_URL'] \
                  + "search/" + research_product \
                  + "?community=" + env['OPENAIRE_COMMUNITY'] \
                  + "&fromDateAccepted=" + env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'] \
                  + "&toDateAccepted=" + env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'] \
                  + "&sortBy=resultdateofacceptance,descending"

              resp = requests.get(url)
    
              while not progress.finished:
                    progress.update(task, advance = 0.5)
                    time.sleep(1)
        
              f.write(resp.content)
              f.close()


def get_research_object(env, page_index):
    ''' Get the list of research object '''

    print(colourise("green", "\n[INFO]"), \
    "Downloading [RO: %s] *%s* from page [%s] in progress..." \
    %(env['OPENAIRE_RESEARCH_OBJECT'], env['OPENAIRE_PAGE_SIZE'], page_index))

    # Saving the list of OpenAIRE Research Products in the XML file 
    with open(os.getcwd() + "/" + env['FILENAME'], 'wb') as f:

         url = str(env['OPENAIRE_API_SERVER_URL']) \
             + "search/" + env['OPENAIRE_RESEARCH_OBJECT'] \
             + "?community=" + env['OPENAIRE_COMMUNITY'] \
             + "&fromDateAccepted=" + str(env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE']) \
             + "&toDateAccepted=" + str(env['OPENAIRE_TO_DATE_OF_ACCEPTANCE']) \
             + "&page=" + str(page_index) \
             + "&size=" + str(env['OPENAIRE_PAGE_SIZE']) \
             + "&sortBy=resultdateofacceptance,descending"

         print(url)    

         response = requests.get(url)
         f.write(response.content)


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
    research_products = {"publications", "datasets", "software", "other"}
    duplicates = []
    publications = []

    env = get_env_settings()
    verbose = env['LOG']
    print("\nVerbose Level = %s" %colourise("cyan", verbose))

    print(colourise("cyan", "\n[%s]" %env['LOG']), "Environmental settings")
    if verbose == "DEBUG":
       print(json.dumps(env, indent=4))

    # Initialize the GSpreads Worksheet
    worksheet = init_GWorkSheet(env)

    # 1. Initialize the headers of the GSpread Worksheet
    configure_headers(env, worksheet)

    # 2. Get the full list of the OpenAIRE Research Products
    print(colourise("cyan", "\n[%s]" %env['LOG']), \
    "Downloading *Research Products* from the EGI's OpenAIRE dashboard in progress")
    print("\tThis operation may take few minutes to complete. Please wait!\n")
    
    console = Console()
    table = Table(show_header = True, header_style = "bold magenta")
    table.add_column("OpenAIRE Research Products", style = "dim", width = 30)
    table.add_column("Total", justify = "right")
    table.add_column("From")
    table.add_column("To")

    table_pub = Table(show_header = True, header_style = "bold magenta")
    table_pub.add_column("#", style = "dim", width = 7)
    table_pub.add_column("Title", style = "dim", width = 82)
    table_pub.add_column("Creator(s)", width = 20)
    table_pub.add_column("DateOfAcceptance", width = 13)

    # Define the header settings
    text_fmt = cellFormat(
         textFormat = textFormat(
         bold = False,
         fontFamily = 'DM Sans',
         strikethrough = False,
         underline = False),
         horizontalAlignment = 'RIGHT'
    )

    index = 1
    tot_publications = 0
    tot_software = 0
    tot_datasets = 0
    tot_other = 0
    for product in research_products:
        get_OpenAIRE_Research_Products(env, product)
        # Parse the XML file
        tot_research_product, research_products = parseXML(env)
        if "publications" in product:
            tot_publications = tot_research_product
            # Adding extra rows (if needed)
            if worksheet.row_count < int(tot_publications):
               worksheet.add_rows(int(tot_publications) - 1000)

        if "software" in product:
            tot_software = tot_research_product
            # Adding extra rows (if needed)
            if worksheet.row_count < int(tot_software):
               worksheet.add_rows(int(tot_software) - 1000)

        if "datasets" in product:
            tot_datasets = tot_research_product
            # Adding extra rows (if needed)
            if worksheet.row_count < int(tot_datasets):
               worksheet.add_rows(int(tot_datasets) - 1000)       

        if "other" in product:
            tot_other = tot_research_product
            # Adding extra rows (if needed)
            if worksheet.row_count < int(tot_other):
               worksheet.add_rows(int(tot_other) - 1000)               

        table.add_row(
             "-" + str(product),
             str(tot_research_product),
             env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'],
             env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'])
       
        _range = "A" + str(index + 1) + ":" + "E" + str(index + 1)
        format_cell_range(worksheet, _range, text_fmt)

        worksheet.update_cell(index + 1, 1, product)
        worksheet.update_cell(index + 1, 2, str(tot_research_product))
        worksheet.update_cell(index + 1, 3, env['OPENAIRE_FROM_DATE_OF_ACCEPTANCE'])
        worksheet.update_cell(index + 1, 4, env['OPENAIRE_TO_DATE_OF_ACCEPTANCE'])

        index = index + 1
    
    print(colourise("green", "\n[INFO]"), \
    "Breakdown of the OpenAIRE Research Products [%s] in the reporting period" %env['OPENAIRE_RESEARCH_OBJECT'])
    console.print(table)

    # 3. Retrieve the full list of *Research Objects* from the dashboard
    duplicates = []
    research_objects = []

    page_index = 1 
    pos = 1

    if env['OPENAIRE_RESEARCH_OBJECT'] == "publications":
       max_pages = round(int(tot_publications) // int(env['OPENAIRE_PAGE_SIZE']) + 1)
       print(colourise("green", "[INFO]"), \
       "Total research objects = %s, Max pages = %s, Page Size = %s" \
       %(tot_publications, max_pages, env['OPENAIRE_PAGE_SIZE']))

    if env['OPENAIRE_RESEARCH_OBJECT'] == "software":
       max_pages = round(int(tot_software) // int(env['OPENAIRE_PAGE_SIZE']) + 1)
       print(colourise("green", "[INFO]"), \
       "Total research objects = %s, Max pages = %s, Page Size = %s" \
       %(tot_software, max_pages, env['OPENAIRE_PAGE_SIZE']))       

    if env['OPENAIRE_RESEARCH_OBJECT'] == "datasets":
       max_pages = round(int(tot_datasets) // int(env['OPENAIRE_PAGE_SIZE']) + 1)
       print(colourise("green", "[INFO]"), \
       "Total research objects = %s, Max pages = %s, Page Size = %s" \
       %(tot_datasets, max_pages, env['OPENAIRE_PAGE_SIZE']))

    if env['OPENAIRE_RESEARCH_OBJECT'] == "other":
       max_pages = round(int(tot_other) // int(env['OPENAIRE_PAGE_SIZE']) + 1)
       print(colourise("green", "[INFO]"), \
       "Total Research Objects = %s, Max pages = %s, Page size = %s" \
       %(tot_other, max_pages, env['OPENAIRE_PAGE_SIZE']))   


    for page_index in range(max_pages):
        get_research_object(env, page_index + 1)
        # Parse the XML file
        tot_research_product, research_products = parseXML(env)

        try:
            for research_object in research_products:
                # Check if research_object['Title'] is NOT a duplicate
                if research_object['Title'] not in research_objects:
                   research_objects.append(research_object['Title'])

                   # Publish into the GSpread Worksheet
                   print(colourise("yellow", "[INFO]"), \
                   "%s) [Title]: %s [..], [Authors]: %s, [Publisher]: %s, [Date]: %s" \
                   %(pos, research_object['Title'][0:150], research_object['Creator(s)'],
                          research_object['Publisher'], research_object['DateOfAcceptance']))

                   worksheet.update_cell(pos + 8, 1, pos)
                   worksheet.update_cell(pos + 8, 2, research_object['Title'])
                   worksheet.update_cell(pos + 8, 3, research_object['Creator(s)'])
                   worksheet.update_cell(pos + 8, 4, research_object['Publisher'])
                   worksheet.update_cell(pos + 8, 5, research_object['DateOfAcceptance'])

                   pos = pos + 1     

                elif research_object['Title'] not in duplicates:
                     duplicates.append(research_object['Title'])
                     print(colourise("red", "[INFO]"), \
                     "[DUPLICATE FOUND] - SKIPPING REGISTRATION OF THE PUBLICATION!")
                     pri nt(colourise("red", "[DEBUG]"), \
                     "[Title]: %s [..], [Authors]: %s, [Publisher]: %s, [Date]: %s" \
                     %(research_object['Title'][0:150], research_object['Creator(s)'],
                     research_object['Publisher'], research_object['DateOfAcceptance']))
    
        except:
           print(colourise("red", "[WARNING]"), \
           "Quota exceeded for metrics: 'Write requests', 'Write requests per minute'")
           time.sleep (120)
           pos = pos - 1


    if len(duplicates):
       print(colourise("red", "\n[WARNING]"), \
       "A total of [%d] duplications have been detected!" %len(duplicates))
    
       with open(os.getcwd() + "/" + env['DUPLICATES'], 'w') as f:
           for item in duplicates:
               f.write("%s\n" %item)
       
       f.close()        
       
       print(colourise("green", "[INFO]"), \
       " See the file [%s] for more details" %env['DUPLICATES'])

       # Identify the proper cell and add a note...
       pos_cell = worksheet.find(env['OPENAIRE_RESEARCH_OBJECT'])
       worksheet.insert_note("B" + str(pos_cell.row), "duplications: " + str(len(duplicates)))

    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS 
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

    # Update timestamp of the last update
    worksheet.insert_note("A1","Last update on: \n" + timestamp)   


if __name__ == "__main__":
        main()

