import sqlite3,traceback,json

class Database:
    def __init__(self, name) -> None:
        self.conn=sqlite3.connect(f"{name}.db",check_same_thread=False)
        self.cursor=self.conn.cursor()
        query1="CREATE TABLE IF NOT EXISTS main(x TEXT PRIMARY KEY,y TEXT)"
        self.cursor.execute(query1)
        self.conn.commit()
    def set(conn,key,val,iterations=0):
        val=json.dumps(val)
        try:
            cursor=conn.conn.cursor()
            cursor.execute("SELECT * FROM main WHERE x = ?",(key,))
            if len(cursor.fetchall())==0:
                query2="INSERT INTO main VALUES (?,?)"
                cursor.execute(query2,(key,val))
                conn.conn.commit()
            else:
                cursor.execute("UPDATE main SET y = ? WHERE x = ?",(val,key))
                conn.conn.commit()
        except Exception as e:
            if iterations>4:
                traceback.print_exc()
                raise e
            set(conn,key,val,iterations+1)
    def get(conn,key,iterations=0):
        try:
            cursor=conn.conn.cursor()
            cursor.execute("SELECT * FROM main WHERE x = ?",(key,))
            data=cursor.fetchall()
            if len(data)==0:
                return False
            return json.loads(list(data[0])[1])
        except Exception as e:
            if iterations>4:
                traceback.print_exc()
                raise e
            return get(conn,key,iterations+1)