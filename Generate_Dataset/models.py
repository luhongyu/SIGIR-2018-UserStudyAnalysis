# coding=utf-8
import pandas as pd
import numpy as np
import utils
import json
from collections import Counter, defaultdict


class News:
    viewport_time = 0
    anno_pos, post_pref = None, None
    pre_pref, read_pref, post_pref = None, None, None
    whyclick, uquality, utitle, dwell_time = None, None, None, None

    def __init__(self, newsid, position, viewport_time, read_logs=None, read_annotation=None, post_annotation=None):
        """
            newsid, position
            ifviewed, viewport_time
        """
        self.newsid = newsid
        self.imp_position = position
        self.equality = utils.get_news_quality(newsid)
        self.topic = utils.get_news_topic(newsid)

        self.ifview = False
        self.ifclick = False

        # --------------- view information -------------- #
        if post_annotation:
            self.ifview = True
            self.viewport_time = viewport_time
            self.anno_pos, self.post_pref = post_annotation[0], int(post_annotation[1])

        # --------------- click information -------------- #
        if read_logs and "4" not in read_annotation['why_click'][0]:
            self.ifclick = True
            self.read_logs = read_logs
            self.pre_pref = int(read_annotation['pre-pref'][0])
            self.read_pref = int(read_annotation['read-item-pref'][0])
            self.whyclick = read_annotation['why_click'][0]
            self.uquality = int(read_annotation['quality'][0])
            self.utitle = int(read_annotation['title'][0])
            self.dwell_time = self.__cal_dwell_time()

    def __cal_dwell_time(self):
        if len(self.read_logs) > 1:
            begin_event = json.loads(self.read_logs[0])
            if type(begin_event) == list:
                begin_time = begin_event[0]['time']
            else:
                begin_time = begin_event['time']

            end_time = 0
            for te in self.read_logs:
                if "PAGE_END" in te:  # 只到第一次PAGE_END （可能多次点击查看同一条新闻）
                    break
                tevent = json.loads(te)
                if type(tevent) != list:
                    end_time = max(end_time, tevent['time'])

            if end_time != 0:
                browse_time = (int(end_time) - int(begin_time)) / 1000
                return browse_time
        return np.nan


class Task:
    def __init__(self, tasklog):
        self.task_id = tasklog['task_id']
        self.condition = tasklog['condition']
        self.tasklog = tasklog
        self.imp_list = tasklog['news_list']

        self.satisfaction = int(tasklog['list_annotation']['satisfaction'][0])
        self.sat_zscore = self.satisfaction
        self.quality = int(tasklog['list_annotation']['quality'][0])

        if "pair-pref" in tasklog['list_annotation']:
            self.pair_pref = int(tasklog['list_annotation']['pair-pref'][0])

        self.read_annotations = tasklog['item_prefs']
        self.post_annotations = tasklog['item_annotation']

        self.behavior_logs = dict([(tk[25:], tv) for tk, tv in tasklog['behavior_logs'].items()])
        self.browse_log = self.behavior_logs['/newslist/']

        self.news_dict = {}
        self.__init_news()

        self.click_list = [utils.get_newsid(tanno[0]) for tanno in self.read_annotations]
        self.browse_time = self.__get_browse_time()

    def __init_news(self):
        vt_list = self.__get_viewport_time()
        for tpos, (newsid, vt) in enumerate(zip(self.tasklog['news_list'], vt_list)):
            # newsid
            turl = '/news/{}?state=content'.format(newsid)

            read_logs = self.behavior_logs[turl] if turl in self.behavior_logs else None

            read_annotation = None
            for tanno in self.read_annotations:
                if utils.get_newsid(tanno[0]) == newsid:
                    read_annotation = tanno[1]
                    break

            post_annotation = None
            for ti, tanno in enumerate(self.post_annotations):
                if tanno[0] == newsid:
                    post_annotation = (ti, tanno[1])
                    break

            tnews = News(newsid, tpos + 1, vt, read_logs, read_annotation, post_annotation)
            self.news_dict[newsid] = tnews

    def __get_browse_time(self):

        begin_event = json.loads(self.browse_log[0])
        end_event = json.loads(self.browse_log[-1])
        if type(begin_event) == list:
            begin_time = begin_event[0]['time']
        else:
            begin_time = begin_event['time']

        if type(end_event) == list:
            end_time = end_event[-1]['time']
        else:
            end_time = end_event['time']
        browse_time = int(end_time) - int(begin_time)
        return browse_time

    def __get_viewport_time(self):
        item_heights = self.tasklog['item_heights']
        item_positions = self.tasklog['item_positions']
        screen_height = self.tasklog['screen_height']
        offset_top = item_positions[0] - item_heights[0]
        item_field = [(tpos - theight, tpos) for tpos, theight in zip(item_positions, item_heights)]

        vt_list = np.zeros(shape=(len(item_positions),))

        last_time = json.loads(self.browse_log[0])['time']
        y = 0
        for te in self.browse_log:
            tlog = json.loads(te)
            if "PAGE_BEGIN" in te and type(tlog) != list:
                last_time = tlog['time']
                continue

            if "SCROLL" in te and type(tlog) != list:
                time_delta = (tlog['time'] - last_time)
                last_time = tlog['time']
                view_field = (y + offset_top, y + screen_height)
                y = tlog['y']

                for ti, item in enumerate(item_field):
                    if (view_field[0] <= item[0] <= view_field[1]) and (view_field[0] <= item[1] <= view_field[1]):
                        vt_list[ti] += time_delta
        return vt_list

if __name__ == "__main__":
    for tlog in utils.loadlogs():
        userid = tlog['studentID']
        print "Loaded Tasklog: ", userid,
        for tasklog in tlog['tasks'][1:]:
            task = Task(tasklog)
            print task.task_id
