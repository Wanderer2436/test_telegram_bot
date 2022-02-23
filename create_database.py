import bs4
import requests
import sqlite3


connection = sqlite3.connect('anekdot.db')
cursor = connection.cursor()
cursor.executescript("""create table anekdot(id int auto_increment primary key, anekdot longtext);""")
for _ in range(10):
    s = requests.get('http://anekdotme.ru/random')
    bs = bs4.BeautifulSoup(s.text, "html.parser")
    p = bs.select('.anekdot_text')
    for x in p:
        s = (x.getText().strip())
        cursor.execute("INSERT INTO anekdot (anekdot) VALUES ('"+s+"')")
        connection.commit()
connection.close()
