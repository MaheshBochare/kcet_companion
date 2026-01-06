import pdfplumber
import pandas as pd
import re
from collections import defaultdict


class SeatMatrixPreprocessor:

    CATEGORY_CODES = [
        '1G','1K','1R','2AG','2AK','2AR','2BG','2BK','2BR',
        '3AG','3AK','3AR','3BG','3BK','3BR',
        'GM','GMK','GMR',
        'SCG','SCK','SCR',
        'STG','STK','STR','SNQ',
        'X'   # temporary category
    ]

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # ---------------- MAIN ----------------

    def process(self):
        rows = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(use_text_flow=False)

                xs = sorted(w['x0'] for w in words)
                left_end = xs[int(len(xs) * 0.33)]
                mid_end  = xs[int(len(xs) * 0.66)]

                blocks = [
                    [w for w in words if w['x0'] <= left_end],
                    [w for w in words if left_end < w['x0'] <= mid_end],
                    [w for w in words if w['x0'] > mid_end]
                ]

                for block in blocks:
                    rows.extend(self._parse_block(block))

        if not rows:
            raise ValueError("❌ No rows extracted from PDF")

        return self._finalize(rows)

    # ---------------- BLOCK PARSER ----------------

    def _parse_block(self, words):
        lines = defaultdict(list)

        for w in words:
            y = round(w['top'])
            lines[y].append(w['text'])

        ordered = [" ".join(lines[y]) for y in sorted(lines)]

        results = []
        current_college = None

        for line in ordered:

            m = re.search(r'E\s*\d{3}.*', line)
            if m:
                current_college = m.group().strip()
                continue

            tokens = line.split()

            if tokens and re.fullmatch(r'[A-Z]{2,5}', tokens[0]):

                branch = tokens[0]
                raw_nums = [t for t in tokens[1:] if t.isdigit()]

                SAFE = len(self.CATEGORY_CODES)
                nums = raw_nums[:SAFE] + ['0'] * (SAFE - len(raw_nums))

                if current_college:
                    results.append([current_college, branch] + nums)

        return results

    # ---------------- FINAL NORMALIZATION ----------------

    def _finalize(self, rows):

        SAFE = len(self.CATEGORY_CODES)
        fixed = []

        for r in rows:
            if not r or len(r) < 2:
                continue

            college_name = str(r[0])
            branch = str(r[1])

            raw_nums = [x for x in r[2:] if str(x).isdigit()]
            nums = raw_nums[:SAFE] + ['0'] * (SAFE - len(raw_nums))

            fixed.append([college_name, branch] + nums)

        fixed = [row[:2+SAFE] for row in fixed]

        df = pd.DataFrame(fixed, columns=['college_name','branch'] + self.CATEGORY_CODES)

        df['college_code'] = (
            df['college_name']
            .str.replace(" ", "")
            .str.extract(r'(E\d{3})', expand=False)
            .fillna("UNKNOWN")
        )

        df['code_branch'] = df['college_code'] + " " + df['branch']

        df[self.CATEGORY_CODES] = (
            df[self.CATEGORY_CODES]
            .apply(pd.to_numeric, errors='coerce')
            .fillna(0)
            .astype(int)
        )

        # Compute TOTAL
        df['TOTAL'] = df[self.CATEGORY_CODES].sum(axis=1)

        # 🧮 Business rule using X
        mask = df['X'] > 0
        df.loc[mask, 'TOTAL'] = (df.loc[mask, 'TOTAL'] / 2).astype(int)

        # 🧹 Remove temporary X column
        df = df.drop(columns=['X'])

        # Final column order
        final_categories = [c for c in self.CATEGORY_CODES if c != 'X']
        df = df[['code_branch','college_code','branch'] + final_categories + ['TOTAL']]

        return df
import pandas as pd
from django.db import transaction


from django.db import transaction
#from core.preprocessing.seat_matrix import SeatMatrixPreprocessor
from core.infrastructure.django_models.Branch_college import CollegeBranch
from core.infrastructure.django_models.Year import Year
from core.infrastructure.django_models.category import Category
from core.infrastructure.django_models.Round import Round
from core.infrastructure.django_models.seat_matrix import SeatMatrix
import pdfplumber
import pandas as pd
import re
from collections import defaultdict


class SeatMatrixPreprocessor:

    CATEGORY_CODES = [
        '1G','1K','1R','2AG','2AK','2AR','2BG','2BK','2BR',
        '3AG','3AK','3AR','3BG','3BK','3BR',
        'GM','GMK','GMR',
        'SCG','SCK','SCR',
        'STG','STK','STR','SNQ',
        'X'   # temporary category
    ]

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # ---------------- MAIN ----------------

    def process(self):
        rows = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(use_text_flow=False)

                xs = sorted(w['x0'] for w in words)
                left_end = xs[int(len(xs) * 0.33)]
                mid_end  = xs[int(len(xs) * 0.66)]

                blocks = [
                    [w for w in words if w['x0'] <= left_end],
                    [w for w in words if left_end < w['x0'] <= mid_end],
                    [w for w in words if w['x0'] > mid_end]
                ]

                for block in blocks:
                    rows.extend(self._parse_block(block))

        if not rows:
            raise ValueError("❌ No rows extracted from PDF")

        return self._finalize(rows)

    # ---------------- BLOCK PARSER ----------------

    def _parse_block(self, words):
        lines = defaultdict(list)

        for w in words:
            y = round(w['top'])
            lines[y].append(w['text'])

        ordered = [" ".join(lines[y]) for y in sorted(lines)]

        results = []
        current_college = None

        for line in ordered:

            m = re.search(r'E\s*\d{3}.*', line)
            if m:
                current_college = m.group().strip()
                continue

            tokens = line.split()

            if tokens and re.fullmatch(r'[A-Z]{2,5}', tokens[0]):

                branch = tokens[0]
                raw_nums = [t for t in tokens[1:] if t.isdigit()]

                SAFE = len(self.CATEGORY_CODES)
                nums = raw_nums[:SAFE] + ['0'] * (SAFE - len(raw_nums))

                if current_college:
                    results.append([current_college, branch] + nums)

        return results

    # ---------------- FINAL NORMALIZATION ----------------

    def _finalize(self, rows):

        SAFE = len(self.CATEGORY_CODES)
        fixed = []

        for r in rows:
            if not r or len(r) < 2:
                continue

            college_name = str(r[0])
            branch = str(r[1])

            raw_nums = [x for x in r[2:] if str(x).isdigit()]
            nums = raw_nums[:SAFE] + ['0'] * (SAFE - len(raw_nums))

            fixed.append([college_name, branch] + nums)

        fixed = [row[:2+SAFE] for row in fixed]

        df = pd.DataFrame(fixed, columns=['college_name','branch'] + self.CATEGORY_CODES)

        # 🔍 Extract college code
        df['college_code'] = (
            df['college_name']
            .str.replace(" ", "")
            .str.extract(r'(E\d{3})', expand=False)
            .fillna("UNKNOWN")
        )

        # 🧭 Normalize branch (take only first 2 letters)
        df['branch'] = (
            df['branch']
            .astype(str)
            .str.strip()
            .str.upper()
            .str.extract(r'^([A-Z]{2})')
        )

        # 🔗 Build relational key
        df['code_branch'] = df['college_code'] + "_" + df['branch']

        # Convert seats
        df[self.CATEGORY_CODES] = (
            df[self.CATEGORY_CODES]
            .apply(pd.to_numeric, errors='coerce')
            .fillna(0)
            .astype(int)
        )

        # 🧹 Remove temp X
        df = df.drop(columns=['X'])

        # 🧪 Melt to ingestion-ready format
        value_cols = [c for c in self.CATEGORY_CODES if c != 'X']

        long_df = df.melt(
            id_vars=["code_branch"],
            value_vars=value_cols,
            var_name="category",
            value_name="seats"
        )

        # Remove zero seats
        long_df = long_df[long_df["seats"] > 0].reset_index(drop=True)

        return long_df


class SeatMatrixIngestionService:

    CATEGORY_CODES = [
        '1G','1K','1R','2AG','2AK','2AR','2BG','2BK','2BR',
        '3AG','3AK','3AR','3BG','3BK','3BR',
        'GM','GMK','GMR',
        'SCG','SCK','SCR',
        'STG','STK','STR','SNQ'
    ]

    @staticmethod
    @transaction.atomic
    def ingest(pdf_path, year_code, round_code):

        df = SeatMatrixPreprocessor(pdf_path).process()

        year, _ = Year.objects.get_or_create(year_code=year_code)
        round_obj, _ = Round.objects.get_or_create(round_code=round_code)

        branch_cache = {b.code_branch: b for b in CollegeBranch.objects.all()}
        category_cache = {c.category_code: c for c in Category.objects.all()}

        stats = {
            "rows_processed": 0,
            "created": 0,
            "updated": 0,
            "missing_branches": 0,
            "missing_categories": 0,
            "zero_seats_skipped": 0
        }

        for _, row in df.iterrows():
            stats["rows_processed"] += 1

            branch = branch_cache.get(row['code_branch'])
            if not branch:
                stats["missing_branches"] += 1
                continue

            for cat in SeatMatrixIngestionService.CATEGORY_CODES:

                seats = int(row.get(cat, 0))

                if seats <= 0:
                    stats["zero_seats_skipped"] += 1
                    continue

                category = category_cache.get(cat)
                if not category:
                    stats["missing_categories"] += 1
                    continue

                _, created = SeatMatrix.objects.update_or_create(
                    college_branch=branch,
                    year=year,
                    category=category,
                    round=round_obj,
                    defaults={"total_seats": seats}
                )

                if created:
                    stats["created"] += 1
                else:
                    stats["updated"] += 1

        return stats
