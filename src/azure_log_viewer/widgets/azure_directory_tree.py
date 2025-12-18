from textual.widgets import Tree, DirectoryTree
from azure.storage.fileshare import ShareDirectoryClient

class AzureDirectoryTree(DirectoryTree):
    def __init__(self, account_name, account_key, share_name, **kwargs):
        super().__init__(share_name, **kwargs)
        self.account_name = account_name
        self.account_key  = account_key
        self.share_name   = share_name
        
        if account_name and share_name:
            self.root_dir = ShareDirectoryClient(
                account_url=f"https://{account_name}.file.core.windows.net",
                directory_path="",
                credential=account_key,
                share_name=share_name
            )
        else:
            self.root_dir = None

    async def on_mount(self):
        self.call_later(self._load_root)

    async def _load_root(self):
        try:
            await self.load_dir(self.root, self.root_dir)
            self.root.expand()
            self.refresh()
        except Exception as e:
            print("Azure load error:", e)

    async def load_dir(self, node, dir_client):
        try:
            for item in dir_client.list_directories_and_files():
                if item["is_directory"]:
                    child = node.add(item["name"])
                    subdir_client = dir_client.get_subdirectory_client(item["name"])
                    await self.load_dir(child, subdir_client)
                else:
                    node.add_leaf(item["name"])
                self.refresh(layout=True)
        except Exception as e:
            print(f"Error loading directory: {e}")
            self.refresh(layout=True)