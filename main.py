from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class Checker:
    def __init__(self, color):
        self.color = color  # 'white' или 'black'
        self.king = False

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Расстановка шашек на начальных позициях только на черных клетках
        for row in range(3):
            for col in range(row % 2, 8, 2):
                self.board[row][col] = Checker('black')
        for row in range(5, 8):
            for col in range(row % 2, 8, 2):
                self.board[row][col] = Checker('white')

class CheckersApp(App):
    def __init__(self, **kwargs):
        super(CheckersApp, self).__init__(**kwargs)
        self.selected_checker = None  # Хранит выбранную шашку
        self.selected_position = None  # Хранит позицию выбранной шашки

    def build(self):
        self.board = Board()  # Создаем экземпляр доски
        self.layout = GridLayout(cols=8)
        self.buttons = [[Button() for _ in range(8)] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                button = self.buttons[row][col]
                button.bind(on_press=self.on_button_press)
                self.layout.add_widget(button)
        
        self.update_board()
        return self.layout

    def update_board(self):
        # Обновление кнопок на доске в зависимости от состояния игры
        for row in range(8):
            for col in range(8):
                button = self.buttons[row][col]  # Получаем ссылку на текущую кнопку
                checker = self.board.board[row][col]
                
                if checker is not None:
                    # Устанавливаем изображение шашки на черной клетке
                    if (row + col) % 2 == 1:  # Только для черных клеток
                        if checker.color == 'black':
                            button.background_normal = 'black_checker.png'
                        else:
                            button.background_normal = 'white_checker.png'
                    else:
                        button.background_normal = ''  # Убираем изображение с белых клеток
                    
                else:
                    # Если клетка пустая
                    if (row + col) % 2 == 0:
                        button.background_color = (1, 1, 1, 1)  # Белый
                    else:
                        button.background_color = (0.5, 0.5, 0.5, 1)  # Серый

    def on_button_press(self, instance):
        button_index = [(i, j) for i in range(8) for j in range(8) if self.buttons[i][j] == instance]
        if button_index:
            row, col = button_index[0]

            if self.selected_checker is None:
                # Если ничего не выбрано, выбираем шашку
                checker = self.board.board[row][col]
                if checker is not None:
                    self.selected_checker = checker
                    self.selected_position = (row, col)
                    print(f"Selected checker at ({row}, {col})")
            else:
                # Если шашка уже выбрана, проверяем возможность перемещения
                target_checker = self.board.board[row][col]
                if target_checker is None and (row + col) % 2 == 1:  
                    # Проверяем что целевая клетка черная и пустая
                    if abs(row - self.selected_position[0]) == abs(col - self.selected_position[1]) == 1:  
                        print(f"Moving checker from {self.selected_position} to ({row}, {col})")
                        # Логика перемещения шашки
                        self.board.board[row][col] = self.selected_checker
                        self.board.board[self.selected_position[0]][self.selected_position[1]] = None
                        self.selected_checker = None
                        self.selected_position = None
                        self.update_board()
                    else:
                        print("Invalid move: can only move diagonally to an empty dark square.")
                else:
                    print("Invalid move: target square must be black or occupied by opponent's checker.")

if __name__ == "__main__":
    CheckersApp().run()