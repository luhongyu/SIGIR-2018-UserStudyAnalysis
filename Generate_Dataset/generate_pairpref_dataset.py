import pandas as pd
import json

def generate(outaddr):
    df_user = pd.read_pickle("../Dataset/{}/df_user.pkl".format(outaddr))

    recs = []
    for userid, tasks in zip(df_user['userid'], df_user['tasks']):
        for ti in range(1, len(tasks)):
            if tasks[ti-1][3] < tasks[ti][3]:
                recs.append((userid, tasks[ti-1][0], tasks[ti][0]))
            elif tasks[ti-1][3] > tasks[ti][3]:
                recs.append((userid, tasks[ti][0], tasks[ti-1][0]))
            else:
                if tasks[ti][4] == 1:
                    recs.append((userid, tasks[ti][0], tasks[ti-1][0]))
                elif tasks[ti][4] == 2:
                    recs.append((userid, tasks[ti-1][0], tasks[ti][0]))
                else:
                    print "error"
    json.dump(recs, open("../Dataset/{}/task_pairpref_satfirst.json".format(outaddr), 'w'), indent=1)

    recs = []
    for userid, tasks in zip(df_user['userid'], df_user['tasks']):
        for ti in range(1, len(tasks)):

            if tasks[ti][4] == 1:
                recs.append((userid, tasks[ti][0], tasks[ti - 1][0]))
            elif tasks[ti][4] == 2:
                recs.append((userid, tasks[ti - 1][0], tasks[ti][0]))
            else:
                print "error"

    json.dump(recs, open("../Dataset/{}/task_pairpref_pairfirst.json".format(outaddr), 'w'), indent=1)

if __name__ == "__main__":
    generate("0103")
