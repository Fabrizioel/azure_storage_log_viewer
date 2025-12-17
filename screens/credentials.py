from textual.screen import Screen
from textual.widgets import Input, Button, Label
from textual.containers import Vertical, Horizontal

class CredentialsScreen(Screen[dict]):
    CSS="""
    #credentials_container {
        height: auto;
        border: round skyblue;
        padding: 1;
    }

    Input {
        margin-bottom: 1;
    }

    #access_button {
        margin-left: 1;
    }
    """

    def compose(self):
        yield Vertical(
            Input(placeholder="Account name", id="account_name"),
            Input(placeholder="Account key", id="account_key"),
            Input(placeholder="Share name", id="share_name"),
            Button("Acceder", id="access_button"),
            id="credentials_container"
        )

    def on_mount(self) -> None:
        container = self.query_one("#credentials_container")
        container.border_title = "Credenciales Azure Web Storage"
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "access_button":
            account_name = self.query_one("#account_name", Input).value
            account_key = self.query_one("#account_key", Input).value
            share_name = self.query_one("#share_name", Input).value

            data = {
                "account_name": account_name,
                "account_key": account_key,
                "share_name": share_name
            }
            
            self.dismiss(data)