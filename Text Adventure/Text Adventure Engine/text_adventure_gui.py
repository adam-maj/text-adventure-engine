#========================================
#Title: Text Adventure GUI

#Creator: Adam Majmudar

#Date Created: Wednesday, July 4th, 2018

#Change Log: https://tinyurl.com/y7lzltvk
#========================================

import sys
import PyQt5.QtWidgets as Qt
import text_adventure_engine as txt
from PyQt5.QtGui import QFont


class Window(Qt.QWidget):
    
    def __init__(self, name):
        """
        <name>: Name of the window
        """
        
        super().__init__()
        
        self.name = name
        self.init_UI()
        
    def init_UI(self):
        """
        This function creates the entire user interface
        """
        
        self.output_layout = OutputLayout()

        self.input_layout = InputLayout()
        self.input_layout.submit_button.clicked.connect(self.submit_command)

        self.layout = Qt.QVBoxLayout()
        self.layout.addLayout(self.output_layout)
        self.layout.addLayout(self.input_layout)        
        
        self.setLayout(self.layout)
        self.setWindowTitle(self.name)
        self.show()
        
        self.output_layout.print_to_console(txt.get_start_description())
        self.output_layout.update_display()
        
    def submit_command(self):
        """
        Dictates what happens when the use clicks the submit button
        
        The user's command is sent to the <text_adventure_engine> file and that file
        returns the string which is printed to the console
        
        Furthermore, the tabs on the information area are updated
        
        Updates both the console and the display through methods inside the
        <OuputLayout> class
        """
        
        self.output_layout.update_console(self.input_layout.command_line.text())
        self.input_layout.command_line.clear()
        self.output_layout.update_display()
        

class OutputLayout(Qt.QHBoxLayout):
    
    def __init__(self):
        
        super().__init__()
        
        self.init_UI()
    
    def init_UI(self):
        """
        Creates the Output Layout consisting of a console where the text adventure
        plays out and a display to view various game statistic
        """
        
        self.console = CustomTextEdit()
        self.inventory = CustomTextEdit()
        self.stats = CustomTextEdit()
        self.help = CustomTextEdit()
        self.description = CustomTextEdit()
        
        self.upper_label = Qt.QLabel("Player Information:")
        
        self.lower_label = Qt.QLabel("Game Information:")
        
        self.upper_display = Qt.QTabWidget()
        self.upper_display.addTab(self.inventory, "Inventory")
        self.upper_display.addTab(self.stats, "Stats")
        
        self.lower_display = Qt.QTabWidget()
        self.lower_display.addTab(self.help, "Help")
        self.lower_display.addTab(self.description, "Description")
        
        self.display = Qt.QVBoxLayout()
        self.display.addWidget(self.upper_label)
        self.display.addWidget(self.upper_display)
        self.display.addWidget(self.lower_label)
        self.display.addWidget(self.lower_display)
        
        self.addWidget(self.console)
        self.addLayout(self.display)
        
        #Cursor implementation necessary to fix the bug where user would click
        #On the console and the text would print in the wrong area
        self.cursor = self.console.textCursor()
        
    
    def print_to_console(self, text):
        """
        Simple command that prints any given text to the console
        
        Makes it easier to make a typewriter feature on the console if desired
        """
        
        self.console.insertPlainText(text)
    
    def update_console(self, command):
        """
        Prints the result of the given command to the console through the
        <print_to_console> function
        """
        
        #Read comment above on cursor creation
        self.console.moveCursor(self.cursor.End)
        self.print_to_console(txt.run_text_adventure_engine(command))
        
    def update_display(self):
        """
        Updates the tabs on the display
        """
        
        self.inventory.clear()
        self.inventory.insertPlainText(txt.get_inventory())
        
        self.stats.clear()
        self.stats.insertPlainText(txt.get_player_stats())
        
        
class InputLayout(Qt.QHBoxLayout):
    
    def __init__(self):
        
        super().__init__()
        
        self.init_UI()
        
    def init_UI(self):
        """
        Creates a simple input layout with a command line to enter text and a button
        to submit the command.
        
        The button is connected to a command in the main <Window> class 
        <submit_command> function
        """
        
        self.command_line = Qt.QLineEdit()
        self.addWidget(self.command_line)
        
        self.submit_button = Qt.QPushButton("Submit")
        self.addWidget(self.submit_button)
        

class CustomTextEdit(Qt.QTextEdit):
    
    def __init__(self):
        """
        This class sets up a text edit widget in the font Courier which is set
        to read only mode
        """
        
        super().__init__()
        
        my_font = QFont("Courier", 10)
        self.setCurrentFont(my_font)
        self.setReadOnly(True)
        
        
def start_engine(x_dist = 420, y_dist = 150, length = 500, width = 500,
                 title = "Text Adventure Engine"):

    """
    Starts the text_adventure_engine loop
    
    <x_dist>: Distance from the left screen edge
    
    <y_dist>: Distance from upper screen edge
    
    <length>, <width>: Initial window dimensions
    
    <title>: Window title    
    """
        
    my_app = Qt.QApplication(sys.argv)
    my_window = Window(title)
    my_window.setGeometry(x_dist, y_dist, length, width)
    sys.exit(my_app.exec_())