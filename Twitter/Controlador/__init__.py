import pymysql

DB_HOST = ''
DB_USER = 'apdif'
DB_PASSWORD = ''
DB_NAME = 'apdif'


def crea_tabla():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    sql = "CREATE TABLE IF NOT EXISTS `twitter_monitoreo` (id INT NOT NULL AUTO_INCREMENT," \
          "PRIMARY KEY (id), usuario INT, texto VARCHAR(500), hashtag VARCHAR(200), referer VARCHAR(155), infringing VARCHAR(280), fecha VARCHAR(100));"
    with con:
        cur = con.cursor()
        cur.execute(sql)

def crea_tablaUsuario():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    sql = "CREATE TABLE IF NOT EXISTS `twitter_usuarios` (id INT NOT NULL AUTO_INCREMENT," \
          "PRIMARY KEY (id), usuario VARCHAR(20));"
    with con:
        cur = con.cursor()
        cur.execute(sql)

def artist_itunes():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT artist FROM `itunes_artist` ORDER BY artist ASC''')
        cur.execute(sql)

        results = cur.fetchall()

        return results
    
def existe_inf(inf):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT infringing FROM `twitter_monitoreo`''')
        cur.execute(sql)

        resultado = cur.fetchall()
        for res in resultado:
            if res[0] == inf:
                return True
        return False
    
def existe_usuario(usuario):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT id FROM `twitter_usuarios` WHERE usuario ="{}"'''.format(usuario))
        cur.execute(sql)
        resultado = cur.fetchone()
        if resultado:
            return resultado[0]
        else:
            return False
    
def inserta_item_nueva(usuario, texto, Hash, url, href, fecha):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''INSERT INTO `twitter_monitoreo` VALUES (DEFAULT,'%s', '%s', '%s', '%s', '%s', '%s') ''' % (usuario, texto, Hash, url, href, fecha) )
        cur.execute(sql)
        return sql
    
def inserta_Usuario(usuario):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''INSERT INTO `twitter_usuarios` VALUES (DEFAULT,'%s')''' % (usuario))
        cur.execute(sql)
        return sql
