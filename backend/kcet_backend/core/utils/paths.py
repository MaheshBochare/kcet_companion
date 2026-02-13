from pathlib import Path
from django.conf import settings

def data_file(filename):
    return Path(settings.BASE_DIR) /'core'/'data'/'collegedunia_college_names.xlsx'