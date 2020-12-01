import os

from django.core.management.base import BaseCommand
from django.conf import settings

from coding_sheets.extractor_script import (
    get_journalist,
    get_people,
    get_sheet,
    read_coding_sheet,
)
from coding_sheets.utils import (
    merge_data,
    get_common_coding_data,
    get_newspaper_coding_data,
    get_radio_coding_data,
    get_tv_coding_data,
    get_internet_coding_data,
    get_twitter_coding_data,
    save_newspaper_news_data,
    save_radio_news_data,
    save_tv_news_data,
    save_internent_news_data,
    save_twitter_news_data,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "filelocation",
            help="Folder containing the excel sheets /the excel sheet location",
        )

    def handle(self, *args, **options):
        filelocation = options["filelocation"]
        if os.path.isdir(filelocation):
            # Ignore the extension
            filenames = [
                f"{filelocation}/{file_name}"
                for file_name in os.listdir(filelocation)
                if file_name.endswith("xlsx")
            ]
        else:
            filenames = [filelocation]

        successful_uploads = []
        failed_uploads = []

        for filename in filenames:
            try:
                coding_dict = read_coding_sheet(filename)
                # functions to run
                journalists = get_journalist(coding_dict.copy())
                people = get_people(coding_dict.copy())
                sheets = get_sheet(coding_dict.copy())
                # We can't merge people and journalists since they both have sex and age fields
                data = merge_data(sheets, people)

                newspaper_coding_data = get_newspaper_coding_data(
                    data.get("NewspaperCoding", {})
                )
                journalist_newspaper_coding_data = get_newspaper_coding_data(
                    journalists.get("NewspaperCoding", {})
                )
                radio_coding_data = get_radio_coding_data(data.get("RadioCoding", {}))
                journalist_radio_coding_data = get_radio_coding_data(
                    journalists.get("RadioCoding", {})
                )
                tv_coding_data = get_tv_coding_data(data.get("TelevisionCoding", {}))
                journalist_tv_coding_data = get_tv_coding_data(
                    journalists.get("TelevisionCoding", {})
                )
                internet_coding_data = get_internet_coding_data(
                    data.get("InternetCoding", {})
                )
                journalist_internet_coding_data = get_internet_coding_data(
                    journalists.get("InternetCoding", {})
                )
                twitter_coding_data = get_twitter_coding_data(
                    data.get("TwitterCoding", {})
                )
                journalist_twitter_coding_data = get_twitter_coding_data(
                    journalists.get("TwitterCoding", {})
                )

                save_newspaper_news_data(
                    newspaper_coding_data, journalist_newspaper_coding_data
                )
                save_radio_news_data(radio_coding_data, journalist_radio_coding_data)
                save_tv_news_data(tv_coding_data, journalist_tv_coding_data)
                save_internent_news_data(
                    internet_coding_data, journalist_internet_coding_data
                )
                save_twitter_news_data(
                    twitter_coding_data, journalist_twitter_coding_data
                )
                successful_uploads.append(filename)
            except Exception as error:
                failed_uploads.append({filename: f"Reason: {error}"})

        self.stdout.write(self.style.WARNING(f"The following sheets were not successfully uploaded {failed_uploads}"))
        self.stdout.write(self.style.SUCCESS("Done Uploading files"))
