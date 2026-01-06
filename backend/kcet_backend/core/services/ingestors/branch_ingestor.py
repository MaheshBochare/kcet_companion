from core.models import Branch
from django.db import transaction

class BranchIngestor:
    def run(self):
        from core.data.branchdata import BRANCH_DATA
        from core.services.preprocessing.branch_ingestion import detect_degree, detect_stream

        with transaction.atomic():
            for code, name in BRANCH_DATA.items():
                Branch.objects.update_or_create(
                    Branch_Code=code,
                    defaults={
                        "Branch_Name": name,
                        "Stream": detect_stream(name),
                        "Degree_Type": detect_degree(name),
                        "Duration_Years": 4 if detect_degree(name) in ["BE", "BTech"] else 3,
                        "Is_Core_Branch": code in {"CS", "EC", "ME", "CE", "EE"},
                        "Is_Emerging_Branch": any(x in name.upper() for x in ["AI", "DATA", "CYBER", "ROBOT", "IOT"]),
                        "Is_Active": True
                    }
                )
