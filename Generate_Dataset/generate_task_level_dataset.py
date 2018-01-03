import numpy as np
import utils
from models import News, Task

def generate(logs, outaddr):
    ds_task = utils.DataSet()
    for ulog in logs:
        userid = ulog['studentID']

        tasks = []
        satlist = []
        for task_pos, task in enumerate(ulog['tasks'][1:]):
            task = Task(task)
            satlist.append(task.satisfaction)
            tasks.append(task)

        mean_sat = np.mean(satlist)
        var_sat = np.var(satlist)

        for task_pos, task in enumerate(tasks):
            task.sat_zscore = (task.sat_zscore - float(mean_sat)) / var_sat

            post_prefs, clk_post_prefs, pre_prefs, read_prefs = [], [], [], []
            for newsid in task.imp_list:
                news = task.news_dict[newsid]
                if news.ifview:
                    post_prefs.append(news.post_pref)

                if news.ifclick:
                    clk_post_prefs.append(news.post_pref)
                    pre_prefs.append(news.pre_pref)
                    read_prefs.append(news.read_pref)
                list_topic = news.topic

            ds_task.add(userid, 'userid')
            ds_task.add(task.task_id, 'task_id')
            if task.task_id in range(1, 6) + range(10, 12):
                ds_task.add(list_topic, "topic")
            else:
                ds_task.add("mixed", 'topic')

            ds_task.add(task_pos, "task_pos")
            ds_task.add(task.condition, 'condition')
            ds_task.add(task.satisfaction, 'satisfaction')
            ds_task.add(task.sat_zscore, "sat_zscore")
            ds_task.add(task.quality, 'quality')

            ds_task.add(int(task.condition[1]), "num_low_news_imp")
            ds_task.add(sum([task.news_dict[tnews].equality for tnews in task.click_list]) if len(pre_prefs) > 0 else 0,
                        "num_high_news_clk")
            ds_task.add(
                sum([task.news_dict[tnews].equality == 0 for tnews in task.click_list]) if len(pre_prefs) > 0 else 0,
                "num_low_news_clk")

            ds_task.add(len(post_prefs), 'view_cnt')
            ds_task.add(len(pre_prefs), 'click_cnt')
            ds_task.add(len(pre_prefs) / float(len(post_prefs)), "ctr")
            ds_task.add(task.news_dict[task.click_list[0]].imp_position if len(pre_prefs) > 0 else None, "first_click_pos")
            ds_task.add([task.news_dict[tnews].imp_position for tnews in task.click_list] if len(pre_prefs) > 0 else None,
                        "click_pos_list")
            ds_task.add([task.news_dict[tnews].dwell_time for tnews in task.click_list] if len(pre_prefs) > 0 else None,
                        "clk_dwells")
            ds_task.add(task.browse_time, "browse time")

            ds_task.add(post_prefs, "post_prefs")
            ds_task.add(pre_prefs, "pre_prefs")
            ds_task.add(read_prefs, "read_prefs")

            #         ds_task.add(np.mean(normalize(post_prefs, userid, "post_prefs")) if post_prefs else None, 'mean_post_prefs')
            ds_task.add(np.mean(post_prefs) if post_prefs else None, 'mean_post_prefs')
            ds_task.add(np.sum(post_prefs) if post_prefs else None, 'sum_post_prefs')
            ds_task.add(np.max(post_prefs) if post_prefs else None, 'max_post_prefs')
            ds_task.add(np.min(post_prefs) if post_prefs else None, 'min_post_prefs')

            ds_task.add(np.mean(clk_post_prefs) if clk_post_prefs else None, 'mean_clk_post_prefs')
            ds_task.add(np.sum(clk_post_prefs) if clk_post_prefs else None, 'sum_clk_post_prefs')
            ds_task.add(np.max(clk_post_prefs) if clk_post_prefs else None, 'max_clk_post_prefs')
            ds_task.add(np.min(clk_post_prefs) if clk_post_prefs else None, 'min_clk_post_prefs')

            #         ds_task.add(np.mean(normalize(pre_prefs, userid, "pre_prefs")) if pre_prefs else None, 'mean_pre_prefs')
            ds_task.add(np.mean(pre_prefs) if pre_prefs else None, 'mean_pre_prefs')
            ds_task.add(np.sum(pre_prefs) if pre_prefs else None, 'sum_pre_prefs')
            ds_task.add(np.max(pre_prefs) if pre_prefs else None, 'max_pre_prefs')
            ds_task.add(np.min(pre_prefs) if pre_prefs else None, 'min_pre_prefs')

            #         ds_task.add(np.mean(normalize(read_prefs, userid, "read_prefs")) if read_prefs else None, 'mean_read_prefs')
            ds_task.add(np.mean(read_prefs) if read_prefs else None, 'mean_read_prefs')
            ds_task.add(np.sum(read_prefs) if read_prefs else None, 'sum_read_prefs')
            ds_task.add(np.max(read_prefs) if read_prefs else None, 'max_read_prefs')
            ds_task.add(np.min(read_prefs) if read_prefs else None, 'min_read_prefs')

            ds_task.add(pre_prefs[-1] if pre_prefs else None, "last_pre_prefs")
            ds_task.add(read_prefs[-1] if read_prefs else None, "last_read_prefs")
            ds_task.add(post_prefs[-1] if post_prefs else None, "last_post_prefs")

    df_task = ds_task.to_pandas()
    df_task.to_pickle("../Dataset/{}/df_task.pkl".format(outaddr))
    print df_task.info()

if __name__ == "__main__":
    logs = utils.loadlogs()
    outaddr = "0103"
    generate(logs, outaddr)
