from PyQt5.QtWidgets import QWidget, QVBoxLayout, QBoxLayout, QTextBrowser, QFileDialog
from PyQt5.QtCore import QUrl

'''
This class purpose is to show and render properly html files
if the file is an html one is rendered properly, otherwise it will be
read as a raw file
'''
class HtmlVisualizer(QWidget):
	def __init__(self):
		super().__init__()

		# normal setup
		self.md_layout = QVBoxLayout()
		self.md_text = QTextBrowser()
		self.setMinimumSize(700, 500)

		#file handling and reading of the single markdown
		self.file_content = ""

		#layout for the markdown text to do at the end
		self.md_layout.addWidget(self.md_text)
		self.setLayout(self.md_layout)

	def read_and_save_html(self, file_to_read: str):
		try:
			with open(file_to_read, "r") as md_file:
				self.file_content = md_file.read()
		except FileNotFoundError as e:
			print("Warning, file to open not found")

	# the actual show of this class sets the data as well
	# unfortunately for the old system "setMarkdown" is too new
	def show_future(self):
		super().show()
		if self.file_content != "":
			self.md_text.setMarkdown(self.file_content)
		else:
			print("the file is empty")
			self.md_text.setText("file non existent or empty")

	'''
	The logic is:
	i push the guide button in the main window --> i select
	the file that i want to read -> i open it
	i prefere to separate the logic of saving the file and select it i two separate functions

	There's no need to check if the file is an html, since the show opens it anyway
	'''
	def show(self):
		self.read_and_save_html(self.select_file_to_read())
		super().show()
		if self.file_content != "":
			self.md_text.setHtml(self.file_content)
		else:
			print("the file is empty")
			self.md_text.setText("file non existent or empty")

	'''
	file selector
	getOpenFileName() -> returns a tuple
	'''
	def select_file_to_read(self):
		res = QFileDialog.getOpenFileName()
		print("retrieved file {}".format(res[0]))
		return res[0]
