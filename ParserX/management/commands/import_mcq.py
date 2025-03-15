from django.core.management.base import BaseCommand
import pandas as pd
from ParserX.models import MCQ
import os

class Command(BaseCommand):
    help = 'Import MCQ data from all Excel files in /data folder'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(os.path.dirname(__file__), '../../data')
        data_dir = os.path.abspath(data_dir)

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {data_dir}"))
            return

        for category_folder in os.listdir(data_dir):
            category_path = os.path.join(data_dir, category_folder)

            if os.path.isdir(category_path):
                for file in os.listdir(category_path):
                    if file.endswith('.xlsx'):
                        file_path = os.path.join(category_path, file)
                        self.import_mcq(file_path, category_folder)

    def import_mcq(self, file_path, category):
        try:
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                try:
                    MCQ.objects.create(
                        category=category,
                        question=row['Questions'],
                        option_a=row['A'],
                        option_b=row['B'],
                        option_c=row['C'],
                        option_d=row['D'],
                        correct_option=row['Ans']
                    )
                    self.stdout.write(self.style.SUCCESS(f"Imported {category} - row {index + 1}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing {category} - row {index + 1}: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read file {file_path}: {e}"))
