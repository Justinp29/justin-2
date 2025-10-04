import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora de Justin')
        self.setFixedSize(400, 600) 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)
        
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)  
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet("font-size: 40px; border: 1px solid gray;")
        
        self.main_layout.addWidget(self.display, 0, 0, 1, 4) 
        
        self.buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), 
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), 
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), 
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)  
        ]
        
        for text, row, col in self.buttons:
            button = QPushButton(text)
            button.setFixedSize(100, 100) 
            button.setStyleSheet("font-size: 30px;")

            if text.isdigit() or text == '.':
                button.clicked.connect(lambda _, t=text: self.append_digit(t))
            elif text in '+-*/':
                button.clicked.connect(lambda _, t=text: self.set_operator(t))
            elif text == '=':
                button.setStyleSheet("background-color: orange; color: white; font-size: 30px;")
                button.clicked.connect(self.calculate_result)
            
            self.main_layout.addWidget(button, row, col)

        self.full_expression = ''
        self.new_number = True
    
    def append_digit(self, digit):
        current_text = self.display.text()
        
        if self.new_number:
            if digit == '.':
                self.display.setText('0.')
            else:
                self.display.setText(digit)
            self.new_number = False
        else:
            if digit == '.' and '.' in current_text:
                return
            self.display.setText(current_text + digit)

    def set_operator(self, op):
        current_value = self.display.text()
        
        if current_value == '':
            return
            
        if self.full_expression:
            self.calculate_result() 
            
        self.full_expression = self.display.text() + ' ' + op
        self.new_number = True
    
    def calculate_result(self):
        if not self.full_expression:
            return
        try:
            expression = self.full_expression + ' ' + self.display.text()
            
            result = str(eval(expression))
            
            self.display.setText(result)
            self.full_expression = '' 
            self.new_number = True 
            
        except Exception:
            self.display.setText('Error')
            self.full_expression = ''
            self.new_number = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())