import os
import numpy as np
import pandas as pd

from gmmpcoding import coding_info


pd.set_option('display.max_colwidth', -1)

def read_coding_sheet(filename):
    """Read the workbook and extract data into different dataframes.
    """
    #excel file
    xl_file = pd.ExcelFile(filename)

    #list of coding names
    coding_names = ['Coding', 'CODAGE', 'CODIFICACIÓN', 'CODIFICAÇÃO']

    sheet_list = [] #empty list to store coding sheet names

    #loop through sheetnames and extract the coding sheets
    for sheet in xl_file.sheet_names:
        for coding in coding_names:
            if coding in sheet:
                sheet_list.append(sheet)

    #read workbook
    sheet_dict = pd.read_excel(xl_file, sheet_name = sheet_list)

    return sheet_dict


def get_response(filename):
    #read data
    coding_dict = read_coding_sheet(filename)

    dict_copy = coding_dict.copy()

    #mark the row in which text starts
    qz = ['Story', 'Reportage', 'Noticia', 'Notícia']

    #import dict which identifies how each sheet looks like
    medias = coding_info.media_dict

    #TODO strip text
    for key,value in dict_copy.items():
        for media_key, media_value in medias.items():
            try:
                if key in dict_copy:
                    name = media_value

                    sheet_title = dict_copy[key].columns[dict_copy[key].isin([name]).any()]

                    dict_copy[key] = dict_copy[key].iloc[:,dict_copy[key].columns.get_loc(str(sheet_title[0])):]

                    #coding starts on the row after "story". create a flag to indicate this row
                    dict_copy[key]['flag'] = dict_copy[key].isin(qz).any(1).astype('str')

                    #select only the rows below the flag and set the first row as header
                    dict_copy[key] = dict_copy[key].iloc[dict_copy[key]\
                                    .flag.str.contains('True').idxmax():].reset_index(drop = True)

                    #set first row as header and drop first two rows
                    dict_copy[key] = dict_copy[key].dropna(how = 'all', axis = 1)\
                                    .rename(columns = dict_copy[key].iloc[1])\
                                    .drop(dict_copy[key].index[0:2])

                    dict_copy[key] = dict_copy[key].drop(columns = ['False'])

                    #drop null rows
                    dict_copy[key].dropna(how = 'all', inplace = True)
                    # add story label new story starts when the first column is not null
                    dict_copy[key]['story_label'] = dict_copy[key].iloc[:,0].notnull().cumsum() #column that indicates story number

                    #edit comments question
                    col_markers = ['Comments','Commentaires','Comentarios','Multimedia','Comentários']
                    new_col = '30 Comments'

                    #edit column names
                    for col in dict_copy[key].columns:
                        for mark in col_markers:
                            if mark in col:
                                dict_copy[key].rename(columns = {col: new_col}, inplace = True)
                                dict_copy[key].columns = dict_copy[key].columns.str.split().str[0].str.strip()\
                                                        .str.replace("\(|\)|\.","")

                                #edit responses in certain columns
                                dict_copy[key] = dict_copy[key].apply(lambda y: y.replace("(?<=\)).*|\(|\)", "", regex = True) if y.name not in ['30', 'story_label'] else y)
            except:
                pass

    return dict_copy


def get_coding_info(filename):
    coding_details = read_coding_sheet(filename)

    col_names = coding_info.basic_info
    translations = coding_info.basicinfo_translations

    for a, b in coding_details.items():
        for col, value in col_names.items():
            if col in coding_details[a].columns:
                coding_details[a] = coding_details[a].iloc[:,coding_details[a].columns.get_loc(col):] 
                coding_details[a] = coding_details[a][coding_details[a][col].eq(value).cumsum().lt(1)]\
                                .transpose()

                #replace country code value
                coding_details[a].fillna(method = 'ffill', inplace = True)

                #first row as header
                coding_details[a].rename(columns=coding_details[a].iloc[0], inplace = True)
                coding_details[a].drop(coding_details[a].index[0:2], inplace = True)

                #rename columns to match database
                for k, v in translations.items():
                    for col in coding_details[a].columns:
                        if col in v:
                            coding_details[a].rename(columns = {col:k}, inplace = True)
    return coding_details


def add_coding_info(filename):
    #read data
    dict_copy = get_response(filename)

    #coding info
    coding_details = get_coding_info(filename)

    # add coding info
    for key, value in dict_copy.items():
        for info_key, info_value in coding_details.items():
            if info_key == key:
                null_cols = coding_details[key].columns.tolist()
                dict_copy[key] = pd.concat([coding_details[info_key],dict_copy[key]], copy = False)
                dict_copy[key][null_cols] = dict_copy[key][null_cols].fillna(method = 'ffill')
                #drop nulls
                dict_copy[key].dropna(subset = ['story_label'], inplace = True)
    return dict_copy


def get_people(filename):
    #read data
    dict_copy = add_coding_info(filename)

    #read people dict
    people = coding_info.people_dict

    for key, value in dict_copy.items():
        for main in people:
            for a,b in people[main].items():
                for col in dict_copy[key].columns:
                    if key == main and col == a:
                        dict_copy[key].rename(columns = {col:b}, inplace = True)

        dict_copy[key] = dict_copy[key].filter(regex = '^(?![0-9])(?![z])', axis = 1)
        dict_copy[key]['person_id'] = dict_copy[key].groupby('story_label').cumcount()+1

    return dict_copy


def get_journalist(filename):
    #read data
    dict_copy = add_coding_info(filename)

    #read people dict
    journalist = coding_info.journalist_dict

    for key, value in dict_copy.items():
        for main in journalist:
            for a,b in journalist[main].items():
                for col in dict_copy[key].columns:
                    if key == main and col == a:
                        dict_copy[key].rename(columns = {col:b}, inplace = True)

        dict_copy[key] = dict_copy[key].filter(regex = '^(?![0-9])(?![z])', axis = 1)
        #drop nulls
        # dict_copy[key] = dict_copy[key][(dict_copy[key]['role'].notnull()) | (dict_copy[key]['journalist_id'] == 1)]

    return dict_copy


def get_sheet(filename):
    #read data
    dict_copy = add_coding_info(filename)

    #read people dict
    sheetinfo = coding_info.sheet_info

    for key, value in dict_copy.items():
        for main in sheetinfo:
            for a,b in sheetinfo[main].items():
                for col in dict_copy[key].columns:
                    if key == main and col == a:
                        dict_copy[key].rename(columns = {col:b}, inplace = True)

        dict_copy[key] = dict_copy[key].filter(regex = '^(?![0-9])(?![z])', axis = 1)

        #dropna
        dict_copy[key].dropna(subset = ['covid19'], inplace = True)
    return dict_copy


story_name = "./data/bbc_world.xlsx"
get_people(story_name)['InternetCoding'].to_json(orient ='records')
get_journalist(story_name)['InternetCoding'].to_json(orient ='records')
get_sheet(story_name)['InternetCoding'].to_json(orient ='records')
