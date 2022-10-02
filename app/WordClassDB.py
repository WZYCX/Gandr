import sqlite3


class WordClassDB:

    def __init__(self, db_name):

        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS words (
                paper INTEGER NOT NULL, keyword TEXT NOT NULL)
            """)
        self.conn.commit()

    def get_papers_by_paper(self, paper):
        self.c.execute('SELECT * FROM words WHERE paper=?', (paper,))
        return self.c.fetchone()

    def get_papers_by_keyword(self, keyword):
        self.c.execute('SELECT paper FROM words WHERE keyword=?', (keyword,))
        return self.c.fetchall()

    def get_papers_by_keywords(self, keywords):
        def key(paper):
            return count_document_ids[paper]
        document_ids = list()
        for keyword in keywords:
            document_ids += self.get_papers_by_keyword(keyword)
        count_document_ids = dict()
        for document_id in document_ids:
            if document_id[0] in count_document_ids:
                count_document_ids[document_id[0]] += 1
            else:
                count_document_ids[document_id[0]] = 1
        return sorted(count_document_ids.keys(), key=key, reverse=True)

    def get_all(self):
        self.c.execute('SELECT * FROM words')
        return self.c.fetchall()

    def get_keywords(self, paper):
        self.c.execute('SELECT keywords FROM words WHERE paper=?', (paper,))
        return self.c.fetchone()

    def delete_paper(self, paper):
        self.c.execute('DELETE FROM words WHERE word=?', (paper,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def add_keywords(self,paper,keywords):
        for keyword in keywords:
            self.c.execute('INSERT INTO words VALUES (?, ?)', (paper, keyword))
        self.conn.commit()

    def already_indexed(self, paper):
        self.c.execute('SELECT * FROM words WHERE paper=?', (paper,))
        return self.c.fetchone() is not None

    def clear_duplicates(self):
        self.c.execute('DELETE FROM words WHERE rowid NOT IN (SELECT MIN(rowid) FROM words GROUP BY paper, keyword)')
        self.conn.commit()


#WordClassDB("test.db").add_paper(1,"test")

#keywords = ["test","test2","test3"]

#WordClassDB("test.db").add_keywords(1,keywords)
#WordClassDB("test.db").add_keywords(2,keywords[0:2])