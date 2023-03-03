
import os
import pandas as pd
files = [i for i in os.listdir() if '.xlsx' in i and '~' not in i]
len(files)
print(f"Nunber of files: {len(files)}")

col = ['url'	,'position'	,'page_found'	,'outcome'	,'allows_booking'	,'height'	,'width'	,'x'	,'y'	,'text']

df = pd.DataFrame()
for f in files:
    # print(f"Parsing file: {f}")
    try:
        d = pd.read_excel(f)
        d = d[col]
        df = pd.concat([df,d], ignore_index=True)
    except Exception as e:
        print(e)
        pass


summary = df[['url', 'outcome']].groupby('outcome', group_keys=True).count()
summary['%'] = summary['url'].apply(lambda x: f"{x/summary['url'].sum()*1e2 :2f}%")
print(f"# of Website checked: {summary['url'].sum()}")
print(summary)