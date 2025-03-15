from django.core.management.base import BaseCommand
import pandas as pd
from ParserX.models import MCQ
import os

class Command(BaseCommand):
    help = 'Import MCQ data from reasoning.xlsx file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), '../../reasoning.xlsx')
        file_path = os.path.abspath(file_path)

        try:
            df = pd.read_excel(file_path)
            
            for index, row in df.iterrows():
                try:
                    MCQ.objects.create(
                        question=row['question'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_option=row['correct_option']
                    )
                    self.stdout.write(self.style.SUCCESS(f"Imported row {index + 1}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {index + 1}: {e}"))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read file: {e}"))
