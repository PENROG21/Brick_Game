import psycopg2
import pandas as pd
from datetime import datetime


class PostgresConnection:
    """Класс для работы с PostgreSQL."""

    def __init__(self, database, password, host="localhost", user="postgres", port=5432):
        """Инициализация подключения к PostgreSQL."""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """Создание подключения к PostgreSQL."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Соединение с PostgreSQL установлено успешно.")
        except psycopg2.Error as e:
            print(f"Ошибка подключения: {e}")

    def close(self):
        """Закрытие подключения к PostgreSQL."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Соединение с PostgreSQL закрыто.")


    def user_exists_login(self, login: str) -> bool:
        """
        Проверяет, что базе данных есть эти данные.
        :return:
        """
        self.cursor.execute("SELECT * FROM users WHERE name = '%s'" % login)

        result = self.cursor.fetchall()
        return len(result) > 0  # True если строка найдена, False иначе

    def user_exists_gmail(self, gmail: str) -> bool:
        """
        Проверяет, что базе данных есть эти данные.
        :return:
        """
        self.cursor.execute("SELECT * FROM users WHERE gmail = '%s'" % gmail)

        result = self.cursor.fetchall()
        return len(result) > 0  # True если строка найдена, False иначе

    def Insert_Users(self, user_login: str, user_password: str, user_gmail: str, is_man,
                     birthdate: str):
        """
        Метод для добавления данных пользователя в базу данных.
        :param user_login: Логин пользователя
        :param user_password: Пароль пользователя
        :param user_gmail: Почту юзера
        :param is_man: Если man то True иначе False
        :param birthdate: Дата рождения
        """
        print(f'{is_man} + 2we')
        try:
            self.cursor.execute("""INSERT INTO users(name, gmail, is_man, birthdate, password) VALUES 
            (%s, %s, %s, %s, %s)""",
                (user_login, user_gmail, is_man, birthdate, user_password))
            self.cursor.execute(f"INSERT INTO resulus(id_user, number_wins, number_games) VALUES((SELECT id FROM users "
                                f"WHERE name = '{user_login}'), 0, 0)")
            self.commit()

        except psycopg2.Error as e:
            print(f"Ошибка выполнения запроса: {e}")

    def get_user_name_by_email(self, gmail: str) -> str:
        """
        Возвращает имя пользователя по его адресу электронной почты.
        Args:
            gmail (str): Адрес электронной почты пользователя.
        Returns:
            str: Имя пользователя или пустая строка, если пользователь не найден.
        """
        print(gmail)
        self.cursor.execute(f"SELECT name FROM users WHERE gmail = '{gmail}'")
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def record_game_result(self, id_user: int, victory: bool):
        """
        Метод записывает в базу данных результат игры
        :param id_user: id юзер
        :param victory: True - выиграл False - Проиграл
        """
        self.cursor.execute(f"SELECT record_game_result({id_user}, {victory})")
        self.commit()

    def table_for_save(self, id_user: int):
        """
        Метод, который выдает таблицы для сохранения.
        :param id_user: id юзера чью статистику надо сохранить.
        :return: Статистику юзера
        """
        self.cursor.execute(f"SELECT number_wins, number_games FROM resulus WHERE id_user = {id_user}")
        result = self.cursor.fetchone()
        return result

    def get_user_id_by_name(self, login: str) -> str:
        """
        Возвращает ID пользователя по его имени.
        Args:
            login (str): Имя пользователя.
        Returns:
            str: ID пользователя или пустая строка, если пользователь не найден.
        """
        try:
            self.cursor.execute(f"SELECT id FROM users WHERE name = '{login}'")
            result = self.cursor.fetchone()
            return str(result[0]) if result else ""
        except psycopg2.Error as e:
            print(f"Ошибка получения результатов: {e}")
            return ''

    def check_user(self, email: str, password: str) -> bool:
        """
        Проверяет, что аккаунт есть в базе данных
        :param email: Почту пользователя
        :param password: Пароль
        :return: True если аккаунт есть, False иначе
        """
        self.cursor.execute(f"SELECT * FROM users WHERE gmail = '{email}' AND password = '{password}'")
        result = self.cursor.fetchall()
        return len(result) > 0  # True если строка найдена, False иначе

    def fetch_leaderboard_data(self):
        try:
            self.cursor.execute("""
                SELECT 
                    users.name, 
                    number_wins, 
                    number_games, 
                    ROUND((CASE 
                        WHEN number_games = 0 THEN 0
                        ELSE (number_wins::numeric * 100) / number_games
                    END), 2) AS win_percentage
                FROM resulus
                JOIN users ON resulus.id_user = users.id
                ORDER BY number_wins DESC;
            """)
            leaderboard_data = self.cursor.fetchall()
            return leaderboard_data
        except psycopg2.Error as e:
            print(f"Database error during leaderboard fetch: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def fetch_leaderboard_by_win_percentage(self):
        try:
            self.cursor.execute("""
                SELECT 
                    users.name, 
                    number_wins, 
                    number_games, 
                    ROUND((CASE 
                        WHEN number_games = 0 THEN 0
                        ELSE (number_wins::numeric * 100) / number_games
                    END), 2) AS win_percentage
                FROM resulus
                JOIN users ON resulus.id_user = users.id
                ORDER BY win_percentage DESC;
            """)
            leaderboard_data = self.cursor.fetchall()
            return leaderboard_data
        except psycopg2.Error as e:
            print(f"Database error during leaderboard fetch: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def commit(self):
        """Сохранение изменений в базе данных."""
        try:
            self.connection.commit()
            print("Изменения сохранены.")
        except psycopg2.Error as e:
            print(f"Ошибка сохранения изменений: {e}")


class ParquetStorage:
    """
    Класс для работы с файлом parquet
    """
    def __init__(self, file_path):
        """
        Иницилизируем путь к фаилу.
        :param file_path:
        """
        self.file_path = file_path
        # Создаем файл, если он не существует

    def add_data_from_dataframe(self, df):
        """Добавить данные из DataFrame в файл Parquet."""
        # Читаем существующий файл Parquet
        existing_df = pd.read_parquet(self.file_path)
        # Объединяем с новыми данными и сохраняем обратно в файл
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_parquet(self.file_path, index=False)

    def add_data(self, user_id: int,  player_id: int, bricks_captured: int, bricks_remaining: int):
        """Добавить данные как отдельные значения в файл Parquet."""
        # Создаем DataFrame из предоставленных данных
        new_data = pd.DataFrame({
            "user_id": [user_id],
            "timestamp": [datetime.now()],
            "player_id": [player_id],
            "bricks_captured": [bricks_captured],
            "bricks_remaining": [bricks_remaining]
        })
        # Вызываем метод для добавления из DataFrame
        self.add_data_from_dataframe(new_data)

    def add_data_topic(self, topic: bool, id_user):
        new_data = pd.DataFrame({
            'to_black': [topic],
            'time': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'id_user': [id_user]
        })

        self.add_data_from_dataframe(new_data)

    def read_data(self):
        """Читать данные из файла Parquet."""
        df = pd.read_parquet(self.file_path)
        return df.to_string(index=False, justify='left')  # Format the output


class TextFileDatabase:
    """
    Класс для взаимодействия с файлом
    """
    def __init__(self, file: str):
        """
        Инитилизация
        :param file: имя файла.
        """
        self.file = file

    def add_entry(self, text: str) -> bool:
        """
        Метод для записи в фаил.
        :param text: Текст, который надо добавить
        :return:
        """
        try:
            with open(self.file, "w") as file:
                # Запишите строку в файл
                file.write(text)
            return True
        except FileNotFoundError:
            print(f"Файл {self.file} не найден!")
            return False
        except Exception as e:
            print(f"Ошибка при записи в файл {self.file}: {e}")
            return False


# Пример использования:
if __name__ == "__main__":
    # Замените данные для подключения на свои
    pq = ParquetStorage(r'C:\Users\user\PycharmProjects\pythonProject1\degs\Brick_Came\Data lake\data_topic.parquet')

    print(pq.read_data())
