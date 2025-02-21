import pandas as pd 
import numpy as np
import os, sys

def isvalid(df):
    cond1 = df.query("videos == '6.mp4'")["sanityscore"].item() != 2
    # cond6 = df.query("videos == '5.mp4'")["scores"].item() <= df.query("videos == '4.mp4'")["scores"].item()
    cond2 = df.query("videos == '1.mp4'")["scores"].item() == df["scores"].max()
    cond3 = df.query("videos == '2.mp4'")["scores"].item() == df["scores"].min()
    cond4 = df.query("videos == '1.mp4'")["sanityscore"].item() == 2
    cond5 = df.query("videos == '2.mp4'")["sanityscore"].item() == 5
    #cond6 = (df.query("videos == '3.mp4'")["sanityscore"].item() == 5) or (df.query("videos == '3.mp4'")["sanityscore"].item() == 4) 
    return cond1 and cond2 and cond3 and cond4 and cond5 
    #return True

def process_one_file(filename):
    with open(filename, "r") as fin:
        lines = [l.strip("\n") for l in fin]
    scores = [int(v) for v in lines[0].split(',')]
    if (len(scores) != 6):
        return None
    #videos = [f"{v}.mp4" for v in lines[1].split(",")]
    videos = [f"{v}.mp4" for v in range(1, 10)]
    videos = videos[:len(scores)]
    usertimes = [int(v) for v in lines[2].split(',')]
    systemtimes = [int(v) for v in lines[3].split(',')]
    userid = lines[4]
    sanityscore = [int(v) for v in lines[9].split(',')]
    df = pd.DataFrame()
    df["scores"] = scores
    df["videos"] = videos
    df["usertimes"] = usertimes
    df["systemtimes"] = systemtimes
    df["userid"] = userid
    df["sanityscore"] = sanityscore
    if isvalid(df):
        return df
    else:
        return None


filenames = os.listdir(".")
#print(filenames)

dfs = []
for file in filenames:
    if "txt" in file:
        try:
            df = process_one_file(file)
            if df is None:
                print(file, "is invalid!")
            else:
                dfs.append(df)
        except:
            pass

print("Got", len(dfs), "valid dataframes")
final_df = pd.concat(dfs)
final_df.to_csv("all.csv", index=None)

final_df[["videos", "scores"]].groupby("videos").mean().reset_index(drop=True).to_csv("mean.csv", index=None)
final_df[["videos", "scores"]].groupby("videos").std().reset_index(drop=True).to_csv("std.csv", index=None)

