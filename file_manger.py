import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets

class FileExplorer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Explorer")
        self.setup_ui()
        self.directory_history = []  # Track directory history for navigation
        self.current_directory = ""

    def setup_ui(self):
        # Create the layout
        self.layout = QtWidgets.QVBoxLayout()

        # Create the navigation layout
        self.navigation_layout = QtWidgets.QHBoxLayout()

        # Create the back button
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon.fromTheme("go-previous"))

        # Connect button click event to the go_back slot
        self.back_button.clicked.connect(self.go_back)

        # Add the button to the navigation layout
        self.navigation_layout.addWidget(self.back_button)

        # Add the navigation layout to the main layout
        self.layout.addLayout(self.navigation_layout)

        # Create a list widget to display the directory contents
        self.file_list_widget = QtWidgets.QListWidget()
        self.layout.addWidget(self.file_list_widget)

        # Connect double-click event to handle_directory_double_click slot
        self.file_list_widget.itemDoubleClicked.connect(self.handle_directory_double_click)

        # Create buttons for opening and deleting files
        self.open_button = QtWidgets.QPushButton("Open")
        self.delete_button = QtWidgets.QPushButton("Delete")

        # Connect button click events to their respective slots
        self.open_button.clicked.connect(self.handle_open_button_click)
        self.delete_button.clicked.connect(self.handle_delete_button_click)

        # Add buttons to the layout
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

    def list_directory_contents(self, directory):
        try:
            contents = os.listdir(directory)
            self.file_list_widget.clear()
            self.file_list_widget.addItems(contents)
        except OSError as e:
            print(f"Error: {e}")
    

    def handle_directory_double_click(self, item):
        selected_file = item.text()
        selected_path = os.path.join(self.current_directory, selected_file)
        if os.path.isdir(selected_path):
            self.directory_history.append(self.current_directory)  # Save current directory in history
            self.current_directory = selected_path
            self.list_directory_contents(selected_path)

    def handle_open_button_click(self):
        selected_items = self.file_list_widget.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            selected_path = os.path.join(self.current_directory, selected_file)
            if os.path.isfile(selected_path):
                self.open_file(selected_path)

    def go_back(self):
        if self.directory_history:
            previous_directory = self.directory_history.pop()
            self.current_directory = previous_directory
            self.list_directory_contents(previous_directory)

    def open_file(self, file_path):
        try:
            subprocess.run(['xdg-open', file_path])
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def handle_delete_button_click(self):
        selected_items = self.file_list_widget.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            selected_path = os.path.join(self.current_directory, selected_file)
            if os.path.isfile(selected_path):
                self.delete_file(selected_path)

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            print(f"File deleted: {file_path}")
            self.list_directory_contents(self.current_directory)
        except OSError as e:
            print(f"Error: {e}")

    def set_initial_directory(self, directory):
        self.current_directory = directory
        self.list_directory_contents(directory)

# Create the application
app = QtWidgets.QApplication([])

# Create the main window
window = FileExplorer()
home_dir = os.path.expanduser('~')
window.set_initial_directory(home_dir)
window.show()

# Start the application event loop
app.exec_()