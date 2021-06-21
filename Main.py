# Простое приложение "крестики-нолики"
# kivy версии 2.0.0

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.modalview import ModalView

class GridEntry(Button):
    coords = ListProperty([0, 0])
    
class MainGrid(GridLayout):
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0]) 
    current_player = NumericProperty(1) # Если 1, то начинает игрок "O", если -1, то "X"
    def __init__(self, *args, **kwargs):
        super(MainGrid, self).__init__(*args, **kwargs)

        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(
                    coords=(row, column))
                grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry)
        

    def button_pressed(self, button):
        # print ('{} button clicked!'.format(button.coords))
        # Создание игроков и присваивание им цвета
        player = {1: 'O', -1: 'X'}
        colours = {
                    1: (1, 1, 0, 1), # Цвет "O" игрока
                    -1: (0, 1, 1, 1) # Цвет "X" игрока
                    } # Цвет в r, g, b, a

        row, column = button.coords # Нажатая кнопка автоматически передается в качестве аргумента

        # Преобразование координат 2D сетки в 1D индекс состояния
        status_index = 3*row + column
        already_played = self.status[status_index]

        # If nobody has played here yet, make a new move
        if not already_played:
            self.status[status_index] = self.current_player
            button.text = {1: 'O', -1: 'X'}[self.current_player]
            button.background_color = colours[self.current_player]
            self.current_player *= -1 # Смена игрока
    
    def on_status(self, instance, new_value):
        status = new_value

        # Суммируем строку и столбец
        sums = [sum(status[0:3]), # Ряды
            sum(status[3:6]), sum(status[6:9]), sum(status[0::3]), # Столбцы
            sum(status[1::3]), sum(status[2::3]), sum(status[::4]), # Диагональ 
            sum(status[2:-2:2])]

        winner = None
        # Объявляем победителя
        if -3 in sums:
            winner = '"Х" Победил'
        elif 3 in sums:
            winner = '"O" Победил'
        elif 0 not in self.status:
            winner = 'Ничья!'
        
        # Вывод окна с победителем 
        if winner:
            popup = ModalView(size_hint=(1, 0.25), background_color = (.12, .53, .90, 1)) # Размер и цвет окна 
            victory_label = Label(text=winner, font_size=58) # Вывод текста с победителем и установка размера шрифта
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()

    # Сброс и повторное начало игры
    def reset(self, *args):
        self.status = [0 for _ in range(9)]

        for child in self.children:
            child.text = ''
            child.background_color = (.12, .53, .90, 1)
        self.current_player = 1 # Если 1, то начинает игрок "O", если -1, то "X"

class Main(App):
    def build(self):
        return MainGrid()

# Не закрывает приложение
if __name__ == "__main__":
    Main().run()