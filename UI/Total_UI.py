import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QPushButton, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QStackedWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import threading

# class MyTableWidget(QTableWidget):
#     def __init__(self, rows, columns):
#         super().__init__(rows, columns)

#         # Add checkboxes to each row
#         for row in range(rows):
#             checkbox = QCheckBox()
#             self.setCellWidget(row, 0, checkbox)  # Place the checkbox in the first column

class BackgroundTask:
    def __init__(self):
        self.running = False
        super().__init__()

    def start(self):
        self.running = True
        # Your Python code goes here. For example, a loop:
        while self.running:
            print("Script is")
            # Add your code or function call here

    def stop(self):
        self.running = False

class MainApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Stacked Widget for switching between login and main app
        self.stackedWidget = QStackedWidget(self)

        # Login UI Setup
        self.loginWidget = QWidget()
        loginLayout = QVBoxLayout()
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton('Login')
        self.loginButton.clicked.connect(self.checkCredentials)
        loginLayout.addWidget(QLabel('Username'))
        loginLayout.addWidget(self.usernameLineEdit)
        loginLayout.addWidget(QLabel('Password'))
        loginLayout.addWidget(self.passwordLineEdit)
        loginLayout.addWidget(self.loginButton)
        self.loginWidget.setLayout(loginLayout)

        # Main Application UI Setup
        self.mainWidget = QWidget()
        mainLayout = QVBoxLayout(self.mainWidget)

        # Horizontal Layout for Logo, Label, and Dropdown
        topLayout = QHBoxLayout()

        # Logo Image
        logoLabel = QLabel()
        pixmap = QPixmap('D:/Work/WebScraping/test/UI/logo.jpg').scaled(70, 70, Qt.KeepAspectRatio)  # Resize logo
        logoLabel.setPixmap(pixmap)
        topLayout.addWidget(logoLabel)

        # Text Label
        self.textLabel = QLabel("Welcome")  # Initially set default text
        topLayout.addWidget(self.textLabel)

        # Dropdown Menu
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Galatasaray - Karagümrükspor", "Galatasaray - Çaykur Rizespor", "Karagümrükspor - Çaykur Rizespor"])
        self.comboBox.currentIndexChanged.connect(self.updateTableData)  # Connect signal to slot
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        topLayout.addWidget(self.comboBox)

        # Add topLayout to mainLayout
        mainLayout.addLayout(topLayout)

        # Data Table
        self.tableWidget = QTableWidget(1, 10)  # Example: 5 rows and 10 columns
        self.tableWidget.setHorizontalHeaderLabels(["Checkbox", "Ticket Category", "Ticket Format", "Quantity", "SELL","Side by Side", "Advert No", "Order", "Earning","Price", "Min"])
        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: red;  # Header background color
                color: white;  # Header text color
                font-size: 12pt;
            }
        """)
        mainLayout.addWidget(self.tableWidget)

        # Add widgets to StackedWidget
        self.stackedWidget.addWidget(self.loginWidget)
        self.stackedWidget.addWidget(self.mainWidget)

        # Set the stacked widget as the central widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stackedWidget)

        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.toggle_start_stop)
        mainLayout.addWidget(self.button)

        # Background Task
        self.task = BackgroundTask()
        self.task_thread = threading.Thread(target=self.task.start)

        for row in range(self.tableWidget.rowCount()):
            checkbox = QCheckBox()
            row_layout = QHBoxLayout()
            mainLayout.addWidget(checkbox)
            for col in range(self.tableWidget.columnCount()):
                item = QTableWidgetItem(f"Row {row}, Col {col}")
                self.tableWidget.setItem(row, col, item)
            cell_widget = QWidget()
            cell_widget.setLayout(row_layout)
            self.tableWidget.setCellWidget(row, 0, cell_widget)

        self.show()

    def checkCredentials(self):
        # Placeholder for credentials check
        self.stackedWidget.setCurrentIndex(1)

    def on_combobox_changed(self, index):
    # Slot method to update label text
        selected_text = self.comboBox.itemText(index)
        self.textLabel.setText(f"{selected_text}")
    def updateTableData(self, index):
        # Clear current data in the table
        self.tableWidget.clearContents()

        # Example data based on dropdown selection
        data = {
            0: [["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]],  # Data for Option 1
            1: [["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]],  # Data for Option 2
            2: [["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]]  # Data for Option 3
        }

        selected_data = data.get(index, [])
        self.tableWidget.setRowCount(len(selected_data))
        # Populate the table with new data
        for i, row in enumerate(data.get(index, [])):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(val))
    def toggle_start_stop(self):
        if self.button.text() == 'Start':
            self.button.setText('Stop')
            if not self.task_thread.is_alive():
                self.task_thread = threading.Thread(target=self.task.start)
                self.task_thread.start()
        else:
            self.button.setText('Start')
            self.task.stop()
            
# PyQt App Initialization
app = QApplication(sys.argv)
window = MainApplication()
window.show()
sys.exit(app.exec_())