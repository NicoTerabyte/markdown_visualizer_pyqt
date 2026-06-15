from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from markdown_visualizer import HtmlVisualizer
import sys
import signal

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Setup of the elements
		self.setWindowTitle("test")
		self.html_button = QPushButton("Guide")
		self.setMinimumSize(700, 500)

		# setup of the window
		self.top_container = QWidget()
		self.main_layout = QVBoxLayout()
		self.design_setup()

		#signal button handling
		self.html_button.clicked.connect(self.open_html_window)

		#html window handling
		#testing the possibility to handle multiple windows at once
		self.html_windows_handler = []
		self.html_window = HtmlVisualizer()

	def show(self):
		super().show()

	def design_setup(self):
		print("setting layout")
		self.main_layout.addWidget(self.html_button)
		self.top_container.setLayout(self.main_layout)
		self.setCentralWidget(self.top_container)

	'''
	it uses another class that basically does that reader and displayer of html
	files.
	'''
	def open_html_window(self):
		print("opening window")
		html_window = HtmlVisualizer()
		self.html_windows_handler.append(html_window)
		html_window.show()

	def closeEvent(self, event):
		for window in self.html_windows_handler:
			window.close()

		# if you don't send the event a traceback will occur
		super().closeEvent(event)

if __name__ == "__main__":
	app = QApplication([])
	main_window = MainWindow()

	main_window.show()
	app.exec()
	print("finiamo")
