import csv
from .report_details import *  # noqa
from forms.modelutils import (TOPICS, FUNCTION, )

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

def generate_csv(csv_name, fieldnames, counts_list, func):
    with open(f'csv/{csv_name}.csv', 'a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in (counts_list):
            func(writer, counts_list, row)
