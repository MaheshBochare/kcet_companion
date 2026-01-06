import pandas as pd
import re
from sklearn.base import BaseEstimator, TransformerMixin


class CutoffDataPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, round_type, year, additional_data_path=None):
        self.round_type = round_type
        self.year = year
        self.additional_data_path = additional_data_path

        self.category_order = [
            "1G","1K","1R","2AG","2AK","2AR","2BG","2BK","2BR",
            "3AG","3AK","3AR","3BG","3BK","3BR",
            "GM","GMK","GMR","SCG","SCK","SCR","STG","STK","STR"
        ]

    def extract_college_names(self, series):
        college_name = None
        names = []
        for value in series:
            if pd.notna(value) and isinstance(value, str) and re.match(r'[A-Z]\d{3}', value.strip()):
                college_name = value
            names.append(college_name)
        return names

    def clean_college_name(self, name):
        return "" if pd.isna(name) else re.sub(r'\bE\d{3}\b|\n', '', name).strip()

    def categorize_branch(self, branch):
        branch_mappings = {
            'CSE': ['CS','Computer','AI','Data'],
            'ECE': ['EC','Electronics'],
            'MECH': ['ME','Mechanical'],
            'CIVIL': ['CE','Civil'],
            'IT': ['IT'],
            'EEE': ['EE','Electrical']
        }
        branch = str(branch)
        for key, values in branch_mappings.items():
            if any(v.lower() in branch.lower() for v in values):
                return key
        return 'Other'

    def fit(self, X, y=None):
        return self

    def transform(self, file_path):

        sheets = pd.read_excel(file_path, sheet_name=None)
        df = pd.concat(sheets.values(), ignore_index=True)

        # Extract & clean college info
        df["college_name"] = self.extract_college_names(df.iloc[:, 0])
        df = df[
            df.iloc[:, 0].notna() &
            ~df.iloc[:, 0].astype(str).str.match(r'[A-Z]\d{3}', na=False)
        ]

        df["college_code"] = df["college_name"].astype(str).str[:4]
        df["Branch"] = df.iloc[:, 0].astype(str)

        # 🧼 Clean branch → only first 2 letters
        df["Branch"] = (
            df["Branch"]
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .str.upper()
            .str.extract(r'^([A-Z]{2})')
        )

        df = df[df["Branch"].notna()]

        # Build code_branch
        df["code_branch"] = df["college_code"] + "_" + df["Branch"]

        # Assign category placeholders
        base_cols = ["Branch"]
        cat_cols = [f"Cat_{i+1}" for i in range(len(self.category_order))]
        tail_cols = ["college_name", "college_code", "branchsss", "code_branch"]
        df.columns = base_cols + cat_cols + tail_cols

        # Rename Cat_i → actual category names
        rename_map = {f"Cat_{i+1}": self.category_order[i] for i in range(len(self.category_order))}
        df = df.rename(columns=rename_map)

        # 🧊 MELT
        melted = df.melt(
            id_vars=["code_branch"],
            value_vars=self.category_order,
            var_name="category",
            value_name="rank"
        )

        melted["round"] = self.round_type
        melted["year"] = self.year

        # Clean ranks
        melted["rank"] = pd.to_numeric(melted["rank"], errors="coerce")
        melted = melted.dropna(subset=["rank"])
        melted["rank"] = melted["rank"].astype(int)

        return melted[["code_branch", "category", "round", "year", "rank"]]
