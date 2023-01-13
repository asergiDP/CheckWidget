



import pandas as pd

df = pd.read_excel('input/hubspot-crm-exports-check-widget-inf-2023-01-13.xlsx')

df.columns

df.loc[pd.isna(df["Doctor/Facility - Doctor's website URL"]) == True, "Doctor/Facility - Doctor's website URL"] =df.loc[pd.isna(df["Doctor/Facility - Doctor's website URL"]) == True]['Website URL']

df.to_excel(f"input/hs_13_01_2023.xlsx", index= False )

df["Doctor/Facility - Doctor's website URL"].fillna("")
urls = list(df["Doctor/Facility - Doctor's website URL"])
urls = [url for url in urls if url != None]

with open("input/hs_urls_13_01_2023.txt","w") as file:
    for url in urls:
        file.write(f"{url}\n")