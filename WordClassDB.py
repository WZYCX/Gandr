import sqlite3
import os

class WordClassDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS words (
                paper INTEGER NOT NULL, keyword TEXT NOT NULL)
            """)
        self.conn.commit()

    def get_papers_by_paper(self, paper):
        self.c.execute('SELECT * FROM words WHERE paper=?', (paper))
        return self.c.fetchone()
    
    def get_papers_by_keyword(self, keyword):
        self.c.execute('SELECT * FROM words WHERE keyword=?', (keyword))
        return self.c.fetchall()

    def get_all(self):
        self.c.execute('SELECT * FROM words')
        return self.c.fetchall()

    def get_keywords(self, paper):
        self.c.execute('SELECT keywords FROM words WHERE paper=?', (paper))
        return self.c.fetchone()

    def delete_paper(self, paper):
        self.c.execute('DELETE FROM words WHERE word=?', (paper))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
    
    
    def add_keywords(self,paper,keywords):
        for keyword in keywords:
            self.c.execute('INSERT INTO words VALUES (?, ?)', (paper, keyword))
        self.conn.commit()
        
def store(document_id,keywords):
    WordClassDB("WordClass.db").add_keywords(document_id,keywords)


#WordClassDB("test.db").add_paper(1,"test")

#keywords = ["test","test2","test3"]

#WordClassDB("test.db").add_keywords(1,keywords)
#WordClassDB("test.db").add_keywords(2,keywords[0:2])