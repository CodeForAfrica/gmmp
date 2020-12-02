from django.db import models


class ProcessedSheet(models.Model):
    country = models.CharField(max_length=255)
    sheet_name = models.CharField(max_length=255)
    sheet_tab = models.CharField(max_length=255)
    sheet_row = models.IntegerField()

    def __str__(self):
        return f"{self.country}-{self.sheet_name}-{self.sheet_tab}-{self.sheet_row}"


class UnProccessedRow(models.Model):
    country = models.CharField(max_length=255)
    sheet_name = models.CharField(max_length=255)
    sheet_tab = models.CharField(max_length=255)
    sheet_row = models.IntegerField()
    row_error = models.TextField()

    def __str__(self):
        return f"{self.country}-{self.sheet_name}-{self.sheet_tab}-{self.sheet_row}: {self.row_error}"
