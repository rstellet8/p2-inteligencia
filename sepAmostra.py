import pandas as pd
import os


def sepAmostra(pathRaw, pathToSave, randomState=None, nSample=10000):
    os.makedirs(getPath(pathToSave), exist_ok=True)

    df = pd.read_csv(pathRaw)
    df = df.sample(n=nSample, random_state=randomState)
    df.to_csv(pathToSave, index=False)
    del df


def getPath(path):
    pth = path.split("/")
    pth = pth[:-1]
    pth = "/".join(pth)
    return pth


if __name__ == "__main__":
    sepAmostra(
        pathRaw="data/raw/accepted_2007_to_2018Q4.csv",
        pathToSave="data/sample/sampleAccepted.csv",
        nSample=10000,
        randomState=None
    )

    sepAmostra(
        pathRaw="data/raw/rejected_2007_to_2018Q4.csv",
        pathToSave="data/sample/sampleRejected.csv",
        nSample=10000,
        randomState=None
    )
