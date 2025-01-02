import datetime
from random import randint
import flet as ft
import pandas as pd
from data_base import PostgresConnection, ParquetStorage
import keyboard

# Подключаемся к базе данны
db = PostgresConnection(
    database="brick_game",
    password="PENROG21"
)
db.connect()

# Подключаемся к файлу для озера данных.
pq = ParquetStorage(r'C:\Users\user\PycharmProjects\pythonProject1\degs\Brick_Came\Data lake\data.parquet')
pq_topic = ParquetStorage(r'C:\Users\user\PycharmProjects\pythonProject1\degs\Brick_Came\Data lake\data_topic.parquet')


# page - это вся страница приложения
def main(page: ft.Page):
    try:
        # Генерация количества кирпичей
        number_bricks = int(randint(12, 20))

        # Данные для сохранения
        # Количество игр
        quality_games = 0
        # Количество побед игрока
        quality_win_player = 0
        # Количество побед компьютера
        quality_win_computer = 0

        # Название приложения
        page.title = "Rainbow"
        # Ширина
        page.window.width = 800
        # Высота
        page.window.height = 800
        # Возможность менять размер окна

        # Глобальные пременые.
        login_user = None
        id_user = None

        def open_dialog(dialog_to_open: ft.AlertDialog):
            """Открывает диалоговое окно.
            Args:
                dialog_to_open: Диалоговое окно, которое нужно открыть.
            """
            dialog_to_open.open = True
            dialog_to_open.update()

        def close_dialog(dialog_to_close: ft.AlertDialog):
            """Закрывает диалоговое окно.
            Args:
                dialog_to_close: Диалоговое окно, которое нужно закрыть.
            """
            dialog_to_close.open = False
            dialog_to_close.update()

        def load(e):
            """
            Функция для сериализации и скачивания данных игры.
            """
            nonlocal id_user
            # Создаем DataFrame
            result = db.table_for_save(int(id_user))
            df = pd.DataFrame([result], columns=['Количество побед', 'Количество игр'])
            # Проверяем какой формат нужен пользователю
            if dropdown.value == 'json':
                df.to_json('Brick_data.json', index=False)
            elif dropdown.value == 'excel':
                df.to_excel('Brick_data.xlsx', index=False)
            elif dropdown.value == 'csv':
                df.to_csv('Brick_data.csv', index=False)

            # Сообщаем что данные скачены.
            open_dialog(load_message)

        # Создаем диалоговое окно для отображения ошибки ввода
        error_message = ft.AlertDialog(
            title=ft.Text("Ошибка хода", size=24, weight=ft.FontWeight.BOLD),  # Заголовок окна
            content=ft.Text("Вы не можете взять столько кирпичей", size=16),  # Основное сообщение
            actions=[
                ft.TextButton(text="OK", on_click=lambda e: close_dialog(error_message)),  # Кнопка для закрытия окна
            ],
            modal=True,  # Делает диалоговое окно модальным
            open=False,  # Начальное положение (не открыто)
            elevation=8,  # Эффект тени
        )

        # Создаем диалоговое окно для отображения сообщения о победе
        victory_message = ft.AlertDialog(
            title=ft.Text("🥇Вы победили🏆", size=24, weight=ft.FontWeight.BOLD),  # Заголовок окна
            content=ft.Text("Поздравляю вы взяли последний кирпич\n"
                            "Игра начнется заново", size=16),  # Основное сообщение
            actions=[
                ft.TextButton(text="Ура", on_click=lambda e: close_dialog(victory_message)),  # Кнопка для закрытия окна
            ],
            modal=True,  # Делает диалоговое окно модальным
            open=False,  # Начальное положение (не открыто)
            elevation=8,  # Эффект тени
            icon_color='#3CB371'  # Цвет иконки
        )

        # Создаем диалоговое окно для отображения сообщения о загрузке
        load_message = ft.AlertDialog(
            title=ft.Text("Скачено📲", size=24, weight=ft.FontWeight.BOLD),  # Заголовок окна
            content=ft.Text("Данные скачены", size=16),  # Основное сообщение
            actions=[
                ft.TextButton(text="Хорошо", on_click=lambda e: close_dialog(load_message)),  # Кнопка для закрытия окна
            ],
            modal=True,  # Делает диалоговое окно модальным
            open=False,  # Начальное положение (не открыто)
            elevation=8,  # Эффект тени
        )

        # Создаем диалоговое окно для отображения сообщения о поражении
        defeat_message = ft.AlertDialog(
            title=ft.Text("😥Поражение", size=24, weight=ft.FontWeight.BOLD),  # Заголовок окна
            content=ft.Text("Компьютер взял последний кирпич.\n"
                            "Компьютер занял предпоследнее место, а вы второе🥈😉", size=16),  # Основное сообщение
            actions=[
                ft.TextButton(text="Реванш", on_click=lambda e: close_dialog(defeat_message)),
                # Кнопка для закрытия окна
            ],
            modal=True,  # Делает диалоговое окно модальным
            open=False,  # Начальное положение (не открыто)
            elevation=8,  # Эффект тени
        )

        rule_message = ft.AlertDialog(
            title=ft.Text("Добро пожаловать", size=24, weight=ft.FontWeight.BOLD),  # Заголовок окна
            content=ft.Text("Это игра 'Кирпич'\nПравило:\n Вы и компьютер берёте кирпичи поочередно.\n"
                            'За ход можно взять 1, 2 или 3 кирпича.\n'
                            "Проиграл тот, кому нечего брать.", size=16),  # Основное сообщение)
            actions=[
                ft.TextButton(text="Играть!", on_click=lambda e: close_dialog(rule_message)),
                # Кнопка для закрытия окна
            ],
            modal=True,  # Делает диалоговое окно модальным
            open=False,  # Начальное положение (не открыто)
            elevation=8,  # Эффект тени
        )

        def change_theme(e):
            """
            Функция, которая меняет тему на противоположную.
            """
            if page.theme_mode == ft.ThemeMode.DARK:
                # Если текущая тема - темная, меняем ее на светлую
                page.theme_mode = ft.ThemeMode.LIGHT
                page.Icon = ft.Icons.DARK_MODE_ROUNDED
                e.control.Icon = ft.Icons.DARK_MODE_ROUNDED

                pq_topic.add_data_topic(False, id_user)
            else:
                # Если текущая тема - светлая, меняем ее на темную
                page.theme_mode = ft.ThemeMode.DARK
                page.Icon = ft.Icons.SUNNY
                e.control.Icon = ft.Icons.SUNNY

                pq_topic.add_data_topic(True, id_user)
            # Обновляем отображение страницы
            page.update()

        # Кнопка смены темы.
        button_sunny = ft.IconButton(icon=ft.Icons.SUNNY, selected_icon=ft.Icons.MOOD_BAD, on_click=change_theme)

        # Создаем текст для отображения количества оставшихся кирпичей
        output_number_brickse = ft.Text(value=f"Количество кирпичей: {number_bricks}", size=32,
                                        weight=ft.FontWeight.BOLD)
        # Создаем текст для отображения количества побед
        number_wins = ft.Text(value="", size=32, visible=False)

        def show_wins_number(e):
            """
            Функция, которая убирает текст о результатах игрока или добавляет
            """
            number_wins.visible = False if number_wins.visible is True else True
            # Обновляем страницу.
            page.update()

        show_number_wins = ft.IconButton(ft.Icons.REMOVE_RED_EYE, visible=False, on_click=show_wins_number)

        # Текст как сходил компьютер
        text_player_move = ft.Text(
            "",
            size=32,
            font_family="",
            weight=ft.FontWeight.W_100,
            visible=False  # Изначально спрятать
        )

        def after_one_game(playr_or_computer: bool):
            """
            Это функция, которая выполняет все действия после первой игры
            :param playr_or_computer:
            :return:
            """
            # Даем возможность скачать данные
            dropdown.visible = True
            download_button.visible = True

            nonlocal quality_games, quality_win_player
            quality_games += 1
            # Записываем итоги игры
            if playr_or_computer:
                nonlocal quality_win_computer
                quality_win_computer += 1
            else:
                quality_win_player += 1

            # Выводи информацию
            show_number_wins.visible = True
            number_wins.value = f"Количество игр {quality_games} Из них побед {quality_win_player}"

            page.update()

        def computer_running(e):
            """
            Функция для хода компьютера.
            """
            nonlocal text_player_move, output_number_brickse, number_bricks
            # Смотрим сколько осталось кирпичей
            if number_bricks in (1, 2, 3):
                computer_player = number_bricks
            else:
                computer_player = randint(1, 3)  # Ход компьютера

            nonlocal id_user
            # Вычитаем ход из общей суммы кирпичей.
            number_bricks -= computer_player
            # Записываем в общий дата лайк
            pq.add_data(int(id_user), 2, computer_player, number_bricks)

            if number_bricks <= 0:  # Проверка на поражение
                # Сообщаем о поражении
                open_dialog(defeat_message)
                number_bricks = int(randint(12, 20))
                # Записываем в бд
                db.record_game_result(int(id_user), False)
                # Открываем все скрытые кнопки
                after_one_game(playr_or_computer=True)

            text_player_move.visible = True
            text_player_move.value = f"Ход компьютера: {computer_player}"

            output_number_brickse.value = f"Количество кирпичей: {number_bricks}"
            page.update()

        def player_move(e):
            """
            Функция для хода игрока.
            """
            # Получаем ход пользователя
            move = int(e.control.data)
            nonlocal number_bricks
            if number_bricks < move:
                # Сообщение об ошибке хода
                open_dialog(error_message)
            else:
                # Вычитаем ход игрока из общей суммы кирпичей.
                taken_bricks = int(move)
                # Вычитаем
                number_bricks -= taken_bricks
                # Записываем в общий дата лайк
                nonlocal id_user
                pq.add_data(int(id_user), 1, taken_bricks, number_bricks)

                if number_bricks <= 0:  # Проверка на победу
                    db.record_game_result(int(id_user), True)
                    # Сообщае о победе
                    open_dialog(victory_message)
                    # Генирируем заново
                    number_bricks = int(randint(12, 20))
                    # Открываем все скрытые кнопки
                    after_one_game(playr_or_computer=False)

                    output_number_brickse.value = f"Количество кирпичей: {number_bricks}"
                    page.update()
                else:
                    # Ход компьютера
                    computer_running(e)

        download_button = ft.ElevatedButton(
            text="Сохранить",
            on_click=load,
            color='#000000',
            visible=False,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.WHITE,  # Цвет фона кнопки.
                shape=ft.RoundedRectangleBorder(radius=10),  # Задаем скругленные углы.
                overlay_color=ft.Colors.GREY,  # Цвет при наведении
            )
        )

        dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("excel"),
                ft.dropdown.Option("json"),
                ft.dropdown.Option("csv"),
            ],
            value='excel',
            visible=False
        )

        welcome_title = ft.Text(size=48, weight=ft.FontWeight.BOLD, selectable=True)

        def switching(where: bool):
            """
            Функция для переключением между слайдами.

            :param where: True для перехода на игровое окно, False для перехода на регистрацию.
            """
            # Удаление всех элементов и перевод в тёмную тему.
            page.clean()
            page.theme_mode = ft.ThemeMode.DARK
            if where:
                # Заполняем глобальные переменные.
                nonlocal login_user, id_user
                # Получение логина юзера
                login_user = db.get_user_name_by_email(user_gmail.value)
                # Получение id юзера
                id_user = db.get_user_id_by_name(login_user)
                # Убираем предыдущий navigation_bar
                page.navigation_bar = None

                welcome_title.value = f'Добро пожаловать {login_user}'

                show_page(0)
                page.add(
                    ft.Container(  # Container для хранения всего содержимого.
                        content=ft.Row([rail, current_page]),  # Расположение содержимого в строку.
                        expand=True  # Разрешение содержимому занимать всю доступную площадь.
                    )
                )
            else:
                # Очищаем значения полей ввода и скрываем элементы, связанные с игрой.
                page.clean()
                user_login.value = None
                user_gmail.value = None
                selected_date.value = None
                gender_radio.value = None
                user_password.value = None
                btn_password.disabled = True
                btn_auth.disabled = True
                btn_reg.disabled = True

                text_player_move.visible = False
                number_wins.visible = False
                show_number_wins.visible = False
                dropdown.visible = False
                download_button.visible = False

                nonlocal quality_games, quality_win_player
                quality_games = 0
                quality_win_player = 0

                # Добавляем панель регистрации и навигационную панель.
                page.add(panel_auth)
                page.navigation_bar = switch
                page.theme_mode = ft.ThemeMode.DARK
                page.update()

        # Упаковка для игры и регистрации
        current_page = ft.Container(
            content=ft.Column(),
            expand=True,
        )

        def show_page(index):
            """
            Функция для переключения из поля игры к статистики и наоборот.
            """
            current_page.content.controls.clear()
            if index == 0:
                current_page.content.controls.append(main_game)
                page.theme_mode = ft.ThemeMode.DARK
            elif index == 1:
                current_page.content.controls.append(ft.Column(
                    [
                        Statistics,
                    ]
                ))
            page.update()

        # Загружаем данные таблицы лидеров.
        leaderboard_data = db.fetch_leaderboard_data()
        # Флаг для переключения между видами таблицы лидеров.
        show_alternative_leaderboard = False

        # Функция для создания таблицы лидеров на основе данных.
        def create_leaderboard_table(leaderboard_data):
            try:
                # Создаем таблицу DataTable с помощью Flet.
                leaderboard_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Место")),
                        ft.DataColumn(ft.Text("Логин")),
                        ft.DataColumn(ft.Text("Побед")),
                        ft.DataColumn(ft.Text("Игр")),
                        ft.DataColumn(ft.Text("Процент побед %"), numeric=True),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(i + 1))),
                                ft.DataCell(ft.Text(str(row[0]))),
                                ft.DataCell(ft.Text(str(row[1]))),
                                ft.DataCell(ft.Text(str(row[2]))),
                                ft.DataCell(ft.Text(str(row[3]))),
                            ]
                        ) for i, row in enumerate(leaderboard_data)
                    ]
                )
                # Возвращаем созданную таблицу.
                return leaderboard_table
            except Exception as e:
                # Обработка других ошибок.
                page.add(ft.Text(f"Произошла ошибка: {e}"))
                return None

        # Функция для переключения между видами таблицы лидеров.
        def toggle_leaderboard(e):
            # Используем nonlocal, так как show_alternative_leaderboard объявлена вне этой функции.
            nonlocal show_alternative_leaderboard
            # Меняем значение флага на противоположное.
            show_alternative_leaderboard = not show_alternative_leaderboard
            # Обновляем содержимое контейнера таблицы.
            leaderboard_container.content = create_leaderboard_table(
                db.fetch_leaderboard_by_win_percentage()
                if show_alternative_leaderboard
                else db.fetch_leaderboard_data()
            )
            if show_alternative_leaderboard:
                text_for_user_table.content = ft.Text(value='Сортировка по проценту побед.', width=160)
            else:
                text_for_user_table.content = ft.Text(value='Сортировка по количеству побед.', width=160)
            # Обновляем контейнер на странице.
            leaderboard_container.update()
            text_for_user_table.update()

        # Создаем кнопку для переключения таблиц.
        save_button = ft.IconButton(
            icon=ft.Icons.UPDATE,
            on_click=toggle_leaderboard,
        )

        # Создаем контейнер для таблицы. Важно: он объявлен вне функции create_leaderboard_table.
        leaderboard_container = ft.Container(expand=True)
        text_for_user_table = ft.Container(expand=True)
        # Добавляем таблицу в контейнер.
        leaderboard_container.content = create_leaderboard_table(leaderboard_data)
        text_for_user_table.content = ft.Text(value='Сортировка по количеству побед', width=160)

        # Создание контейнера для статистики
        Statistics = ft.Container(
            content=ft.Column(
                [
                    # Первая строка: Заголовок "Статистика" и кнопка button_sunny
                    ft.Row([button_sunny], alignment=ft.MainAxisAlignment.END),
                    ft.Row([
                        ft.Stack(
                            [
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "Статистика",
                                            ft.TextStyle(
                                                size=48,
                                                weight=ft.FontWeight.BOLD,
                                                foreground=ft.Paint(
                                                    color=ft.Colors.BLUE_700,
                                                    stroke_width=6,
                                                    stroke_join=ft.StrokeJoin.ROUND,
                                                    style=ft.PaintingStyle.STROKE,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "Статистика",
                                            ft.TextStyle(
                                                size=48,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREY_300,
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    # Вторая строка: Текст text_for_user_table и кнопка save_button
                    ft.Row([text_for_user_table, save_button], alignment=ft.MainAxisAlignment.CENTER),
                    # Третья строка: Контейнер с таблицей лидеров
                    ft.Row([leaderboard_container], alignment=ft.MainAxisAlignment.CENTER),
                ]
            )
        )

        # Создание навигационного рельса
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            on_change=lambda e: show_page(e.control.selected_index),
            min_extended_width=400,
            group_alignment=-0.9,

            destinations=[
                # Назначение для страницы игры
                ft.NavigationRailDestination(
                    icon=ft.Icons.GAMES_OUTLINED,
                    selected_icon=ft.Icons.GAMEPAD_SHARP,
                    label="Игра",
                ),
                # Назначение для страницы статистики
                ft.NavigationRailDestination(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.Icons.ANALYTICS_ROUNDED,
                    label="Статистика",
                ),
            ],
            trailing=ft.Column([
                # Кнопка с вопросительным знаком, открывающая диалоговое окно с правилами
                ft.IconButton(icon=ft.Icons.QUESTION_MARK, width=58, height=58,
                              on_click=lambda e: open_dialog(rule_message)),
                # Кнопка с логотипом GitHub, открывающая ссылку на проект на GitHub
                ft.IconButton(
                    content=ft.Image(src="github-mark-white.png", width=32, height=32),
                    width=58,
                    height=58,
                    url='https://github.com/PENROG21/Brick_Game'
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            # Кнопка "Домой", возвращающая пользователя на страницу регистрации
            leading=ft.Row(
                [ft.IconButton(icon=ft.Icons.HOME, width=32, height=58, on_click=lambda _: switching(False))],
                alignment=ft.MainAxisAlignment.END),

            height=600
        )

        # Это главный экран игрового приложения.
        main_game = ft.Container(
            image_src='https://cdna.artstation.com/p/assets/images/images/000/548/348/large/'
                      'martin-teichmann-stones-02.jpg?1443931018',
            image_fit=ft.ImageFit.COVER,
            expand=True,
            content=ft.Column(  # Оборачиваем все элементы в Column
                [
                    ft.Row([welcome_title], alignment=ft.MainAxisAlignment.CENTER),
                    # Заголовок приложения
                    ft.Row([output_number_brickse], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text(value='Сколько кирпичей возьмёте?', size=24, weight=ft.FontWeight.BOLD,
                                    selectable=True)],
                           alignment=ft.MainAxisAlignment.CENTER),
                    # Кнопки хода
                    ft.Row(
                        [
                            ft.IconButton(
                                on_click=player_move,
                                data=1,
                                content=ft.Image(
                                    src="icons8-1st-50.png",
                                    width=56,
                                    height=56,
                                    fit=ft.ImageFit.COVER,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                )
                            ),
                            ft.IconButton(
                                on_click=player_move,
                                data=2,
                                content=ft.Image(
                                    src="icons8-circled-2-50.png",
                                    width=56,
                                    height=56,
                                    fit=ft.ImageFit.COVER,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                )
                            ),
                            ft.IconButton(
                                on_click=player_move,
                                data=3,
                                content=ft.Image(
                                    src="icons8-circled-3-50.png",
                                    width=56,
                                    height=56,
                                    fit=ft.ImageFit.COVER,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                )
                            ),
                            # Различные сообщея.
                            error_message,
                            victory_message,
                            defeat_message,
                            load_message,
                            rule_message
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Надпись как сходил компьютер
                    ft.Row([text_player_move], alignment=ft.MainAxisAlignment.CENTER),
                    # Кнопка показа результата.
                    ft.Row([number_wins, show_number_wins], alignment=ft.MainAxisAlignment.CENTER),
                    # Скачивание результата.
                    ft.Row([dropdown, download_button], alignment=ft.MainAxisAlignment.CENTER)
                ],
            ),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        def show_error_template(message: str):
            """
            Отображает SnackBar с сообщением об ошибке.
            Args:
                message: Текст сообщения об ошибке.
            """
            snack_bar = ft.SnackBar(ft.Text(message), open=True)  # Создаем SnackBar с сообщением
            page.overlay.append(snack_bar)  # Добавляем SnackBar в overlay страницы
            page.update()  # Обновляем страницу для отображения SnackBar

        def check_email() -> bool:
            """
            Функция, которая проверяет, адрес почты.
            Если не верен, то выводит сообщение пользователю.
            """
            from re import split
            if split(r'@', user_gmail.value)[-1] != 'gmail.com':
                return False
            else:
                return True

        def register(e):
            """
            Функция, которая записывает данные пользователя
            """
            print(gender_radio.value + ' 1')
            if len(user_password.value) < 6:
                show_error_template("Пароль должен состоять из 6 символов и более.")
            # Проверяем, что адрес правильно указан.
            elif any(char.isspace() for char in user_password.value):
                show_error_template("В пароле не должно быть пробелов.")
            elif len(user_login.value) > 10 or len(user_login.value) < 3:
                show_error_template("Пароль должен быть от 3 до 10 символов.")
            elif any(char.isspace() for char in user_login.value):
                show_error_template("В логине не должны быть пробелов.")
            elif any(char.isspace() for char in user_gmail.value):
                show_error_template("В почте не должны быть пробелов.")
            # Проверяем, что адрес правильно указан.
            elif not check_email():
                show_error_template("Не корректный адрес почты")
            elif db.user_exists_login(user_login.value):
                show_error_template("Это имя уже занято")
            elif db.user_exists_gmail(user_gmail.value):
                show_error_template("Эта почта уже занята")
            else:
                # Выполнение SQL-запроса
                db.Insert_Users(user_login.value, user_password.value, user_gmail=user_gmail.value,
                                is_man=gender_radio.value,
                                birthdate=(selected_date.value))
                switching(True)

        def auth_user(e):
            """
            Функция, которая проверяет авторизацию пользователя.
            """
            # Проверяем, что адрес правильно указан.
            if check_email():
                # Проверяем что аккаунт существует
                if not db.check_user(email=user_gmail.value, password=user_password.value):
                    show_error_template('Неправильно введен пароль или почта.')
                else:
                    # Если есть начинаем игру.
                    switching(True)
            else:
                show_error_template('Неправильно указан адрес почты')

        def validate(e):
            """
            Функция, которая делает кнопки действительными смотря по условию
            """
            is_valid = all([
                user_login.value is not None,
                user_password.value is not None,
                user_gmail.value is not None,
                gender_radio.value is not None,
                selected_date.value is not None and len(selected_date.value) > 0,
            ])
            print(gender_radio.value)

            is_value_auth = all([
                user_gmail.value,
                user_password.value
            ])

            btn_auth.disabled = not is_value_auth
            btn_reg.disabled = not is_valid
            btn_password.disabled = not user_password.value
            page.update()

        def validate_PASSWORD(e):
            """
            Функция делает видным пароль.
            """
            user_password.password = False if user_password.password is True else True
            page.update()

        btn_password = ft.IconButton(ft.Icons.REMOVE_RED_EYE, on_click=validate_PASSWORD, disabled=True)
        user_password = ft.TextField(label='Пароль', password=True, width=320, on_change=validate)

        user_login = ft.TextField(label='Логин', width=320, on_change=validate, max_length=10, min_lines=3)
        user_gmail = ft.TextField(label='gmail', width=320, on_change=validate)
        btn_reg = ft.OutlinedButton(text='Зарегистрироваться', width=240, on_click=register, disabled=True)
        btn_auth = ft.OutlinedButton(text='Авторизация', width=240, on_click=auth_user, disabled=True)

        gender_radio = ft.RadioGroup(content=ft.Column([
            ft.Radio(value=True, label="Мужской"),
            ft.Radio(value=False, label="Женский"),
        ]), on_change=validate)
        gender_radio.value = None  # Начальное значение - ничего не выбрано

        selected_date = ft.TextField(
            label="Ваша дата рождения",
            width=200,
            multiline=False,
            min_lines=6,
            read_only=True,
            value=None,
            on_change=validate
        )

        def handle_change(e):
            selected_date.value = e.control.value.strftime('%Y-%m-%d')
            page.update()

        # Страница регистрации
        panel_register = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([button_sunny], alignment=ft.MainAxisAlignment.END),
                        ft.Stack(
                            [
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "Регистрация",
                                            ft.TextStyle(
                                                size=48,
                                                weight=ft.FontWeight.BOLD,
                                                foreground=ft.Paint(
                                                    color=ft.Colors.BLUE_700,
                                                    stroke_width=6,
                                                    stroke_join=ft.StrokeJoin.ROUND,
                                                    style=ft.PaintingStyle.STROKE,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "Регистрация",
                                            ft.TextStyle(
                                                size=48,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREY_300,
                                            ),
                                        ),
                                    ],
                                ),
                            ]
                        ),
                        user_login,
                        ft.Row([user_password, btn_password]),
                        user_gmail,
                        ft.Text('Ваш пол'),
                        gender_radio,
                        ft.ElevatedButton(
                            "Выбрать дату рождения",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=lambda e: page.open(
                                ft.DatePicker(
                                    first_date=datetime.datetime(year=1900, month=1, day=1),
                                    last_date=datetime.datetime(year=2024, month=10, day=1),
                                    on_change=handle_change,
                                )
                            ),
                        ),
                        selected_date,
                        btn_reg,
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        # Страница авторизации
        panel_auth = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([button_sunny], alignment=ft.MainAxisAlignment.END),
                        ft.Stack(
                            [
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "Авторизация",
                                            ft.TextStyle(
                                                size=48,
                                                weight=ft.FontWeight.BOLD,
                                                foreground=ft.Paint(
                                                    color=ft.Colors.BLUE_700,
                                                    stroke_width=6,
                                                    stroke_join=ft.StrokeJoin.ROUND,
                                                    style=ft.PaintingStyle.STROKE,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "Авторизация",
                                            ft.TextStyle(
                                                size=48,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREY_300,
                                            ),
                                        ),
                                    ],
                                ),
                            ]
                        ),
                        user_gmail,
                        ft.Row([user_password, btn_password]),
                        btn_auth
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        def navigate(e):
            """
            Функция, которая переключает страницу регистрации на авторизацию и на оборот.
            :param e:
            :return:
            """
            index = page.navigation_bar.selected_index
            page.clean()

            if index == 0:
                page.add(panel_register)
            if index == 1:
                page.add(panel_auth)

        switch = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER, selected_icon=ft.Icons.VERIFIED_USER_OUTLINED,
                                            label='Регистрация'),
                ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER, selected_icon=ft.Icons.VERIFIED_USER_OUTLINED,
                                            label='Авторизация')
            ], on_change=navigate
        )

        page.navigation_bar = switch
        # Стартовая панель регистрацииы
        page.add(
            panel_register
        )
        # Обработка горячей клавиши
        keyboard.add_hotkey('ctrl+s', lambda: switching(False))

    except Exception as e:
        page.add(ft.Text(f"An error occurred: {e}"))


if __name__ == "__main__":
    # Запуск приложения
    ft.app(target=main)
