from textual.app import App

from azure_log_viewer.screens.credentials import CredentialsScreen
from azure_log_viewer.screens.logs_viewer import LogViewer

class AzureLogViewerApp(App):
    SCREENS = {
        "credentials": CredentialsScreen,
        "log_viewer": LogViewer
    }

    def __init__(self):
        super().__init__()

    def on_mount(self):
        self.push_screen("credentials", self.on_credentials_entered)

    def on_credentials_entered(self, credentials):
        if credentials is None:
            self.exit()
            return
        
        self.push_screen(LogViewer(credentials=credentials))

def main() -> None:
    app = AzureLogViewerApp()
    app.run()