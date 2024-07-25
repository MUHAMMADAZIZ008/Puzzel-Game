from random import shuffle
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import(
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel, 
    QRadioButton
)



class StepSelection(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Step Selection")
        self.setWindowIcon(QIcon("selection.png"))
        self.setGeometry(700, 200, 500, 600)
        self.v_box = QVBoxLayout()
        self.select_lable = QLabel("Aelect a stage:")
        self.grid = QGridLayout()
        self.start_game_btn = QPushButton("Start the game")
        self.start_game_btn.clicked.connect(self.start_game)

        self.v_box.addWidget(self.select_lable, 0 , Qt.AlignCenter)
        self.v_box.addLayout(self.grid)
        self.v_box.addWidget(self.start_game_btn, 0 , Qt.AlignCenter)
        self.setLayout(self.v_box)  

        self.matrix = list()
        self.numbers = self.fill_numbers()
        index = 0
        for i in range(5):
            row = list()
            for j in range(4):
                rtb = QRadioButton(f"{self.numbers[index]}")
                rtb.toggled.connect(self.return_rBtn)
                rtb.setFixedSize(100, 50)
                rtb.setStyleSheet("""
                    padding: 15px; 
                    background-color: #176B87;
                    color: #fff;
                    font-size: 20px;
                    border-radius: 15px;
                """)
                # rtb.setStyleSheet
                self.grid.addWidget(rtb, i,j)
                row.append(rtb)
                index += 1
            self.matrix.append(row)
        self.show()

        #style
        self.setStyleSheet("""
            background-color: #04364A;
        """)
        self.select_lable.setStyleSheet("""
            color: #64CCC5;
            font-size: 50px;
            font-family: sans-serif;
            font-weight: 500;
        """)
        self.start_game_btn.setFixedSize(300, 50)
        self.start_game_btn.setStyleSheet("""
            background-color: #176B87;
            border-radius: 15px;
            color: #fff;
            font-size: 20px;
            font-family: sans-serif;
        """)
        
        #



    def fill_numbers(self):
        numbers = list(range(1, 21))
        numbers = list(map(str, numbers))
        return numbers 

    def return_rBtn(self):
        rbtn = self.sender()
        if rbtn.isChecked():
            self.selection_rd = int(rbtn.text()) + 1

    def start_game(self):
        select = self.selection_rd
        self.game_puzzle = Window(select)
        self.close()



class Window(QWidget):
    def __init__(self, num = 4) -> None:
        self.num = num
        super().__init__()
        self.setGeometry(700, 200, 300, 400)
        self.setWindowTitle("Puzzle Game")
        self.setWindowIcon(QIcon("puzzle-icon.png"))
        self.setStyleSheet("""
            background-color: #EEEEEE;
        """)


        #creat
        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()
        self.box_btn = QHBoxLayout()
        self.time_lable = QLabel("Time: ")
        self.moves_lable = QLabel("Moves: ")
        self.moves_count = 1
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.resetWindow)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_window)

        self.box_btn.addWidget(self.reset_btn)
        self.box_btn.addSpacing(10)
        self.box_btn.addWidget(self.pause_btn)
        #time
        self.sec = 0
        self.time = QTimer()
        self.time.timeout.connect(self.handle_timeout)
        self.elapsed_time = 0
        self.start_time()

        #creat game
        self.grid = QGridLayout()
        self.numbers = self.fill_number()
        self.matrix = list()
        
        self.real_matrix = [[str(1 + self.num * i + j) for j in range(self.num)] for i in range(self.num)]
        self.real_matrix[-1][-1] = " "

        self.is_paused = True
        self.game_gui()

        #style

        self.time_lable.setFixedHeight(70)
        self.time_lable.setStyleSheet("""
            padding: 5px;
            background-color: #0E185F;
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 20px
        """)

        self.moves_lable.setFixedHeight(70)
        self.moves_lable.setStyleSheet("""
            padding: 5px;
            background-color: #0E185F;
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 20px
        """)

        self.reset_btn.setFixedHeight(50)
        self.reset_btn.setStyleSheet("""
            padding: 10px;
            background-color: #0E185F;
            color: #fff;
            font-size: 25px;
            border-radius: 15px;
            font-weight: 500;
        """)

        self.pause_btn.setFixedHeight(50)
        self.pause_btn.setStyleSheet("""
            padding: 10px;
            background-color: #0E185F;
            color: #fff;
            font-size: 25px;
            border-radius: 15px;
            font-weight: 500;
        """)
        #


        self.h_box.addWidget(self.time_lable)
        self.h_box.addSpacing(10)
        self.h_box.addWidget(self.moves_lable)

        self.v_box.addLayout(self.h_box)
        self.v_box.addSpacing(50)
        self.v_box.addLayout(self.grid)
        self.v_box.addSpacing(30)
        self.v_box.addLayout(self.box_btn)
        self.setLayout(self.v_box)
        self.show()

    def game_gui(self):
        index = 0
        for i in range(self.num):
            row = list()
            for j in range(self.num):
                btn = QPushButton(self.numbers[index])
                btn.clicked.connect(self.on_lick)

                btn.setFixedSize(80, 80)
                btn.setStyleSheet("""
                    background-color: #2FA4FF;
                    border: none;
                    border-radius: 15px;
                    color: white;
                    font-size: 25px;
                    font-family: Arial, Helvetica, sans-serif;
                    font-weight: 500;
                """)
                
                row.append(btn)
                self.grid.addWidget(btn, i, j)
                index += 1
                if btn.text() == " ":
                    btn.hide()
            self.matrix.append(row)
        self.change_btn_color()

    def change_btn_color(self):
        for i in range(self.num):
            for j in range(self.num):
                btn = self.matrix[i][j]
                if btn.text() == self.real_matrix[i][j]:
                    btn.setStyleSheet("""
                        background-color: #3EC70B; 
                        border: none;
                        border-radius: 15px;
                        color: white;
                        font-size: 25px;
                        font-family: Arial, Helvetica, sans-serif;
                        font-weight: 500;
                    """)
                elif btn.text() == " ":
                    btn.setStyleSheet("""
                        background-color: #2FA4FF; 
                        border: none;
                        border-radius: 15px;
                        color: #fff;
                        font-size: 25px;
                        font-family: Arial, Helvetica, sans-serif;
                        font-weight: 500;
                    """)
                else:
                    btn.setStyleSheet("""
                        background-color: #2FA4FF; 
                        border: none;
                        border-radius: 15px;
                        color: white;
                        font-size: 25px;
                        font-family: Arial, Helvetica, sans-serif;
                        font-weight: 500;
                    """)                    


    def fill_number(self):

        numbers = list(range(1, self.num * self.num))
        numbers = list(map(str, numbers))
        numbers += [" "]
        shuffle(numbers)
        return numbers
    
    def start_time(self):
        self.time.start(1000)


    def on_lick(self):
        btn = self.sender()
        self.moves_lable.setText(f"Moves: {self.moves_count}")
        for x in range(self.num):
            for y in range(self.num):
                if btn == self.matrix[x][y]:
                    if self.matrix[x][y].text != " ":
                        if y > 0 and self.matrix[x][y-1].text() == " ":
                            text = self.matrix[x][y].text()
                            self.matrix[x][y].setText(" ")
                            self.matrix[x][y].hide()
                            self.matrix[x][y-1].setText(text)
                            self.matrix[x][y-1].show()
                            self.moves_count += 1
                            self.change_btn_color()


                        if y < self.num - 1 and self.matrix[x][y+1].text() == " ":
                            text = self.matrix[x][y].text()
                            self.matrix[x][y].setText(" ")
                            self.matrix[x][y].hide()
                            self.matrix[x][y+1].setText(text)
                            self.matrix[x][y+1].show()
                            self.moves_count += 1
                            self.change_btn_color()



                        if x > 0 and self.matrix[x-1][y].text() == " ":
                            text = self.matrix[x][y].text()
                            self.matrix[x][y].setText(" ")
                            self.matrix[x][y].hide()
                            self.matrix[x-1][y].setText(text)
                            self.matrix[x-1][y].show()
                            self.moves_count += 1
                            self.change_btn_color()


                        if x < self.num - 1 and self.matrix[x+1][y].text() == " ":
                            text = self.matrix[x][y].text()
                            self.matrix[x][y].setText(" ")
                            self.matrix[x][y].hide()
                            self.matrix[x+1][y].setText(text)
                            self.matrix[x+1][y].show()
                            self.moves_count += 1
                            self.change_btn_color()
        self.check_martix()


    def check_martix(self):
        sec = self.sec
        moves = self.moves_count
        for i in range(self.num):
            for j in range(self.num):
                if self.matrix[i][j].text() != self.real_matrix[i][j]:
                    return
        self.time.stop()
        self.winner = WinnerWindow(sec, moves)
        self.close()  




    def handle_timeout(self):
        self.sec += 1
        self.time_lable.setText(f"Time: {self.sec}")
    def resetWindow(self):
        self.sec = 0
        self.moves_count = 0
        self.time_lable.setText("Time: 0")
        self.moves_lable.setText("Moves: 0")
        self.numbers = self.fill_number()
        self.reset_buttom()
        self.start_time()

    
    def reset_buttom(self):
        index = 0
        for i in range(self.num):
            for j in range(self.num):
                btn = self.matrix[i][j]
                btn.setText(self.numbers[index])
                if btn.text() == " ":
                    btn.hide()
                else:
                    btn.show()
                index += 1
        self.change_btn_color()

    def pause_window(self):
        if self.is_paused:
            self.time.start(1000)
            self.pause_btn.setText("Pause")
            for row in self.matrix:
                for btn in row:
                    btn.setEnabled(True)
                    self.change_btn_color()
        else:
            self.time.stop()
            self.pause_btn.setText("Contiune")
            for row in self.matrix:
                for btn in row:
                    btn.setEnabled(False)
                    btn.setStyleSheet("""
                        background-color: #3b3838;
                        border: none;
                        border-radius: 15px;
                        color: white;
                        font-size: 25px;
                        font-family: Arial, Helvetica, sans-serif;
                        font-weight: 500
                    """)
        self.is_paused = not self.is_paused


class WinnerWindow(QWidget):
    def __init__(self, time, moves) -> None:
        super().__init__()
        self.setFixedSize(450, 400)
        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()
        self.congratulations = QLabel("Congratulations 🎉🎉🎉")
        self.time_lable = QLabel(f"Time: {time}")
        self.moves_lable = QLabel(f"Moves: {moves}")
        self.try_btn = QPushButton("Replay the game")
        self.try_btn.clicked.connect(self.try_game)

        self.h_box.addWidget(self.time_lable, 0, Qt.AlignCenter)
        self.h_box.addWidget(self.moves_lable, 0, Qt.AlignCenter)

        self.v_box.addWidget(self.congratulations, 0, Qt.AlignCenter)
        self.v_box.addLayout(self.h_box)
        self.v_box.addWidget(self.try_btn, 0, Qt.AlignCenter)

        self.setLayout(self.v_box)
        self.show()
        # style
        self.setStyleSheet("""
            background-color: #F8EDED;
        """)
        self.congratulations.setStyleSheet("""
            font-size: 30px;
            font-family: Arial, Helvetica, sans-serif;
            font-weight: 600;
            color: #180161;
        """)
        self.time_lable.setStyleSheet("""
            font-size: 30px;
            font-weight: 600;
            color: #180161;
            font-family: Arial, Helvetica, sans-serif;
        """)
        self.moves_lable.setStyleSheet("""
            font-size: 30px;
            font-weight: 600;
            color: #180161;
            font-family: Arial, Helvetica, sans-serif;
        """)
        self.try_btn.setFixedSize(200, 50)
        self.try_btn.setStyleSheet("""
            QPushButton{
                font-size: 20px;
                background-color: #FF8225;
                border: none;
                border-radius: 15px;
                color: #4F1787;
            }
            QPushButton:hover{
                background-color: #F8EDED;
                border: 2px solid #FF8225;
                color: FF8225;
            }
        """)
        # 
    def try_game(self):
        self.game = StepSelection()
        self.close()

app = QApplication([])
game = StepSelection()
app.exec_()















