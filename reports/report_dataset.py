import csv, os
from .report_details import *  # noqa
from forms.modelutils import (TOPICS, FUNCTION, YESNO, )

def get_gender(gender_id):
    if gender_id == 1:
        return "Female"
    elif gender_id == 2:
        return "Male"
    elif gender_id == 3:
        return "Transgender"
    else:
        return "Don't Know"

def ws_05_csv(writer, counts_list, row, **kwargs):
    for media_type in row:
        for topic in row[media_type]:
            topic_name = [x for x in MAJOR_TOPICS if x[0] == topic[1]][0][1]
            gender = get_gender(topic[0])

            writer.writerow({'Topic': topic_name, 'Gender': gender, 'Medium': media_type, 'Count': row[media_type][topic]})

def ws_06_csv(writer, counts_list, row, **kwargs):
    for topic, gender in counts_list[row]:
        count = counts_list[row][(gender, topic)]
        gender = get_gender(gender)
        topic_name = [x for x in MAJOR_TOPICS if x[0] == topic][0][1]
        writer.writerow({'Topic': topic_name, 'Gender': gender, 'Region': row, 'Count': count})

def ws_09_csv(writer, counts_list, row, **kwargs):
    topic = [y for x in TOPICS for y in x[1] if y[0]==row[1]][0][1]
    gender = get_gender(row[0])

    writer.writerow({'Topic': topic, 'Gender': gender, 'Count': counts_list[row]})

def ws_15_csv(writer, counts_list, row, **kwargs):
    function = [func[1] for func in FUNCTION if func[0] == row[1]]
    if function:
        function = function[0][4:] # [4:] is used to remove the (number) part
        gender = get_gender(row[0])

        writer.writerow({'Function': function, 'Gender': gender, 'Count': counts_list[row]})

def ws_28b_csv(writer, counts_list, row, **kwargs):
    medium = kwargs['medium']
    regions = kwargs['regions']
    for reporter in counts_list[row]:
        gender = get_gender(reporter[0])
        if type(regions) == dict:
            region = regions[reporter[1]]
        else:
            region = regions[reporter[1]][1]
        writer.writerow({'Region': region, 'Medium': medium, 'Gender': gender, 'Count': counts_list[row][reporter]})

def ws_28c_csv(writer, counts_list, row, **kwargs):
    medium = kwargs['medium']
    regions = kwargs['regions']
    
    for presenter in counts_list[row]:
        gender = get_gender(presenter[0])
        if type(regions) == dict:
            region = regions[presenter[1]]
        else:
            region = regions[presenter[1]][1]
        writer.writerow({'Region': region, 'Medium': medium, 'Gender': gender, 'Count': counts_list[row][presenter]})

def ws_30_csv(writer, counts_list, row, **kwargs):
    for reporter in counts_list[row]:
        gender = get_gender(reporter[0])
        topic = [t for t in MAJOR_TOPICS if t[0] == reporter[1]][0][1]
        writer.writerow({'Region': row, 'Topic': topic, 'Gender': gender, 'Count': counts_list[row][reporter]})

def ws_38_csv(writer, counts_list, row, **kwargs):
    topic = [t for t in MAJOR_TOPICS if t[0] == row[1]][0][1]
    writer.writerow({'Topic': topic, 'Answer': row[0], 'Count': counts_list[row]})

def ws_41_csv(writer, counts_list, row, **kwargs):
    all_topics = [y for x in TOPICS for y in x[1]]
    topic = [x[1] for x in all_topics if x[0] == row[1]][0]
    writer.writerow({'Topic': topic[4:].strip(), 'Answer': row[0], 'Count': counts_list[row]})

def ws_47_csv(writer, counts_list, row, **kwargs):
    topic = [t for t in MAJOR_TOPICS if t[0] == row[1]][0][1]
    answer = 'Agree' if row[0] == 1 else 'Disagree'
    writer.writerow({'Topic': topic, 'Answer': answer, 'Count': counts_list[row]})

def ws_48_csv(writer, counts_list, row, **kwargs):
    topic = [t for t in MAJOR_TOPICS if t[0] == row[1]][0][1]
    answer = 'Agree' if row[0] == 1 else 'Disagree'
    gender = get_gender(kwargs['gender'])
    writer.writerow({'Topic': topic, 'Gender': gender, 'Answer': answer, 'Count': counts_list[row]})

def ws_83_csv(writer, counts_list, row, **kwargs):
    regions = kwargs['regions']
    for gender, region in counts_list[row]:
        count = counts_list[row][(gender, region)]
        region = [x[1] for x in regions if x[0] == region][0]
        gender = get_gender(gender)
        writer.writerow({'Topic': row, 'Region': region, 'Gender': gender, 'Count': count})

def ws_85_csv(writer, counts_list, row, **kwargs):
    regions = kwargs['regions']
    function, region = row
    region = [x[1] for x in regions if x[0] == region][0]
    function = [func[1] for func in FUNCTION if func[0] == function]
    if function:
        function = function[0][4:] # [4:] is used to remove the (number) part
        writer.writerow({'Region': region, 'Function': function, 'Count': counts_list[row]})

def ws_92_csv(writer, counts_list, row, **kwargs):
    topic, agree_disagree = row
    count = counts_list[row]
    region = kwargs['region']
    topic = [t for t in MAJOR_TOPICS if t[0] == topic][0][1]
    agree_disagree = 'Agree' if agree_disagree == 1 else 'Disagree'
    writer.writerow({'Region': region, 'Topic': topic, 'Answer': agree_disagree, 'Count': count})

def ws_93_csv(writer, counts_list, row, **kwargs):
    topic, yes_no = row
    count = counts_list[row]
    region = kwargs['region']
    topic = [t for t in MAJOR_TOPICS if t[0] == topic][0][1]
    yes_no = 'Yes' if yes_no == 'Y' else 'No'
    writer.writerow({'Region': region, 'Topic': topic, 'Answer': yes_no, 'Count': count})

def ws_97_csv(writer, counts_list, row, **kwargs):
    regions = kwargs['regions']
    for region_answer in counts_list[row]:
        answer, region = region_answer
        agree_disagree = 'Agree' if answer == 1 else 'Disagree'
        region = [x[1] for x in regions if x[0] == region][0]
        count = counts_list[row][region_answer]
        writer.writerow({'Region': region, 'Topic': row, 'Agree/Disagree': agree_disagree, 'Count': count})

def ws_100_csv(writer, counts_list, row, **kwargs):
    for answer_topic in counts_list[row]:
        answer, topic = answer_topic
        yes_no = 'Yes' if answer == 'Y' else 'No'
        topic = [t for t in MAJOR_TOPICS if t[0] == topic][0][1]
        count = counts_list[row][answer_topic]
        writer.writerow({'Topic': topic, 'Medium': row, 'Yes/No': yes_no, 'Count': count})

def ws_101_csv(writer, counts_list, row, **kwargs):
    gender, topic = row
    gender = get_gender(gender)
    topic = [t for t in MAJOR_TOPICS if t[0] == topic][0][1]
    count = counts_list[row]
    writer.writerow({'Topic': topic, 'Gender': gender, 'Count': count})

def ws_102_csv(writer, counts_list, row, **kwargs):
    agree_disagree, topic = row
    topic = [t for t in MAJOR_TOPICS if t[0] == topic][0][1]
    agree_disagree = 'Agree' if agree_disagree == 1 else 'Disagree'
    count = counts_list[row]
    writer.writerow({'Topic': topic, 'Agree/Disagree': agree_disagree, 'Count': count})

def ws_104_csv(writer, counts_list, row, **kwargs):
    function, gender = row
    function = [func[1] for func in FUNCTION if func[0] == function]
    if function:
        function = function[0][4:] # [4:] is used to remove the (number) part
        gender = get_gender(gender)
        count = counts_list[row]
        writer.writerow({'Topic': kwargs['topic'], 'Gender': gender, 'Function': function, 'Count': count})

def generate_dataset(csv_name, fieldnames, counts_list, func, **kwargs):
    filename = f'dataset/{csv_name}.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in (counts_list):
            func(writer, counts_list, row, **kwargs)
