from flask import Flask, render_template, request

# import AiClassifyText
import WordClassDB
import NTRS


app = Flask(__name__, template_folder='static')
db = WordClassDB.WordClassDB("WordClass.db")
db.clear_duplicates()


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    keywords = AiClassifyText.classify(query)
    document_ids = db.get_papers_by_keywords(keywords)[:5]

    results = list()
    for document_id in document_ids:
        results.append(NTRS.get_document(document_id).json())

    return render_template(
        'search.html',
        query=query,
        results=results,
        results_count=len(results),
        results_plural="s" if len(results) != 1 else "",
        NTRS=NTRS.HOST
    )

@app.route('/favicon', methods=['GET'])
def main():
    return render_template('favicon.ico')


if __name__ == '__main__':
	app.run(debug=True, use_reloader=False)