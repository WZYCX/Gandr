import asyncio

import WordClassDB
import AiClassifyText
import NTRS


async def main():
    db = WordClassDB.WordClassDB("WordClassDB copy.db")
    db.clear_duplicates()

    query = "How can we shield against radiation from space?"
    print(query)

    keywords = AiClassifyText.classify(query)
    print(keywords) # ['shield', 'radiation', 'space']

    document_ids = db.get_papers_by_keywords(keywords)[:5]
    print(document_ids)

    for document_id in document_ids:
        url = "/api/citations/" + str(document_id)
        document = await NTRS.async_get_json(url)
        print(document["title"])


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(main())
loop.run_until_complete(future)