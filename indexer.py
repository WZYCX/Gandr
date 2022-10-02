import asyncio
from urllib.parse import urlencode

import NTRS
import AiClassifyText
import WordClassDB


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
db = WordClassDB.WordClassDB("WordClass.db")
db.clear_duplicates()


async def async_index_all():
    params = {
        "sort.field": "published",
        "sort.order": "desc",
        "page.size": 100,
        "page.from": 0,
        # "published.lte": "2021-03-22"
    }

    url = "/api/citations/search?" + urlencode(params)
    json = await NTRS.async_get_json(url)
    total = json["stats"]["total"]
    total_indexed = 0
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
            keywords = AiClassifyText.classify(text)[:20]
            db.add_keywords(document_id, keywords)
            indexed += 1

        total_indexed += indexed
        print(f"Indexed {indexed} documents ({total_indexed} so far)", end="\n\n")
        indexed = 0

        params["page.from"] += params["page.size"]
        if params["page.from"] >= total:
            break

        # NTRS only allows pages up to 10000
        if params["page.from"] >= 10000:
            print("Searching documents from before", document["distributionDate"][:10])
            params["published.lte"] = document["distributionDate"][:10]
            params["page.from"] = 0

        url = "/api/citations/search?" + urlencode(params)
        json = await NTRS.async_get_json(url)
        total = json["stats"]["total"]


asyncio.run(async_index_all())