from app.scan.run import startscan_process
from app.scan.conn import dbconn

def scheduler_scan(id, current_user):
    conn, cursor = dbconn()
    sql = "SELECT target_status from Target WHERE id=%s AND (target_status = 7 or target_status = 0)"
    result = cursor.execute(sql,(id))
    if(result):
        sql = "UPDATE Target SET target_status=%s WHERE id=%s"
        cursor.execute(sql,(1, id))
        conn.commit()
    cursor.close()
    conn.close()

    startscan_process(id, current_user)
    return