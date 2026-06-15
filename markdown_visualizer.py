from PyQt5.QtWidgets import QWidget, QVBoxLayout, QBoxLayout, QHBoxLayout, QTextBrowser, QFileDialog, QLineEdit, QLabel

from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QUrl
from utils import total_of_occurencies


'''
This class purpose is to show and render properly html files
if the file is an html one is rendered properly, otherwise it will be
read as a raw file, if no file it's given or the file it's empty, the page will simply tell that
the file it's empty
'''
class HtmlVisualizer(QWidget):
	def __init__(self):
		super().__init__()

		# normal declaration
		self.main_layout = QVBoxLayout()
		self.html_text_layout = QVBoxLayout()

		#layout for the text in the document
		self.html_text = QTextBrowser()
		self.setMinimumSize(700, 500)

		#mini layout for the searchbar
		self.searchbar_layout = QHBoxLayout()
		self.bar_title = QLabel()
		# the idea is to do something like "1 of 12" of the same word
		self.total_number_of_occurencies = QLabel()
		#todo if you want to make it more stylish you add a counter of which
		#of the occureces you are at
		self.out_of_number_of_occurencies = QLabel()
		self.search_bar = QLineEdit()

		#file content var
		self.file_content = ""

		#various setups
		self.bar_title.setText("Search🔎: ")
		self.search_bar.textChanged.connect(self.update_display)
		self.search_bar.returnPressed.connect(self.find_next)

		self.total_number_of_occurencies.hide()

		#layout widget logic
		#file text layout
		self.html_text_layout.addWidget(self.html_text)

		#searchbar layout
		self.searchbar_layout.addWidget(self.bar_title)
		self.searchbar_layout.addWidget(self.search_bar)
		self.searchbar_layout.addWidget(self.total_number_of_occurencies)
		#then i wrap all the layout to the main layout
		self.main_layout.addLayout(self.searchbar_layout)
		self.main_layout.addLayout(self.html_text_layout)
		self.setLayout(self.main_layout)

	def read_and_save_html(self, file_to_read: str):
		try:
			with open(file_to_read, "r") as html_file:
				self.file_content = html_file.read()
		except FileNotFoundError as e:
			print("Warning, file to open not found")

	# the actual show of this class sets the data as well
	# unfortunately for the old system "setMarkdown" is too new
	def show_future(self):
		super().show()
		if self.file_content != "":
			self.html_text.setMarkdown(self.file_content)
		else:
			print("the file is empty")
			self.html_text.setText("file non existent or empty")

	'''
	The logic is:
	i push the guide button in the main window --> i select
	the file that i want to read -> i open it
	i prefer to separate the logic of saving the file and select it in two separate functions

	There's no need to check if the file is an html, since the show opens it anyway
	'''
	def show(self):
		self.read_and_save_html(self.select_file_to_read())
		super().show()
		if self.file_content != "":
			self.html_text.setHtml(self.file_content)
		else:
			print("the file is empty")
			self.html_text.setText("file non existent or empty")

	'''
	file selector
	getOpenFileName() -> returns a tuple
	in this case the path of the file the user has choosen
	'''
	def select_file_to_read(self):
		res = QFileDialog.getOpenFileName()
		print("retrieved file {}".format(res[0]))
		return res[0]

	'''
	searchbar logic to search in the text window
	The cursor must be controlled in order to not go to the next word while searching.
	find (the method) checks a word and every successive search goes to the next word
	that's troublesome because it would skip the words before, that's why i used
	movecursor, this works only for one word that's why i did find_next.
	'''
	def update_display(self, text: str):
		self.html_text.moveCursor(QTextCursor.Start)
		self.html_text.find(text)
		self.total_number_of_occurencies.setText("found " + str(total_of_occurencies(self.file_content, text)))
		if "0" not in self.total_number_of_occurencies.text():
			self.total_number_of_occurencies.show()
		else:
			self.total_number_of_occurencies.hide()

	'''
	method to check the next word put in the searchbar
	pressing enter will make it go to the next word, you can't go back
	'''
	def find_next(self):
		self.html_text.find(self.search_bar.text())




