import inspect
import sys
import json
# import pandas as pd

class CocoPart:
    Nose = 0
    Neck = 1
    RShoulder = 2
    RElbow = 3
    RWrist = 4
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8
    RKnee = 9
    RAnkle = 10
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14
    LEye = 15
    REar = 16
    LEar = 17
    Background = 18


def json_to_row(data, filter_list="all"):
    columns = []
    for i in filter_list:
        columns.append('_'.join([i, 'score']))
        columns.append('_'.join([i, 'x']))
        columns.append('_'.join([i, 'y']))
    print(','.join(['file', 'index', 'yaw', 'pitch', 'roll'] + columns))
    for f, indexs in data.items():
        for index, value in indexs.items():
            output = str(f)
            if not (value['fsa'] or value['tf_pose']):
                continue
            output = ','.join([
                output, 
                str(index),
                # str(value['frame']), 
                str(value['fsa']['yaw']), 
                str(value['fsa']['pitch']), 
                str(value['fsa']['roll'])
            ])
            for part in filter_list:
                if part in value['tf_pose'].keys():
                    output = ','.join([
                        output,
                        value['tf_pose'][part]['score'],
                        value['tf_pose'][part]['x'],
                        value['tf_pose'][part]['y'],
                    ])
                else:
                    output = ','.join([output,'','',''])
            print(output)



if __name__ == "__main__":
    attributes = inspect.getmembers(CocoPart, lambda a:not(inspect.isroutine(a)))
    cocopart = [a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
    data = json.load(sys.stdin)
    json_to_row(data, cocopart)