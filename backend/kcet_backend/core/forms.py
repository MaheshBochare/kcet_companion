from django import forms

class CollegeExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload College Excel File (.xlsx)"
    )
