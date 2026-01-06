from openpyxl import Workbook
from django.http import HttpResponse


def export_to_excel(queryset, fields, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    # Header row
    ws.append(fields)

    # Data rows
    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field)
            row.append(str(value))
        ws.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
    wb.save(response)

    return response
