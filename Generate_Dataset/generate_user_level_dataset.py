# coding=utf-8
import numpy as np
import utils
from models import News, Task

def generate(logs, outaddr):
    ds_user = utils.DataSet()

    for ulog in logs:
        userid = ulog['studentID']
        age = int(ulog['pre_questions']['pq1'][0])
        news_exp = int(ulog['pre_questions']['pq2'][0])
        newsrec_exp = int(ulog['pre_questions']['pq3'][0])

        pre_topic_pref = [(tk, int(ulog['pre_questions'][tk][0])) for tk in [u'社会', u'娱乐', u'科技', u'体育', u'历史']]
        post_topic_pref = [(tk, int(ulog['post_questions'][ti][0])) for ti, tk in zip(['topic-1', 'topic-2', 'topic-3', 'topic-4', 'topic-5'],
                                                                          [u'社会', u'娱乐', u'科技', u'体育', u'历史'])]

        # --- for normalization --- #
        pre_prefs, read_prefs, post_prefs = [], [], []
        satlist = []

        task_list = []
        for task_pos, task in enumerate(ulog['tasks'][1:]):
            task = Task(task)
            satlist.append(task.satisfaction)
            task_list.append((task.task_id, task.condition, task.satisfaction, task.quality, task.pair_pref if task_pos > 0 else None))
            for newsid in task.imp_list:
                news = task.news_dict[newsid]
                if news.ifview:
                    post_prefs.append(news.post_pref)

                if news.ifclick:
                    pre_prefs.append(news.pre_pref)
                    read_prefs.append(news.read_pref)

        ds_user.add(userid, "userid")
        ds_user.add(age, "age")
        ds_user.add(news_exp, "exp_news")
        ds_user.add(newsrec_exp, "exp_newsrec")
        ds_user.add(pre_topic_pref, "pre_topic_prefs")
        ds_user.add(post_topic_pref, "post_topic_prefs")

        ds_user.add(task_list, "tasks")
        ds_user.add(satlist, "satisfactions")

        ds_user.add(np.mean(post_prefs), "post_prefs_mean")
        ds_user.add(np.var(post_prefs), "post_prefs_var")

        ds_user.add(np.mean(pre_prefs), "pre_prefs_mean")
        ds_user.add(np.var(pre_prefs), "pre_prefs_var")

        ds_user.add(np.mean(read_prefs), "read_prefs_mean")
        ds_user.add(np.var(read_prefs), "read_prefs_var")

    df_user = ds_user.to_pandas()
    df_user.to_pickle("../Dataset/{}/df_user.pkl".format(outaddr))
    print df_user.info()

if __name__ == "__main__":
    logs = utils.loadlogs()
    outaddr = "0103"
    generage(logs, outaddr)