import utils
from models import News, Task

def generate(logs, outaddr):
    ds_news = utils.DataSet()

    for ulog in logs:
        userid = ulog['studentID']
        topic_pref = ulog['pre_questions']

        for task_pos, task in enumerate(ulog['tasks'][1:]):
            task = Task(task)

            for newsid in task.imp_list:
                news = task.news_dict[newsid]

                ds_news.add(userid, "userid")
                ds_news.add(newsid, "newsid")
                ds_news.add(news.topic, "topic")
                ds_news.add(int(topic_pref[news.topic][0]), "topic_pref")
                ds_news.add(task.task_id, "taskid")
                ds_news.add(task_pos, "task_pos")

                ds_news.add(task.condition, "condition")
                ds_news.add(news.equality, 'equality')

                ds_news.add(news.imp_position, 'imp_position')
                ds_news.add(news.ifview, 'ifview')
                ds_news.add(news.ifclick, 'ifclick')
                ds_news.add(news.viewport_time, 'viewport_time')

                ds_news.add(news.dwell_time, 'dwell_time')
                ds_news.add(news.pre_pref, 'pre_pref')
                ds_news.add(news.read_pref, 'read_pref')
                ds_news.add(news.whyclick, 'whyclick')
                ds_news.add(news.uquality, 'uquality')
                ds_news.add(news.utitle, 'utitle')

                ds_news.add(news.post_pref, 'post_pref')

    df_news = ds_news.to_pandas()
    print df_news.info()
    df_news.to_pickle("../Dataset/{}/df_news.pkl".format(outaddr))

if __name__ == "__main__":
    logs = utils.loadlogs()
    outaddr = "0103"
    generate(logs, outaddr)