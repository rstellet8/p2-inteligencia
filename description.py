import pandas as pd


URL = "https://resources.lendingclub.com/LCDataDictionary.xlsx"

def description(URL=URL):
    return pd.read_excel(
        URL, 
        sheet_name="browseNotes", 
        engine="openpyxl", 
        usecols=[0, 1], 
        skipfooter=2
    )

if __name__ == "__main__":
    description()
