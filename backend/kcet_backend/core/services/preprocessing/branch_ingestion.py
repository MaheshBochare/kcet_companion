from django.core.management.base import BaseCommand
from core.models import Branch

# =======================
# 1️⃣ Complete Raw Dataset
# =======================

BRANCH_DATA = {
    # ---- Medical & Allied Health ----
    "BN": "B.Sc Nursing",
    "BT": "B.Sc Radiotherapy",
    "PT": "Bachelor of Physiotherapy",
    "BR": "B.Sc Respiratory Care Technology",
    "PO": "Bachelor of Prosthetics and Orthotics",
    "BE": "B.Sc Emergency",
    "BD": "B.Sc Renal Dialysis Technology",
    "OT": "B.Sc Operation Theater Technology",
    "BA": "B.Sc Anaesthesia and Operation Theater Technology",
    "RI": "B.Sc Radiology Technology",
    "BC": "B.Sc Cardiac Care Technology",
    "BU": "Bachelor of Audiology",
    "BI": "B.Sc Imaging Technology",
    "BO": "Bachelor of Occupational Therapy",
    "BL": "B.Sc Medical Laboratory Technology",
    "MR": "B.Sc Medical Records Technology",
    "BS": "B.Sc Neuro Science Technology",
    "BH": "Bachelor of Public Health",
    "BM": "B.Sc Optometry",
    "HA": "Bachelor of Hospital Administration",
    "BP": "B.Sc Perfusion Technology",

    # ---- Pharmacy ----
    "BPY": "B.Pharm",
    "PD": "Pharma-D",

    # ---- Engineering ----
    "AD": "Artificial Intelligence And Data Science",
    "AE": "Aeronautical Engineering",
    "AI": "Artificial Intelligence and Machine Learning",
    "AR": "Architecture",
    "AT": "Automotive Engineering",
    "AU": "Automobile Engineering",
    "BC2": "BTech Computer Technology",
    "BD2": "Computer Science Engineering-Big Data",
    "BE2": "Bio-Electronics Engineering",
    "BI2": "Information Technology and Engineering",
    "BM2": "Bio Medical Engineering",
    "BR2": "BioMedical and Robotic Engineering",
    "BT2": "Bio Technology",
    "CA": "Computer Science Engineering-AI",
    "CB": "Computer Science and Business Systems",
    "CC": "Computer and Communication Engineering",
    "CD": "Computer Science and Design",
    "CE": "Civil Engineering",
    "CH": "Chemical Engineering",
    "CO": "Computer Engineering",
    "CS": "Computers Science And Engineering",
    "CY": "Computer Science Engineering-Cyber",
    "DC": "Data Sciences",
    "DM": "Computer Science and Engineering",
    "DS": "Computer Science Engineering-Data",
    "EA": "Agriculture Engineering",
    "EC": "Electronics and Communication Engineering",
    "EE": "Electrical And Electronics Engineering",
    "EG": "Energy Engineering",
    "ME": "Mechanical Engineering",
    "MN": "Mining Engineering",

    # ---- Farm Sciences ----
    "FH": "B.F.Sc Fisheries Science",
    "AM": "B.Sc.(Hons) Ag. Business Management",
    "AG": "B.Sc.(Hons) Agriculture",
    "HS": "B.Sc.(Hons) Community Science",
    "FR": "B.Sc.(Hons) Forestry",
    "HT": "B.Sc.(Hons) Horticulture",
    "SR": "B.Sc.(Hons) Sericulture",
    "VS": "B.V.Sc and A.H"
}

# =======================
# 2️⃣ Intelligent Detectors
# =======================

def detect_degree(name):
    name = name.upper()
    if "PHARMA" in name: return "PharmaD"
    if "B.PHARM" in name: return "BPharm"
    if "B.V.SC" in name: return "BVSc"
    if "B.SC" in name: return "BSc"
    if "B.F.SC" in name: return "BFSc"
    if "B.TECH" in name: return "BTech"
    if "ARCH" in name: return "BArch"
    return "BE"

def detect_stream(name):
    n = name.upper()
    if any(k in n for k in ["COMPUTER", "AI", "DATA", "CYBER", "SOFTWARE"]):
        return "Computer Science"
    if any(k in n for k in ["ELECTRONICS", "ELECTRICAL", "VLSI", "COMMUNICATION"]):
        return "Electronics & Communication"
    if any(k in n for k in ["MECHANICAL", "MECHATRONICS", "AUTOMOBILE"]):
        return "Mechanical"
    if any(k in n for k in ["CIVIL", "CONSTRUCTION", "PLANNING"]):
        return "Civil"
    if any(k in n for k in ["MEDICAL", "NURSING", "RADIOLOGY", "PHYSIOTHERAPY", "HOSPITAL"]):
        return "Medical"
    if "PHARM" in n:
        return "Pharmacy"
    if any(k in n for k in ["AGRICULTURE", "HORTICULTURE", "FORESTRY", "FISHERIES"]):
        return "Agriculture"
    if "VETERINARY" in n:
        return "Veterinary"
    return "General"

# =======================
# 3️⃣ Django Command
# =======================

class Command(BaseCommand):
    help = "Ingest all academic branches into Branch table"

    def handle(self, *args, **kwargs):
        for code, name in BRANCH_DATA.items():
            degree = detect_degree(name)
            stream = detect_stream(name)

            is_core = code in {"CS", "EC", "ME", "CE", "EE"}
            is_emerging = any(k in name.upper() for k in ["AI", "DATA", "CYBER", "ROBOT", "IOT"])

            Branch.objects.update_or_create(
                Branch_Code=code,
                defaults={
                    "Branch_Name": name,
                    "Stream": stream,
                    "Degree_Type": degree,
                    "Duration_Years": 4 if degree in {"BE", "BTech"} else 3,
                    "Is_Core_Branch": is_core,
                    "Is_Emerging_Branch": is_emerging,
                    "Is_Active": True
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Branch ingestion completed successfully"))
