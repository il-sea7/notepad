import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTextEdit,
    QPushButton,
    QLabel,
    QMessageBox,
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes App")
        self.setGeometry(200, 200, 600, 400)

        # Set dark theme
        self.set_dark_theme()

        # Create widgets
        self.note_list = QListWidget()
        self.note_text = QTextEdit()
        self.new_note_button = QPushButton("New Note")
        self.save_note_button = QPushButton("Save Note")
        self.delete_note_button = QPushButton("Delete Note")
        self.search_label = QLabel("Search:")
        self.search_input = QTextEdit()

        # Set fonts
        font = QFont()
        font.setPointSize(12)
        self.note_text.setFont(font)
        self.search_input.setFont(font)

        # Create layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Add widgets to layouts
        left_layout.addWidget(self.note_list)
        left_layout.addWidget(self.new_note_button)
        left_layout.addWidget(self.delete_note_button)

        right_layout.addWidget(self.note_text)
        right_layout.addWidget(self.save_note_button)
        right_layout.addWidget(self.search_label)
        right_layout.addWidget(self.search_input)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect signals and slots
        self.new_note_button.clicked.connect(self.create_note)
        self.save_note_button.clicked.connect(self.save_note)
        self.delete_note_button.clicked.connect(self.delete_note)
        self.note_list.itemClicked.connect(self.on_note_select)
        self.search_input.textChanged.connect(self.search_notes)

        # Initialize notes list and selected note variables
        self.notes = []
        self.selected_note = None

        # Load existing notes
        self.load_notes()

    def set_dark_theme(self):
        # Set dark background color
        self.setStyleSheet(
            "background-color: #222222; color: #FFFFFF; selection-color: #FFFFFF; selection-background-color: #555555"
        )

        # Set text color for disabled buttons
        self.new_note_button.setStyleSheet("color: #AAAAAA")
        self.delete_note_button.setStyleSheet("color: #AAAAAA")

    def create_note(self):
        self.selected_note = None
        self.note_text.clear()

    def save_note(self):
        note_content = self.note_text.toPlainText().strip()

        if note_content:
            if self.selected_note:
                # Update existing note
                index = self.notes.index(self.selected_note)
                self.notes[index] = note_content
                self.note_list.item(index).setText(note_content)
            else:
                # Create new note
                self.notes.append(note_content)
                self.note_list.addItem(note_content)
                self.note_list.setCurrentRow(self.note_list.count() - 1)
                self.selected_note = note_content

            self.save_notes()
            QMessageBox.information(self, "Note Saved", "Note has been saved successfully.")

    def delete_note(self):
        if self.selected_note:
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                "Are you sure you want to delete the note?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                index = self.notes.index(self.selected_note)
                self.note_list.takeItem(index)
                self.notes.pop(index)
                self.note_text.clear()
                self.selected_note = None
                self.save_notes()
                QMessageBox.information(self, "Note Deleted", "Note has been deleted successfully.")

    def on_note_select(self, item):
        self.selected_note = item.text()
        self.note_text.setText(self.selected_note)

    def search_notes(self):
        keyword = self.search_input.toPlainText().strip().lower()

        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            note = item.text().lower()
            if keyword in note:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def load_notes(self):
        try:
            with open("notes.txt", "r") as file:
                self.notes = [line.strip() for line in file.readlines()]
                for note in self.notes:
                    self.note_list.addItem(note)
        except FileNotFoundError:
            self.notes = []

    def save_notes(self):
        with open("notes.txt", "w") as file:
            file.writelines("\n".join(self.notes))

    def closeEvent(self, event):
        self.save_notes()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes_app = NotesApp()
    notes_app.show()
    sys.exit(app.exec_())
