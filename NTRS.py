import asyncio
import aiohttp
import requests
import WordClassDB
import AiClassifyText

# Removes certificate verification warning from requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


API = 'https://www.ntrs.nasa.gov/api/'
HEADERS = {"Host": "ntrs.nasa.gov"}


# Gets the documents using the document ids from the NTRS API asyncronously

async def _get(document_ids, classify, store):

    async with aiohttp.ClientSession() as session:
        for document_id in document_ids:
            url = API + f"citations/{document_id}/downloads/{document_id}.txt"

            async with session.get(url, headers=HEADERS, ssl=False) as response:

                if response.status != 200:
                    continue
                text = await response.text()

            keywords = classify(text)
            store(document_id, keywords)

def async_get(document_ids, function):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_get(document_ids, function))


# Gets the documents using the document ids from the NTRS API

def get(document_ids):

    for document_id in document_ids:
            url = API + f"citations/{document_id}/downloads/{document_id}.txt"
            response = requests.get(url, headers=HEADERS, verify=False)

            if response.status_code != 200:
                continue

            keywords = AiClassifyText.classify(response.text) # we could move this and the next line to a separate function
            WordClassDB.store(document_id, keywords)
      
            
get(["20190000001"])