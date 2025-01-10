import sqlite3


class Query:
    def __init__(self, sql="", var=None, params=None, conn=None):
        self.sql = sql
        self.params = params
        self.conn = conn
        self.var = var
        self.last_row_id = 0

        self.cur = self.conn.cursor()
        self.result = None

    def _execute(self,params=None):
        if params:
            self.params = params
        if self.params:
            self.cur.execute(self.sql, self.params)
        else:
            self.cur.execute(self.sql)

    def set_result(self, params=None):
        self._execute(params=params)
        self.last_row_id = self.cur.lastrowid
        if not self.result.rowcount:
            return 0
        return self.last_row_id


    def get_result(self, params=None):
        self._execute(params=params)
        self.result=None
        self.result = self.cur.fetchall()

        res = []
        for r in self.result:
            if self.var:
                res.append(dict(zip(self.var, r)))
            else:
                res.append(r)
        return res

    def get_one_result(self, params=None):
        self._execute(params=params)
        self.result=None
        self.result=self.cur.fetchone()
        if self.result:
            if self.var:
                return dict(zip(self.var, self.result))
            else:
                return self.result
        else:
            return ()


    def close(self):
        self.cur.close()

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.close()


if __name__=="__main__":
    connect=sqlite3.connect("../../../data/tickets.db")
    q=Query(sql="SELECT ticket_id,user_id FROM tickets WHERE ticket_id=:ticket_id",conn=connect,var=['id','user'])
    with q as q:
        r=q.get_result(params={"ticket_id":1})
        print(r)
        r=q.get_one_result(params={"ticket_id":1},)
        print(r)
    connect.close()