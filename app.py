from textual.app import App

from screens.credentials import CredentialsScreen
from screens.logs_viewer import LogViewer

class Main(App):
    SCREENS = {
        "credentials": CredentialsScreen,
        "log_viewer": LogViewer
    }

    def on_mount(self):
        # self.push_screen(LogViewer(credentials=data))
        self.push_screen("credentials", self.on_credentials_entered)

    def on_credentials_entered(self, credentials):
        if credentials is None:
            self.exit()
            return
        
        self.push_screen(LogViewer(credentials=credentials))

if __name__ == "__main__":
    app = Main()
    app.run()