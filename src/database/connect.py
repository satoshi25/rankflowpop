from dotenv import load_dotenv
import pymysql
import os


load_dotenv()

conn = pymysql.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSEORD"),
    port=int(os.getenv("PORT")),
    db=os.getenv("DB"),
    charset=os.getenv("CHARSET"),
)

cur = conn.cursor()

