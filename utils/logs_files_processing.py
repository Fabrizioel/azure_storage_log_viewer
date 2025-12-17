from datetime import datetime, date
import pandas as pd

from helpers.download_from_file_path import download_file
from helpers.obtain_files_paths import get_files_paths
from validations.ip_validations import is_valid_ip
from validations.time_validations import is_valid_time

output_file = "output/ScanLogs_Output.xlsx"
rows = []

def readLogs(logs, start_date, end_date, account_name, account_key, share_name) -> int:
    rows.clear()
    for log in logs:
        try:
            file_content = download_file(account_name, account_key, share_name, log)

            for line in file_content.splitlines():
                col = line.strip().split(",")
                if (len(col) == 5 and col[0] == "SUCESS" and
                    len(col[1]) == 8 and col[1].isdigit() and is_valid_time(col[2]) and is_valid_ip(col[3]) and col[4].isdigit() and start_date <= datetime.strptime(col[1][0:2] + col[1][2:4] + col[1][4:8], "%d%m%Y").date() <= end_date):
                    rows.append([col[0], col[1], col[2], col[3], col[4], log])
        except Exception as e:
            print(f"Error reading {log}: {e}")
    df = pd.DataFrame(rows, columns=["Status", "Date", "Time", "IP", "ComplaintId", "LogFile"])
    # df.to_excel(output_file, sheet_name="Data", index=False)

    # result = []
    # for filename, group in df.groupby("LogFile"):
        # unique_ids = group["ComplaintId"].nunique() 
        # total_occurrences = group["ComplaintId"].count()
        # result.append([filename, unique_ids, total_occurrences])

    # summary_df = pd.DataFrame(result, columns=["Log Filename", "# of Complaints", "Sum of Occurrences"])
    
    # with pd.ExcelWriter(output_file, mode='a', engine='openpyxl') as writer:
    #     summary_df.to_excel(writer, sheet_name="Summary", index=False)
    
    unique_ids = df["ComplaintId"].nunique()

    return unique_ids