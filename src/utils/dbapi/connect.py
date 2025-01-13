import logging
from .query import Query
from .exceptions import DBConnectError

logger = logging.getLogger(__name__)



class Connection:
    def __init__(self, connect=None, engine=None):
        self.transaction = False
        self.connect = connect
        self.engine = engine

        # self.connect.isolation_level=None

    @classmethod
    def create_connection(cls, url="",engine=None):
        if url=="" or not engine:
            raise DBConnectError(url)
        engine.paramstyle="named"
        connect = engine.connect(url)

        return cls(connect=connect,engine=engine)


    def create_query(self, sql="", var=None, params=None):
        return Query(sql=sql, var=var, params=params, cursor=self.connect.cursor())

    def b(self):
        if not self.transaction:
            self.transaction = True

    def c(self):
        self.connect.commit()
        if self.transaction:
            self.transaction = False

    def r(self):
        self.connect.rollback()
        if self.transaction:
            self.transaction = False

    def close(self):
        self.connect.close()

