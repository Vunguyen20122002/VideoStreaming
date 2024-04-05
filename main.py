import sys
import json
import os.path
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QPushButton, QHBoxLayout, QCheckBox, QComboBox, QProgressBar
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SocialMediaViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player Video Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)
        self.url_input.setStyleSheet("border-radius: 5px; padding: 5px; font-size: 16px;")

        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.load_media)
        self.layout.addWidget(self.open_button)
        self.open_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 5px;font-size: 16px;")

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)
        self.save_button.setStyleSheet("background-color: #FF9800; color: white; border-radius: 10px; padding: 5px;font-size: 16px;")
        
        self.combobox_option = QComboBox()
        self.layout.addWidget(self.combobox_option)
        self.combobox_option.addItem("Chọn video của bạn")
        self.combobox_option.addItem("Video 1")
        self.combobox_option.addItem("Video 2")
        self.combobox_option.setStyleSheet("border-radius:5px; padding:5px;font-size: 16px;")
        
        self.process_bar = QProgressBar()
        self.process_bar.setStyleSheet("border-radius: 10px; padding: 0.1px;border: 1px solid;")

        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)
        self.webview.loadProgress.connect(self.process_video)
        
        
        hbox_layouts = QHBoxLayout()
        self.layout.insertLayout(0, hbox_layouts)
        self.layout.addLayout(hbox_layouts)
        hbox_layouts.addWidget(self.url_input)
        hbox_layouts.addWidget(self.open_button)
        hbox_layouts.addWidget(self.save_button)
        
        hbox_layout = QHBoxLayout()
        self.layout.addLayout(hbox_layout)
        hbox_layout.addWidget(self.process_bar)
         
        self.saved_urls = []
        
    def save(self):
        url = self.url_input.text().strip()  # Remove leading/trailing whitespace

        # Check if file exists
        if not os.path.isfile("list_video.json"):
            # File doesn't exist, create it
            with open("list_video.json", "w") as f:
                json.dump([], f, indent=4)  # Create an empty list in the file
                # Check if URL is empty
                if not url:
                    QMessageBox.warning(self, "Empty URL", "Please enter a valid URL to save.")
                    return

        # Read existing data from JSON file
        try:
            with open("list_video.json", "r") as f:
                self.saved_urls = json.load(f)
        except FileNotFoundError:
            return

        # Check if URL already exists
        if any(item["url"] == url for item in self.saved_urls):
            QMessageBox.warning(self, "Duplicate URL", f"The URL '{url}' already exists in your list.")
            return

        # Get the highest ID from existing data
        max_id = 0
        for item in self.saved_urls:
            if item["id"] > max_id:
                max_id = item["id"]

        # Generate a new ID
        new_id = max_id + 1

        # Add new URL to existing data
        self.saved_urls.append({"id": new_id, "url": url})

        # Save updated data to JSON file
        try:
            with open("list_video.json", "w") as f:
                json.dump(self.saved_urls, f, indent=4)  # Add indentation for readability
        except Exception as e:
            QMessageBox.warning(self, "Save Error", "An error occurred while saving data.")

        print(f"Saved URL '{url}' with ID {new_id} to list.")

    def load_media(self):
        url = self.url_input.text()
        embed_url = None

        if "youtube.com" in url:
            try:
                video_id = self.get_video_id(url)
                if video_id:
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    self.webview.load(QUrl(embed_url))
                else:
                    QMessageBox.warning(self, "Invalid URL", "Please enter a valid YouTube video URL.")
            except Exception as e:
                QMessageBox.warning(self, "Load Error", "An error occurred while loading the video.")
        else:
            QMessageBox.warning(self, "Invalid URL", "Please enter a YouTube video URL.")

        return embed_url

    def get_video_id(self, url):
        if "youtube.com" in url and "v=" in url:
            index = url.index("v=")
            video_id = url[index + 2:]
            if "&" in video_id:
                video_id = video_id[:video_id.index("&")]
            return video_id
        else:
            return None
        
    def process_video(self,process_url):
        self.process_bar.setValue(process_url)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialMediaViewer()
    window.show()
    sys.exit(app.exec_())
