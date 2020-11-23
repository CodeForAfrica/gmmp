import pandas as pd
import json
from django.conf import settings
import sheets.coding_info as coding_info

pd.set_option("display.max_colwidth", 100)

# read coding sheets
def read_coding_sheet(filename):
    """Read the workbook and extract data into different dataframes.
    """
    # excel file
    file_name = settings.BASE_DIR + "/sheets/data_transfer/data/" + f"{filename}.xlsx"
    xl_file = pd.ExcelFile(file_name)

    # list of coding names
    coding_names = ["Coding", "CODAGE", "CODIFICACIÓN", "CODIFICAÇÃO"]

    sheet_list = []  # empty list to store coding sheet names

    # loop through sheetnames and extract the coding sheets
    for coding in coding_names:
        [sheet_list.append(sheet) for sheet in xl_file.sheet_names if coding in sheet]

    # read workbook
    sheet_dict = pd.read_excel(xl_file, sheet_name=sheet_list)

    return sheet_dict


"""
## 2. Extract the responses from the coding sheet
This function will extract all the responses, leaving out blank columns
"""


def get_response(coding_dict):
    dict_copy = coding_dict.copy()

    # mark the row in which text starts
    qz = ["Story", "Reportage", "Noticia", "Notícia"]

    # extract reponses
    for key, value in dict_copy.items():
        # strip whitespace
        dict_copy[key] = dict_copy[key].applymap(
            lambda x: x.strip() if isinstance(x, str) else x
        )
        # coding starts on the row after "story". create a flag to indicate this row
        dict_copy[key]["flag"] = dict_copy[key].isin(qz).any(1).astype("str")

        # select only the rows below the flag and set the first row as header
        dict_copy[key] = (
            dict_copy[key]
            .iloc[dict_copy[key].flag.str.contains("True").idxmax() :]
            .reset_index(drop=True)
        )

        # set first row as header and drop first two rows
        dict_copy[key] = (
            dict_copy[key]
            .dropna(how="all", axis=1)
            .rename(columns=dict_copy[key].iloc[1])
            .drop(dict_copy[key].index[0:2])
            .drop(columns=["False"])
        )

        # add story label new story after a completely null row
        dict_copy[key].loc[:, "story_label"] = (
            dict_copy[key].isnull().apply(lambda y: all(y), axis=1).cumsum() + 1
        )  # column that indicates story number

        # edit comments question
        col_markers = [
            "Comments",
            "Commentaires",
            "Comentarios",
            "Multimedia",
            "Comentários",
        ]
        new_col = "30 Comments"

        # edit column names
        for col in dict_copy[key].columns:
            for mark in col_markers:
                if mark in col:
                    dict_copy[key].rename(columns={col: new_col}, inplace=True)
                    dict_copy[key].columns = (
                        dict_copy[key]
                        .columns.str.split()
                        .str[0]
                        .str.strip()
                        .str.replace("\(|\)|\.", "")
                    )

                    # edit responses in certain columns
                    dict_copy[key] = dict_copy[key].apply(
                        lambda y: y.replace("(?<=\)).*|\(|\)", "", regex=True)
                        if y.name not in ["30", "story_label"]
                        else y
                    )

                    # drop nulls
                    dict_copy[key].dropna(thresh=2, inplace=True)

    return dict_copy


# 3. Extract the basic information from coding sheets
# read coding info
def get_coding_info(coding_details):

    col_names = coding_info.basic_info
    translations = coding_info.basicinfo_translations

    for a, b in coding_details.items():
        for col, value in col_names.items():
            if col in coding_details[a].columns:
                coding_details[a] = coding_details[a].iloc[
                    :, coding_details[a].columns.get_loc(col) :
                ]
                coding_details[a] = coding_details[a][
                    coding_details[a][col].eq(value).cumsum().lt(1)
                ].transpose()

                # strip whitespace
                coding_details[a] = coding_details[a].applymap(
                    lambda x: x.strip() if isinstance(x, str) else x
                )

                # first row as header
                coding_details[a].rename(
                    columns=coding_details[a].iloc[0], inplace=True
                )
                coding_details[a].drop(coding_details[a].index[0:1], inplace=True)

                # rename columns to match database
                for k, v in translations.items():
                    for col in coding_details[a].columns:
                        if col in v:
                            coding_details[a].rename(columns={col: k}, inplace=True)

                            # replace country code value
                            coding_details[a].fillna(method="ffill", inplace=True)

                            # drop rows
                            coding_details[a] = coding_details[a].tail(1)

    return coding_details


# add coding info to sheet
def add_coding_info(coding_dict):
    # read data
    dict_copy = get_response(coding_dict)

    # coding info
    coding_details = get_coding_info(coding_dict)

    # add coding info
    for key, value in dict_copy.items():
        for info_key, info_value in coding_details.items():
            if info_key == key:
                basicinfo = coding_details[key].columns.tolist()
                dict_copy[key] = pd.concat(
                    [coding_details[info_key], dict_copy[key]], copy=False
                )
                dict_copy[key][basicinfo] = dict_copy[key][basicinfo].fillna(
                    method="ffill"
                )

        # drop nulls
        dict_copy[key].dropna(subset=["story_label"], inplace=True)

    return dict_copy


# extract people info
def get_people(coding_dict):
    # read data
    dict_copy = add_coding_info(coding_dict)

    # read people dict
    people = coding_info.people_dict

    # read sheetname mapping
    mapping = coding_info.sheetname_mapping

    # extract people in the news
    for key, value in dict_copy.items():
        # access mapping dictionary
        for map_name, sheetname in mapping.items():
            # access journalust dictionary
            for main in people:
                if key in sheetname and map_name == main:
                    for a, b in people[main].items():
                        # rename columns
                        for col in dict_copy[key].columns:
                            if col == a:
                                dict_copy[key].rename(columns={col: b}, inplace=True)

        dict_copy[key] = dict_copy[key].filter(regex="^(?![0-9])(?![z])", axis=1)
        dict_copy[key].loc[:, "people_id"] = (
            dict_copy[key].groupby("story_label").cumcount() + 1
        )

    coding_data = format_coding_data(dict_copy)
    return coding_data


# get journalist info
def get_journalist(coding_dict):

    # read data
    dict_copy = add_coding_info(coding_dict)

    # read journalist dict
    journalist = coding_info.journalist_dict

    # read sheetname mapping
    mapping = coding_info.sheetname_mapping

    # extract journalists
    for key, value in dict_copy.items():
        # access mapping dictionary
        for map_name, sheetname in mapping.items():
            # access journalist dictionary
            for main in journalist:
                if key in sheetname and map_name == main:
                    for a, b in journalist[main].items():
                        # rename columns
                        for col in dict_copy[key].columns:
                            if col == a:
                                dict_copy[key].rename(columns={col: b}, inplace=True)

        # filter columns
        dict_copy[key] = dict_copy[key].filter(regex="^(?![0-9])(?![z])", axis=1)

        # add journalist id
        dict_copy[key].loc[:, "journalist_id"] = (
            dict_copy[key].groupby("story_label").cumcount() + 1
        )

        # drop additonal nulls in internet and twitter, brought about by a story having no journalists and multiple people in the news.
        dict_copy[key].dropna(inplace=True)

    coding_data = format_coding_data(dict_copy)
    return coding_data


# Extract information related to the sheet
# get sheet information
def get_sheet(coding_dict):
    # read data
    dict_copy = add_coding_info(coding_dict)

    # read people dict
    sheetinfo = coding_info.sheet_info

    # read sheetname mapping
    mapping = coding_info.sheetname_mapping

    # extract sheet info
    for key, value in dict_copy.items():
        # access mapping dictionary
        for map_name, sheetname in mapping.items():
            # access sheetinfo dictionary
            for main in sheetinfo:
                if key in sheetname and map_name == main:
                    for a, b in sheetinfo[main].items():
                        # rename columns
                        for col in dict_copy[key].columns:
                            if col == a:
                                dict_copy[key].rename(columns={col: b}, inplace=True)

        dict_copy[key] = dict_copy[key].filter(regex="^(?![0-9])(?![z])", axis=1)

        # dropna
        dict_copy[key].dropna(subset=["covid19"], inplace=True)

    coding_data = format_coding_data(dict_copy)
    return coding_data


def format_coding_data(coding_dict):
    mapping = coding_info.sheetname_mapping
    for media in mapping:
        for multi_lang in mapping[media]:
            media_coding = coding_dict.get(multi_lang)
            if media_coding is not None:
                if media == "Print":
                    newspaperCoding = media_coding.to_json()
                if media == "Radio":
                    radioCoding = media_coding.to_json()
                if media == "Television":
                    televisionCoding = media_coding.to_json()
                if media == "Internet":
                    internetCoding = media_coding.to_json()
                if media == "Twitter":
                    twitterCoding = media_coding.to_json()
    return {
        "NewspaperCoding": json.loads(newspaperCoding),
        "RadioCoding": json.loads(radioCoding),
        "TelevisionCoding": json.loads(televisionCoding),
        "InternetCoding": json.loads(internetCoding),
        "TwitterCoding": json.loads(twitterCoding),
    }
