from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reports.historical import Historical
from reports.report_details import REGION_COUNTRY_MAP, get_countries


class Command(BaseCommand):
    help = "Import historical GMMP data from an XLSX file"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", help="Excel file(s) to import")
        parser.add_argument("--global", action="store_true", help="Coverage is global")
        parser.add_argument(
            "--region",
            action="store",
            dest="region",
            help="Import historical data for a region. One of: {}".format(
                ", ".join(sorted(REGION_COUNTRY_MAP.keys()))
            ),
        )
        parser.add_argument(
            "--country",
            action="store",
            dest="country",
            help="Import historical data for a country. One of: {}".format(
                ", ".join(sorted(c[0] for c in get_countries()))
            ),
        )
        parser.add_argument(
            "--year",
            action="store",
            dest="year",
            help="Historical GMMP year the Excel file(s) belongs to. One of:  2010, 2015",
        )

    def handle(self, *args, **options):
        historical = Historical()
        coverage = None
        region = None
        country = None
        year = options["year"] or settings.REPORTS_HISTORICAL_YEAR
        filenames = options["filename"]

        if year not in ["2010", "2015"]:
            raise ValueError("Invalid historical GMMP year: {}".format(year))

        if options["global"]:
            coverage = "global"
        elif options["region"]:
            coverage = "region"
            region = options["region"]
            if region not in REGION_COUNTRY_MAP:
                raise ValueError("Unknown region: %s" % region)
        elif options["country"]:
            coverage = "country"
            country = options["country"]
            countries = {c: n for c, n in get_countries()}
            if not country.upper() in countries:
                for code, name in countries.items():
                    if name.upper() == country:
                        country = code
                        break
                if not country in countries:
                    raise ValueError("Unknown country: %s" % country)
        else:
            raise CommandError("Must specify --global or --region")

        for fname in filenames:
            historical.import_from_file(
                fname, coverage, region=region, country=country, year=year
            )

        historical.save()
