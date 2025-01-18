from db_connection import create_connection
from db_connection import close_connection


class Bot_func():
    def __init__(self, conn):
        self._conn = conn

    def create_user(self, last_name, first_name, id_tg):
        cursor = self._conn.cursor()
        try:
            cursor.execute("insert into db_tg_bot.user (last_name, first_name, id_telegram) values (%s, %s, %s)",
                           (last_name, first_name, id_tg))
            self._conn.commit()
        except Exception as e:
            print("Пользователь не создан!", e)
        finally:
            cursor.close()

    def check_user(self, id_tg):
        cursor = self._conn.cursor()
        try:
            cursor.execute("select coalesce((select id_telegram from db_tg_bot.user where id_telegram = %s), 0);", (id_tg,))
            result = cursor.fetchone()

            if result[0] != 0:
                return True
            else:
                return False
        except Exception as e:
            print("Ошибка!", e)
        finally:
            cursor.close()


    def create_event(self, date, time_start, time_end, moment, user_ids):
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                "insert into db_tg_bot.event (date_moment, time_start, time_end, moment, user_ids) values (%s, %s, %s, %s, %s)",
                (date, time_start, time_end, moment, (user_ids,)))
            self._conn.commit()
            return True
        except Exception as e:
            print("Событие не создано!", e)
        finally:
            cursor.close()

    def get_users_id(self, members):
        cursor = self._conn.cursor()
        try:
            query = """select id_telegram from db_tg_bot.user where (first_name, last_name) in %s;"""
            name_tuples = [tuple(name.split()) for name in members]
            cursor.execute(query, (tuple(name_tuples),))
            user_ids = [row[0] for row in cursor.fetchall()]
            return user_ids
        except Exception as e:
            print("Ошибка!", e)
        finally:
            cursor.close()

    def get_user_name(self, tg_ids):
        cursor = self._conn.cursor()
        try:
            if isinstance(tg_ids, list):
                query = "SELECT first_name, last_name FROM db_tg_bot.user WHERE id_telegram = ANY(%s);"
                cursor.execute(query, (tg_ids,))
                result = cursor.fetchall()
            else:
                query = "SELECT first_name, last_name FROM db_tg_bot.user WHERE id_telegram = %s;"
                cursor.execute(query, (tg_ids,))
                result = cursor.fetchone()
            return result
        except Exception as e:
            print("Ошибка!", e)
        finally:
            cursor.close()


