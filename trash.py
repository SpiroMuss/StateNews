style = """
            /* Основной фон */
            QWidget {
                background-color: #f5f1e6;  /* Светлый бежевый */
                color: #3e2723;  /* Темно-коричневый для текста */
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            /* Заголовки */
            QLabel {
                color: #5d4037;  /* Коричневый */
                font-weight: bold;
                padding: 5px 0px;
            }

            /* Поля ввода (QLineEdit) */
            QLineEdit {
                background-color: #faf8f3;  /* Очень светлый бежевый */
                border: 2px solid #6b8e71;  /* Зеленый акцент */
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                color: #4e342e;  /* Темно-коричневый */
                selection-background-color: #a5d6a7;  /* Светло-зеленый для выделения */
            }

            QLineEdit:focus {
                border: 2px solid #4a7c59;  /* Более насыщенный зеленый */
                background-color: #ffffff;
            }

            QLineEdit::placeholder {
                color: #a1887f;  /* Светло-коричневый для placeholder */
                font-style: italic;
            }

            /* Многострочные текстовые поля (QTextEdit) */
            QTextEdit {
                background-color: #faf8f3;
                border: 2px solid #6b8e71;  /* Зеленый акцент */
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                color: #4e342e;
                selection-background-color: #a5d6a7;
            }

            QTextEdit:focus {
                border: 2px solid #4a7c59;
                background-color: #ffffff;
            }

            QTextEdit::placeholder {
                color: #a1887f;
                font-style: italic;
            }

            /* Кнопки */
            QPushButton {
                background-color: #8d6e63;  /* Коричневый */
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }

            QPushButton:hover {
                background-color: #6d4c41;  /* Темно-коричневый */
            }

            QPushButton:pressed {
                background-color: #4a3429;  /* Очень темный коричневый */
                padding-top: 13px;
                padding-bottom: 11px;
            }

            QPushButton:disabled {
                background-color: #bcaaa4;  /* Светло-коричневый */
                color: #757575;
            }
            """