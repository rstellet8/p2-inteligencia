import pandas as pd


URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FEDFUNDS&scale=left&cosd=1954-07-01&coed=2021-06-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-07-04&revision_date=2021-07-04&nd=1954-07-01"


def getIntRate(url=URL):
    df = pd.read_csv(URL, names=["date", "BasicIntRate"], skiprows=1)
    df["date"] = pd.to_datetime(df["date"])
    return df.query("date >= '2000-01-01'")

if __name__ == "__main__":
    print(getIntRate())