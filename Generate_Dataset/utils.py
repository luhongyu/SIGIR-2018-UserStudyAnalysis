# coding=utf-8
import json
import pandas as pd
import re
import configs

# loadlogs
# get_news_quality
# get_news_topic
# get_newsid
# utils.DataSet

def loadlogs():
    reload(configs)
    logfiles = configs.logfiles
    anslist = []
    for tf in logfiles:
        anslist.append(json.load(open(tf)))
    return anslist

df_news_info = pd.read_excel("exp_list_1221.xlsx")
newsinfo = {}
for ti, trow in df_news_info.iterrows():
    newsinfo[str(trow['newsid'])] = {
        "quality": trow['control_quality'],
        "title": trow['title'],
        "topic": trow['topic']
    }

def get_news_quality(newsid):
    return int(newsinfo[str(newsid)]['quality'])

def get_news_topic(newsid):
    return newsinfo[str(newsid)]['topic']

def get_newsid(turl):
    tl = re.findall("news/(\d+)", turl)
    if tl:
        return tl[0]


class DataSet:
    """
    .add(data, "colname")
    .to_pandas
    """
    def __init__(self):
        self.column_datas = {}
        self.column_names = []

    def add(self, data, colname):
        if colname not in self.column_datas:
            self.column_datas[colname] = []
            self.column_names.append(colname)

        self.column_datas[colname].append(data)

    def to_pandas(self):
        return pd.DataFrame(self.column_datas)[self.column_names]

if __name__ == "__main__":
    log = loadlogs()
    print len(log)