from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (Header, Footer, Input, Button, Label, Tree, DirectoryTree, LoadingIndicator)

import datetime

from azure_log_viewer.helpers.obtain_files_paths import get_files_paths
from azure_log_viewer.utils.logs_files_processing import readLogs
from azure_log_viewer.widgets.azure_directory_tree import AzureDirectoryTree

class LogViewer(Screen):
    CSS = """
    #sidebar {
        width: 30%;
        border: round skyblue;
    }

    #main {
        width: 70%;
        layout: vertical;
    }

    #filters {
        height: 20%;
        border: round skyblue;
        padding: 1;
        layout: horizontal;
    }

    #logs {
        border: round skyblue;
        padding: 1;
        height: 40%;
    }

    #results {
        border: round skyblue;
        padding: 1;
        height: 40%;
    }

    Input {
        width: 1fr;
        margin-right: 1;
    }

    Button {
        width: 20;
    }
    """

    account_name: str | None = None
    account_key: str | None = None
    share_name: str | None = None

    result_label: Label | None = None
    start_date_label: Label | None = None
    end_date_label: Label | None = None

    def __init__(self, credentials: dict):
        super().__init__()
        self.account_name = credentials['account_name']
        self.account_key = credentials['account_key']
        self.share_name = credentials['share_name']

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Horizontal():
            # Sidebar tree
            yield Container(id="sidebar")
            
            # Main panel
            with Container(id="main"):
                # Filters section
                with Container(id="filters"):
                    self.start_input = Input(placeholder="Fecha de inicio (AAAA-MM-DD)", id="start_date")
                    self.end_input = Input(placeholder="Fecha de fin (AAAA-MM-DD)", id="end_date")
                    yield self.start_input
                    yield self.end_input
                    yield Button("Ejecutar", id="apply_filters")
                
                # Logs section
                with Container(id="logs"):
                    self.result_label = Label("Aquí se mostrará la cantidad de archivos .log a analizar.")
                    self.start_date_label = Label("Fecha de inicio: -")
                    self.end_date_label = Label("Fecha de fin: -")
                    yield self.result_label
                    yield self.start_date_label
                    yield self.end_date_label

                # Results section
                with Container(id="results"):
                    # self.loading = LoadingIndicator()
                    self.unique_complaints = Label("A")
                    # self.loading.display = False
                    self.unique_complaints.display = False
                    # yield self.loading
                    yield self.unique_complaints
    
    async def on_mount(self) -> None:
        self.title = "SCD Activity viewer"

        sidebar = self.query_one("#sidebar")
        sidebar.border_title = "Directorio Azure - SCD"
        self.query_one("#filters").border_title = "Rango de fechas (Obligatorio)"
        self.query_one("#logs").border_title = "Ejecución"
        self.query_one("#results").border_title = "Resultado"

        loading = LoadingIndicator()
        await sidebar.mount(loading)

        azure_tree = AzureDirectoryTree(
            account_name=self.account_name,
            account_key=self.account_key,
            share_name=self.share_name,
            id="folder_tree"
        )

        self.run_worker(self.load_tree(sidebar=sidebar, azure_tree=azure_tree))

    async def load_tree(self, sidebar, azure_tree):
        try:
            await azure_tree._load_root()
            sidebar.remove_children()
            sidebar.mount(azure_tree)
        except Exception as e:
            print("Azure tree loading failed:", e)

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "apply_filters":
            # self.loading.display = False
            self.unique_complaints.display = False

            start_date_input = self.start_input.value
            end_date_input = self.end_input.value

            start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d").date()
            
            self.result_label.update("Buscando archivos .log...")

            self.run_worker(
                lambda: self.process_log_worker(
                    account_name=self.account_name,
                    account_key=self.account_key,
                    share_name=self.share_name,
                    filename="systemlog.log",
                    start_date=start_date,
                    end_date=end_date
                    ),
                name="process_logs",
                thread=True
            )

            self.start_date_label.update(f"Fecha de inicio: {start_date}")
            self.end_date_label.update(f"Fecha de fin: {end_date}")
    
    def process_log_worker(self, account_name, account_key, share_name, filename, start_date, end_date):
        logs = get_files_paths(
            account_name=account_name,
            account_key=account_key,
            share_name=share_name,
            filename=filename
        )

        self.app.call_from_thread(
            lambda: self.result_label.update(f"Se encontraron {len(logs)} archivos .log. Analizando...")
        )

        unique_complaints = readLogs(logs, start_date, end_date, account_name, account_key, share_name)

        def update_ui():
            # self.loading.display = False
            self.unique_complaints.display = True

            self.result_label.update("Archivos .log analizados exitosamente.")
            self.unique_complaints.update(f"{unique_complaints} reportes han sido registrados y/o se les han agregado comentarios.")
        
        self.app.call_from_thread(update_ui)