
# from CheckWidget import Website
import pandas as pd
from dataclasses import asdict
import os 
import datetime as dt
import time
from WidgetChecker import Website
import sys
import warnings

sys.setrecursionlimit(100_000)


def add_protocol(s:str)->str:
    try:
        if s.startswith("https://") == False and s.startswith("http://") == False:
            return f"https://{s}"
        else:
            return s
    except Exception as e:
        print(e)
        return s

# if __name__ == '__main__':
#     while True:
#         dir = input("Inserisci il percorso della cartella che contiene gli URL: ")
#         input_file = input("Inserisci il nome del file che contiene gli URL (includi .txt): ")
#         out_dir = input("Inserisci il percorso della cartella di destinazione: ")
#         start = time.time()
#         urls = [i.replace('\n','').strip() for i in open(f"{dir}/{input_file}", "r").readlines() if i != '']
#         urls = [i.strip() for i in urls if i != '']
#         urls = [i.strip() for i in urls if i != None]
#         urls = [i.strip() for i in urls if i != 'nan']
#         urls = [add_protocol(i) for i in urls]

#         print(urls)
#         df = pd.DataFrame()
#         for url in urls:
#             print(url)
#             w = Website(url, True)
#             warnings.resetwarnings()
#             print(w.outcome)
#             if w.location is not None:
#                 data = asdict(w.outcome) | w.location
#             else:
#                 data = asdict(w.outcome)
#             df = df.append(data, ignore_index = True)
#             # df = df.append(asdict(w.outcome), ignore_index = True)
#         time_now = dt.datetime.strftime(dt.datetime.now(), '%d-%m-%Y_%H_%M_%S')
#         df.to_excel(f'output/{input_file.replace(".txt", "")}_output_{time_now}.xlsx', index = False)
#         end = time.time()
#         total_time = end - start
#         with open(f'output/TIME_{input_file.replace(".txt", "")}_output_{time_now}.txt','w') as time_file:
#             time_file.write(f"Start: {str(start)}\n")
#             time_file.write(f"End: {str(end)}\n")
#             time_file.write(f"Total Time: {str(total_time)}\n")

if __name__ == '__main__':
    while True:
        dir = input("Inserisci il percorso della cartella che contiene gli URL: ")
        input_file = input("Inserisci il nome del file che contiene gli URL (includi .txt): ")
        out_dir = input("Inserisci il percorso della cartella di destinazione: ")
        start = time.time()
        urls = [i.replace('\n','').strip() for i in open(f"{dir}/{input_file}", "r").readlines() if i != '']
        urls = [i.strip() for i in urls if i != '']
        urls = [i.strip() for i in urls if i != None]
        urls = [i.strip() for i in urls if i != 'nan']
        urls = [add_protocol(i) for i in urls]
        idx = range(0, len(urls),10)
        idx = [i for i in idx]
        if len(urls)%10 != 0:
            idx[len(idx)-1] = idx[len(idx)-1]+len(urls)%10 
        print(urls)
        for i in range(len(idx)-1):
            df = pd.DataFrame()

            for url in urls[idx[i]:idx[i+1]]:
                print(url)
                w = Website(url, True)
                warnings.resetwarnings()
                print(w.outcome)
                if w.location is not None:
                    data = asdict(w.outcome) | w.location
                else:
                    data = asdict(w.outcome)
                df = df.append(data, ignore_index = True)
            
            # df = df.append(asdict(w.outcome), ignore_index = True)
            time_now = dt.datetime.strftime(dt.datetime.now(), '%d-%m-%Y_%H_%M_%S')
            print(f"Saving to excel urls from {idx[i]} to {idx[i+1]}")
            # df.to_excel(f'output/march/{idx[i]}_{idx[i+1]}_{input_file.replace(".txt", "")}_output_{time_now}.xlsx', index = False)
            with pd.ExcelWriter(f'output/march/{idx[i]}_{idx[i+1]}_{input_file.replace(".txt", "")}_output_{time_now}.xlsx',engine = "openpyxl") as df_file:
                df.to_excel(df_file, index = False)
            end = time.time()
            total_time = end - start
            with open(f'output/march/{idx[i]}_{idx[i+1]}_TIME_{input_file.replace(".txt", "")}_output_{time_now}.txt','w') as time_file:
                time_file.write(f"Start: {str(start)}\n")
                time_file.write(f"End: {str(end)}\n")
                time_file.write(f"Total Time: {str(total_time)}\n")