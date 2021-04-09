import csv, os
from .report_details import *  # noqa
from forms.modelutils import (TOPICS, FUNCTION, YESNO, )

def get_gender(gender_id):
    return "Female" if gender_id==1 else "Male"

def ws_05_csv(writer, counts_list, row):
    for media_type in row:
        for topic in row[media_type]:
            topic_name = [x for x in MAJOR_TOPICS if x[0] == topic[1]][0][1]
            gender = get_gender(topic[0])

            writer.writerow({'Topic': topic_name, 'Gender': gender, 'Medium': media_type, 'Count': row[media_type][topic]})

def ws_09_csv(writer, counts_list, row):
    topic = [y for x in TOPICS for y in x[1] if y[0]==row[1]][0][1]
    gender = get_gender(row[0])

    writer.writerow({'Topic': topic, 'Gender': gender, 'Count': counts_list[row]})

def ws_15_csv(writer, counts_list, row):
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

def generate_csv(csv_name, fieldnames, counts_list, func, **kwargs):
    filename = f'csv/{csv_name}.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in (counts_list):
            func(writer, counts_list, row, **kwargs)
