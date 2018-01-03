# coding=utf-8

import generate_news_level_dataset
import generate_user_level_dataset
import generate_task_level_dataset
import generate_pairpref_dataset
import utils

logs = utils.loadlogs()
outaddr = "0103"

generate_news_level_dataset.generate(logs, outaddr)
generate_user_level_dataset.generate(logs, outaddr)
generate_task_level_dataset.generate(logs, outaddr)
generate_pairpref_dataset.generate(outaddr)


