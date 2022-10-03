![GANDR](https://sa-2019.s3.amazonaws.com/media/images/tAsjyXh.2e16d0ba.fill-591x300.png)

[Gandr](https://takeagandr.herokuapp.com) is an AI powered search engine that utilizes indexes generated through Natural Language Processing (NLP) to assist researchers in finding reports. To do this we leveraged NLP to process text from documents on the NASA Technical Report Server (NTRS) and summarize them into a collection of keywords.

Gandr is our submission for the 2022 [NASA Space Apps Challenge](https://www.spaceappschallenge.org/)


## Overview
Gandr uses Spacy's NLP model to process text and generate tokens, then using the tokens, and the frequency of each tokenized word, it generates a list of keywords which is stored in a SQL database along with the document id.

To create our corpus, we created an algorithm to asynchronously scrape the NTRS and then index each document. Having the scraper run throughout our project, we were able to index more than 25,000 documents.

With our corpus in place we created a Flask web application. The site has a simple user interface which allows users to enter a query which is sent to the server and tokenized to generate a list of keywords. The keywords are matched with the database to find the most relevant documents, which are returned back to the user in an easily accessible format.

The NTRS database takes several inputs such as a search query, the authors' names, date, document type, etc. Most users are not able to make use of most of these fields. However, while the search function certainly is useful, it only queries the titles and abstracts, which not all documents contain (the abstracts that is), and can only hold so much information about the actual document.

Our project allows for a more inclusive method of querying the NTRS, by allowing users to make searches that are relevant to entire documents.

All scripts are written in python. We used SpaCy's NLP model to help us analyize lexical data. asyncio and AIOHTTP were used to scrape files from the NTRS. We used SQLite3 to create and interact with our SQL database. Our front end was created using the Flask framework, with the individual pages structured and styled with HTML and CSS.

## Video Demonstration
[![image](https://raw.githubusercontent.com/WZYCX/Word-Classification-AI/main/app/static/thumbnail.png)](https://www.youtube.com/watch?v=OLUS1lEPJjs)
