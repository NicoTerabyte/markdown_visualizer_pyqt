from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QFileDialog, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QTextCursor, QTextDocument
from utils import count_occurrences


'''
This class purpose is to show and render properly html files
if the file, is an html one is going to be rendered properly, otherwise it will be
shown as a raw file, if no file it's given or the file it's empty, the page will simply tell that
the file it's empty. there are a number of feature to make the navigation of the file more smooth

the class has two main layout one is for the searchbar that should help the user searching for specific
words back and forth in the document that it had opened, the search layout has buttons and some
logic related to the searching of specific words in it.

the other layout is the text layout that simply has the task to render an html file and display it.
There's a specific widget for that, QTextBrowser check it out.

To organize the layouts properly i made a main layout that works as a wrapper for all the layouts in the applicative
'''
class HtmlVisualizer(QWidget):
	def __init__(self):
		super().__init__()

		# normal declaration
		self.occurrence_out_of = 1
		self.counted_occurrences = 0

		self.main_layout = QVBoxLayout()
		self.html_text_layout = QVBoxLayout()
		self.next_button = QPushButton()
		self.previous_button = QPushButton()

		#layout for the text in the document
		self.html_text = QTextBrowser()
		self.setMinimumSize(700, 500)

		#mini layout for the searchbar
		self.searchbar_layout = QHBoxLayout()
		self.bar_title = QLabel()
		self.total_number_of_occurrences = QLabel()
		self.occurrence_out_of_label = QLabel()
		self.search_bar = QLineEdit()

		#file content var
		self.file_content = ""

		#various setups
		##setText
		self.bar_title.setText("Search: ")
		self.next_button.setText("Next occ.")
		self.previous_button.setText("Prev. occ.")
		## signal conenct
		self.search_bar.returnPressed.connect(self.find_next)
		self.search_bar.textChanged.connect(self.update_display)
		self.next_button.pressed.connect(self.find_next)
		self.previous_button.pressed.connect(self.find_previous)
		##others
		self.total_number_of_occurrences.hide()
		self.occurrence_out_of_label.hide()
		#layout widget logic
		#file text layout
		self.html_text_layout.addWidget(self.html_text)

		#searchbar layout widget management
		self.searchbar_layout.addWidget(self.bar_title)
		self.searchbar_layout.addWidget(self.search_bar)
		self.searchbar_layout.addWidget(self.next_button)
		self.searchbar_layout.addWidget(self.previous_button)
		self.searchbar_layout.addWidget(self.occurrence_out_of_label)
		self.searchbar_layout.addWidget(self.total_number_of_occurrences)

		#then i wrap all the layout to the main layout
		self.main_layout.addLayout(self.searchbar_layout)
		self.main_layout.addLayout(self.html_text_layout)
		self.setLayout(self.main_layout)

	def read_and_save_html(self, file_to_read: str):
		try:
			with open(file_to_read, "r") as html_file:
				self.file_content = html_file.read()
		except FileNotFoundError as e:
			print("Warning, file to open not found {}".format(e))
	'''
	the actual show of this class sets the data as well
	unfortunately for the old system "setMarkdown" is too new
	so, this is never used
	'''
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

	tricky logic is the one of the labels that shows the occurrences i made two of them to handle the total number of occurrences
	and one to keep track at which occurence we are at, the first one the total, can be set once,
	instead the other occurence tracker has to be updated every time we move to another occurrence
	both forward and backword
	'''
	def update_display(self, text: str):
		self.html_text.moveCursor(QTextCursor.Start)
		self.html_text.find(text)
		# this label updates over time how at which occurrence of the word the user is at
		self.counted_occurrences = count_occurrences(self.html_text.toPlainText(), text)

		if self.counted_occurrences != 0:
			self.occurrence_out_of = 1
			print("showing number of occurrences")
			self.occurrence_out_of_label.setText("found "+ str(self.occurrence_out_of))
			self.total_number_of_occurrences.setText("/ " + str(self.counted_occurrences))
			self.total_number_of_occurrences.show()
			self.occurrence_out_of_label.show()
		else:
			self.occurrence_out_of = 0
			self.counted_occurrences = 0
			self.total_number_of_occurrences.hide()
			self.occurrence_out_of_label.hide()

	'''
	method to check the next word put in the searchbar
	pressing enter will make it go to the next word
	'''
	def find_next(self):
		if self.occurrence_out_of != 0 and self.occurrence_out_of < self.counted_occurrences:
			self.occurrence_out_of += 1
			self.occurrence_out_of_label.setText("found "+ str(self.occurrence_out_of))
			self.html_text.find(self.search_bar.text())


	'''
	Method to searchbackward. Pylance doesn't seem to find the method "findbackward"
	of the object QTextDocument, but it actually exists
	'''
	def find_previous(self):
		if self.occurrence_out_of != (1 or 0):
			self.occurrence_out_of -= 1
			self.occurrence_out_of_label.setText("found "+ str(self.occurrence_out_of))
			self.html_text.find(self.search_bar.text(), QTextDocument.FindBackward) # type: ignore


