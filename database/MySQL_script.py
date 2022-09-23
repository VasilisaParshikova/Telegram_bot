from config_data import config
import mysql.connector
from datetime import date

class DB_Worker:
    def __init__(self):
        self.username = config.DB_USER
        self.password = config.DB_PASSWORD

    def write_to_db(self, user_id: int, data_dict):
        request_param = f'Вы искали отели в городе {data_dict["city"]} ' \
                        f'на период с {data_dict["date_in"]} по {data_dict["date_out"]}.'
        with mysql.connector.connect(database="bot_db",
                                     user=config.DB_USER,
                                     password=config.DB_PASSWORD,
                                     host='localhost',
                                     port='3306') as db_connection:
            with db_connection.cursor() as work_cursor:
                work_cursor.execute("INSERT INTO request_info (user_id, command, request_params, request_result, data) "
                                    "VALUES (%s, %s, %s, %s, %s)", (
                                                                    user_id,
                                                                    data_dict['command'],
                                                                    request_param,
                                                                    data_dict['result_text'],
                                                                    date.today()))
                db_connection.commit()

    def read_from_db(self, user_id):
        with mysql.connector.connect(database="bot_db",
                                     user=config.DB_USER,
                                     password=config.DB_PASSWORD,
                                     host='localhost',
                                     port='3306') as db_connection:
            with db_connection.cursor() as work_cursor:
                work_cursor.execute("SELECT * FROM request_info WHERE user_id = %s ORDER BY id DESC LIMIT 5", (user_id,))
                message_texts = []
                print(work_cursor)
                for line in work_cursor:
                    text = '{request_param} \nДата: {req_date}, команда: {command} . \n\n' \
                           'Результаты: \n{results}'.format(
                        request_param = line[3],
                        req_date = line[5],
                        command = line[2],
                        results = line[4]
                        )
                    message_texts.append(text)
                return message_texts
