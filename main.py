
# from CheckWidget import Website
import pandas as pd
from dataclasses import asdict
import os 
import datetime as dt
import time
from WidgetChecker import Website


if __name__ == '__main__':
    while True:
        dir = input("Inserisci il percorso della cartella che contiene gli URL: ")
        input_file = input("Inserisci il nome del file che contiene gli URL (includi .txt): ")
        out_dir = input("Inserisci il percorso della cartella di destinazione: ")
        start = time.time()
        urls = [i.replace('\n','').strip() for i in open(f"{dir}/{input_file}", "r").readlines() if i != '']
        urls = [i.strip() for i in urls if i != '']
        print(urls)
        df = pd.DataFrame()
        for url in urls:
            w = Website(url)
            print(w.outcome)
            if w.location is not None:
                data = asdict(w.outcome) | w.location
            else:
                data = asdict(w.outcome)
            df = df.append(data, ignore_index = True)
            # df = df.append(asdict(w.outcome), ignore_index = True)
        time_now = dt.datetime.strftime(dt.datetime.now(), '%d-%m-%Y_%H_%M_%S')
        df.to_excel(f'output/{input_file.replace(".txt", "")}_output_{time_now}.xlsx', index = False)
        end = time.time()
        total_time = end - start
        with open(f'output/TIME_{input_file.replace(".txt", "")}_output_{time_now}.txt','w') as time_file:
            time_file.write(f"Start: {str(start)}\n")
            time_file.write(f"End: {str(end)}\n")
            time_file.write(f"Total Time: {str(total_time)}\n")