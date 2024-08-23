import pymysql
import asyncio
from config import DBconf


async def get_connection():
    return pymysql.connect(
        host=DBconf.host,
        port=DBconf.port,
        user=DBconf.user,
        password=DBconf.password,
        database=DBconf.database,
    )


async def INSERT(TABLENAME, INTO, VALUES):
    connect = await get_connection()
    print(f"INSERT INTO `{TABLENAME}` "
          f"({INTO}) "
          f"VALUES ({VALUES})")
    with connect.cursor() as con:
        con.execute(f"INSERT INTO `{TABLENAME}` "
                    f"({INTO}) "
                    f"VALUES ({VALUES})")
        connect.commit()
        connect.close()


async def SELECT(INTO, TABLENAME, WHERE):
    connect = await get_connection()
    print(f"SELECT {INTO} "
          f"FROM `{TABLENAME}` "
          f"WHERE {WHERE}")
    with connect.cursor() as con:
        con.execute(f"SELECT {INTO} "
                    f"FROM `{TABLENAME}` "
                    f"WHERE {WHERE}")
        connect.close()
        return con.fetchall()


async def DELETE(TABLENAME, ID):
    connect = await get_connection()
    print(f"DELETE FROM `{TABLENAME}` "
          f"WHERE `{TABLENAME}`.`id` = {ID}")
    with connect.cursor() as con:
        con.execute(f"DELETE FROM `{TABLENAME}` "
                    f"WHERE `{TABLENAME}`.`id` = {ID}")
        connect.commit()
        connect.close()


async def DELETEWHERE(TABLENAME, WHERE):
    connect = await get_connection()
    print(f"DELETE FROM `{TABLENAME}` "
          f"WHERE {WHERE}")
    with connect.cursor() as con:
        con.execute(f"DELETE FROM `{TABLENAME}` "
                    f"WHERE {WHERE}")
        connect.commit()
        connect.close()


async def UPDATE(TABLENAME, SET, ID):
    connect = await get_connection()
    with connect.cursor() as con:
        con.execute(f"UPDATE `{TABLENAME}` SET {SET} WHERE `{TABLENAME}`.`id` = {ID}")
        connect.commit()
        connect.close()


async def UPDATEWHERE(TABLENAME, SET, WHERE):
    connect = await get_connection()
    print(f"UPDATE `{TABLENAME}` SET {SET} WHERE {WHERE}")
    with connect.cursor() as con:
        con.execute(f"UPDATE `{TABLENAME}` SET {SET} WHERE {WHERE}")
        connect.commit()
        connect.close()


async def IFUSERINDB(TABLENAME, USERNAME):
    connect = await get_connection()
    with connect.cursor() as con:
        RES = con.execute(f"SELECT `userName` "
                          f"FROM `{TABLENAME}` "
                          f"WHERE `userName` = '{USERNAME}'")
        connect.close()
        return bool(RES)


async def IF(TABLENAME, INTO, WHERE):
    connect = await get_connection()
    print(f"SELECT {INTO} "
          f"FROM `{TABLENAME}` "
          f"WHERE {WHERE}")
    with connect.cursor() as con:
        RESO = con.execute(f"SELECT {INTO} "
                           f"FROM `{TABLENAME}` "
                           f"WHERE {WHERE}")
        connect.close()
        return bool(RESO)


async def CREATE_TABLE(TABLENAME, ARGS):
    connect = await get_connection()
    with connect.cursor() as con:
        con.execute(f"CREATE TABLE `{TABLENAME}` ({ARGS})")
        connect.commit()
        connect.close()


async def COUNT(TABLENAME, INTO, WHERE):
    connect = await get_connection()
    with connect.cursor() as con:
        RESO = con.execute(f"SELECT {INTO} "
                           f"FROM `{TABLENAME}` "
                           f"WHERE {WHERE}")
        connect.close()
        return RESO


async def ENTER(ENTER):
    connect = await get_connection()
    with connect.cursor() as con:
        con.execute(f"{ENTER}")
        connect.close()
        return con.fetchall()
