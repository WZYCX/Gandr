import asyncio
from urllib.parse import urlencode

import NTRS
import AiClassifyText
import WordClassDB


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
db = WordClassDB.WordClassDB("WordClass.db")


async def async_index_all():
    params = {
        "sort.field": "published",
        "sort.order": "asc",
        "page.size": 100,
        "page.from": 0
    }

    url = "/api/citations/search?" + urlencode(params)
    json = await NTRS.async_get_json(url)
    total = json["stats"]["total"]
    indexed = 0

    while True:
        print(params["page.from"], "to", params["page.from"]+99, "out of", total)
        for document in json["results"]:
            document_id = document["id"]

            # Checks to see if the document has a file available to be downloaded
            if not document["downloadsAvailable"]:
                continue

            url = None
            for download in document["downloads"]:
                if "fulltext" in download["links"]:
                    url = download["links"]["fulltext"]

            if url is None:
                continue

            if db.already_indexed(document_id):
                continue

            # Downloads the file associated with the document id
            text = await NTRS.async_get_text(url)

            # Classifies the text and stores the keywords
            keywords = AiClassifyText.classify(text, 20)
            db.add_keywords(document_id, keywords)
            indexed += 1

        print("Indexed", indexed, "documents", end="\n\n")
        indexed = 0

        params["page.from"] += params["page.size"]
        if params["page.from"] >= total:
            break

        url = "/api/citations/search?" + urlencode(params)
        json = await NTRS.async_get_json(url)


def index_all():
    params = {
        "sort.field": "published",
        "sort.order": "asc",
        "page.size": 100,
        "page.from": 0
    }

    response = NTRS.get("/api/citations/search?" + urlencode(params))
    data = response.json()
    total = data["stats"]["total"]
    indexed = 0
    total_indexed = 0

    while True:
        print(params["page.from"], "to", params["page.from"]+99, "out of", total)
        for document in data["results"]:
            document_id = document["id"]

            # Checks to see if the document has a file available to be downloaded
            if not document["downloadsAvailable"]:
                continue

            url = None
            for download in document["downloads"]:
                if "fulltext" in download["links"]:
                    url = download["links"]["fulltext"]

            if url is None:
                continue

            if db.already_indexed(document_id):
                continue

            # Downloads the file associated with the document id
            response = NTRS.get(url)

            # Classifies the text and stores the keywords
            keywords = AiClassifyText.classify(response.text, 20)
            db.add_keywords(document_id, keywords)
            indexed += 1

        total_indexed += indexed
        print("Indexed", indexed, "documents", end="\n\n")
        print("Total Indexed:", total_indexed, end="\n\n")
        indexed = 0

        params["page.from"] += params["page.size"]
        if params["page.from"] >= total:
            break

        response = NTRS.get("/api/citations/search?" + urlencode(params))
        data = response.json()


# index_all()
asyncio.run(async_index_all())