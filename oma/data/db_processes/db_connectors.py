
import cx_Oracle


class OpenConnector(object):

    def __init__(self):
        ip = '10.240.142.101'
        port = '2050'
        sid = 'PRODVG'
        user = 'pase01'
        password = 'pase02'
        dsn_str = cx_Oracle.makedsn(ip, port, sid)
        self.conn = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=dsn_str,
            encoding='iso-8859-1'
        )
