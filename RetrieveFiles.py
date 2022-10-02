import AiClassifyText
import WordClassDB

def processQuery(query):
    keywords = AiClassifyText.classify(query, int(abs(len(query.split())/2))) #int(abs(len(query)/2)) can be changed to whatever
    return keywords

def retrieve(keywords):
    db = WordClassDB.WordClassDB("WordClass.db")
    papers = []
    for keyword in keywords:
        current = db.get_papers_by_keyword(keyword)
        if current not in papers:
            papers.append(current)
    return papers

#tests

queryKeywords = processQuery("How can we shield against radiation from space?")
print(queryKeywords)
print(retrieve(queryKeywords))