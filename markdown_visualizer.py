from PyQt5.QtWidgets import QWidget, QVBoxLayout, QBoxLayout, QTextBrowser
from PyQt5.QtCore import QUrl

class MarkdowVisualiser(QWidget):
	def __init__(self):
		super().__init__()
		self.md_layout = QVBoxLayout()
		self.md_text = QTextBrowser()
		self.setMinimumSize(700, 500)


		#file handling and reading of the single markdown
		self.file_content = ""
		self.read_and_save_md()

		#layout for te markdown text to do at the end
		self.md_layout.addWidget(self.md_text)
		self.setLayout(self.md_layout)

	def read_and_save_md(self):
		with open("prova.html", "r") as md_file:
			self.file_content = md_file.read()

	# the actual show of this class sets the data as well
	# unfortunately for the old system "setMarkdown" is too new
	def show_future(self):
		super().show()
		if self.file_content != "":
			self.md_text.setMarkdown(self.file_content)
		else:
			print("the file is empty")
			self.md_text.setText("file non existent or empty")

	def show(self):
		super().show()
		if self.file_content != "":
			self.md_text.setHtml(self.file_content)
		else:
			print("the file is empty")
			self.md_text.setText("file non existent or empty")
