class Query:
    def __init__(self, sql="", var=None, params=None, conn=None):
        self.sql = sql
        self.params = params
        self.conn = conn
        self.var = var
        self.last_row_id = 0

        self.cur = self.conn.cursor()
        self.result = None

    def execute(self):
        if self.params:
            self.result = self.cur.execute(self.sql, self.params)
        else:
            self.result = self.cur.execute(self.sql)

        self.last_row_id = self.cur.lastrowid
        # if not self.result.returns_rows:
        #    self.result=None

    def set_result(self, params=None):
        if params:
            self.params = params
        self.execute()
        if not self.result.rowcount:
            return None

        return self.last_row_id

    def get_result(self, params=None):
        if params:
            self.params = params
        self.execute()
        for r in self.result:
            if self.var:
                yield dict(zip(self.var, r))
            else:
                return r

    def get_result_list(self, params=None):
        if params:
            self.params = params
        self.execute()
        res = []
        for r in self.result:
            res.append(dict(zip(self.var, r)))
        return res

    def one_result(self, params=None):
        if params:
            self.params = params
        self.execute()
        if self.result:
            for r in self.result:
                if self.var:
                    return dict(zip(self.var, r))
                else:
                    return r
        return None

    def close(self):
        self.cur.close()
