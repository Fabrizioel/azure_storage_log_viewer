from azure.storage.fileshare import ShareFileClient

def download_file(account_name, account_key, share_name, file_path):
    file_client = ShareFileClient(
        account_url=f"https://{account_name}.file.core.windows.net/",
        share_name=share_name,
        file_path=file_path,
        credential=account_key
    )

    download = file_client.download_file()
    return download.readall().decode('utf-8')