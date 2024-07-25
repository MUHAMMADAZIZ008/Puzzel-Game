from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QGridLayout

)
from puzzle_game import Window

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
        print(self.selection_rd)
        self.game_puzzle = Window(select)
        self.close()
app = QApplication([])
step = StepSelection()
app.exec_()