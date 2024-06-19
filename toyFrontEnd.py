import sys
import toyBackEnd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QFrame

class evoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initButtons()
        self.initDisplay()
        self.initUI()
        
    def initButtons(self):
        # Make a vertical layout for the buttons
        button_layout = QVBoxLayout()
        self.up_button = QPushButton('Up', self)
        self.select_button = QPushButton('Select', self)
        self.down_button = QPushButton('Down', self)
        self.OD_button = QPushButton('Plot OD', self)

        # Button Functionality
        self.up_button.clicked.connect(self.up_clicked)
        self.select_button.clicked.connect(self.sel_clicked)
        self.down_button.clicked.connect(self.down_clicked)
        self.OD_button.clicked.connect(self.OD_clicked)

        # Button layout
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.down_button)
        button_layout.addStretch()  # Add a stretch at the end to keep buttons together
        button_layout.addWidget(self.OD_button)

        self.button_layout = button_layout

    def initDisplay(self):
        # Create a grid layout for the labels inside a frame
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(2)
        
        grid_layout = QGridLayout(frame)
        
        # Create labels
        self.uptime_label = QLabel('Uptime:', self)
        self.uptime_display = QLabel('0:00:00', self)
        
        self.ambient_temp_label = QLabel('Ambient Temperature:', self)
        self.ambient_temp_display = QLabel('0°C', self)
        
        self.media_temp_label = QLabel('Media Temperature:', self)
        self.media_temp_display = QLabel('0°C', self)
        
        self.heaterplate_temp_label = QLabel('HeaterPlate Temperature:', self)
        self.heaterplate_temp_display = QLabel('0°C', self)
        
        self.ir_label = QLabel('IR:', self)
        self.ir_display = QLabel('0', self)
        
        self.od_label = QLabel('OD:', self)
        self.od_display = QLabel('0', self)

        # Add labels to the grid layout
        grid_layout.addWidget(self.uptime_label, 0, 0)
        grid_layout.addWidget(self.uptime_display, 0, 1)
        
        grid_layout.addWidget(self.ambient_temp_label, 1, 0)
        grid_layout.addWidget(self.ambient_temp_display, 1, 1)
        
        grid_layout.addWidget(self.media_temp_label, 2, 0)
        grid_layout.addWidget(self.media_temp_display, 2, 1)
        
        grid_layout.addWidget(self.heaterplate_temp_label, 3, 0)
        grid_layout.addWidget(self.heaterplate_temp_display, 3, 1)
        
        grid_layout.addWidget(self.ir_label, 4, 0)
        grid_layout.addWidget(self.ir_display, 4, 1)
        
        grid_layout.addWidget(self.od_label, 5, 0)
        grid_layout.addWidget(self.od_display, 5, 1)

        self.frame = frame

    def initUI(self):
        # Initialize main layout
        main_layout = QHBoxLayout()

        # Add button layout and frame layout to the main layout
        main_layout.addLayout(self.button_layout)
        main_layout.addWidget(self.frame)

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Window settings
        self.setWindowTitle('easyEVO')
        self.setGeometry(300, 300, 600, 400)

        self.show()
    
    def up_clicked(self):
        print("Up button clicked")

    def sel_clicked(self):
        print("Select button clicked")

    def down_clicked(self):
            print("Down button clicked")

    def OD_clicked(self):
        toyBackEnd.plot_OD()




if __name__ == '__main__':
    # toyBackEnd.init_BackEnd_Connection()
    app = QApplication(sys.argv)
    ex = evoUI()
    sys.exit(app.exec_())
