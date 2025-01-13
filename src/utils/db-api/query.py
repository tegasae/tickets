from exceptions import DBOperationError




class Query:
    def __init__(self, sql="", var=None, params:dict=None,conn=None,cursor=None):
        self.sql = sql
        self.params = params
        #self.conn = conn
        self.var = var
        self.last_row_id = 0

        #self.cur = self.conn.cursor()
        self.cur=cursor
        self.result = None
        self.count=0

    def _execute(self,params:dict=None):
        if params:
            self.params = params
        try:
            if self.params:
                self.cur.execute(self.sql, self.params)
            else:
                self.cur.execute(self.sql)
        except self.cur.connection.OperationalError as e:
            raise DBOperationError(e)

    def set_result(self, params:dict=None):
        self.last_row_id=0
        self.count=0
        try:
            self._execute(params=params)
            self.count=self.cur.rowcount
            if self.count:
                self.last_row_id = self.cur.lastrowid
        except self.cur.connection.ProgrammingError as e:
            raise DBOperationError(e)
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


