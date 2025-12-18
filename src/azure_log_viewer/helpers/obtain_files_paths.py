from azure.storage.fileshare import ShareDirectoryClient

def get_files_paths(account_name, account_key, share_name, filename):
    root = ShareDirectoryClient(
        account_url=f"https://{account_name}.file.core.windows.net/",
        share_name=share_name,
        credential=account_key,
        directory_path=""
    )

    files_paths=[]

    for item in root.list_directories_and_files():
        if item['is_directory']:
            folder_name = item['name']
            folder_client = root.get_subdirectory_client(folder_name)

            try:
                for sub_item in folder_client.list_directories_and_files():
                    if not sub_item['is_directory'] and sub_item['name'].endswith(f"{filename}"):
                        files_paths.append(f"{folder_name}/{sub_item['name']}")
            except Exception as e:
                print(f"Error accessing folder {folder_name}: {e}")
    return files_paths