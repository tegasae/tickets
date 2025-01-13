import sqlite3


from connect import Connection

if __name__=="__main__":
    create_conn=Connection.create_connection("../../../data/tickets.db",engine=sqlite3)

    query=create_conn.create_query(sql="SELECT ticket_id, user_id FROM tickets WHERE user_id=:user_id",
                                   var=["ticket_id","user_id"],params={"user_id":2})
    query_insert=create_conn.create_query(sql="INSERT INTO tickets (user_id) VALUES (:user_id)",params={"user_id":100})

    query_update=create_conn.create_query(sql="UPDATE tickets SET user_id=user_id+1 WHERE user_id=:user_id")
    query_delete = create_conn.create_query(sql="DELETE FROM tickets WHERE user_id=:user_id")
    create_conn.b()
    r=query.get_result()

    print(r)
    i=query_insert.set_result()
    i = query_insert.set_result()
    i = query_insert.set_result()

    print(i)
    u=query_update.set_result(params={"user_id":i+100000})
    print(u)
    d = query_delete.set_result(params={"user_id": 100})
    print(d)
    create_conn.c()
    create_conn.close()