import time, re
import pandas as pd
from rapidfuzz import process, fuzz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ======================================================
# 🌐  Scraper Layer
# ======================================================

class CollegeScraper:
    def __init__(self, url, wait=6, scroll_pause=1.2):
        self.url = url
        self.wait = wait
        self.scroll_pause = scroll_pause
        self.data = []

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape(self):
        driver = self._init_driver()
        driver.get(self.url)
        time.sleep(self.wait)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.listing-table")))

        scroll_container = driver.find_element(By.CSS_SELECTOR, "div.table-wrapper")

        last_count, stable_rounds = 0, 0

        while True:
            rows = driver.find_elements(By.CSS_SELECTOR, "table.listing-table tbody tr")
            current_count = len(rows)

            if current_count == last_count:
                stable_rounds += 1
            else:
                stable_rounds = 0
                last_count = current_count

            if stable_rounds >= 6:
                break

            driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight", scroll_container)
            time.sleep(self.scroll_pause)

        seen = set()

        for row in rows:
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                link = cols[1].find_element(By.TAG_NAME, "a").get_attribute("href")

                if link in seen:
                    continue
                seen.add(link)

                naac = cols[1].find_elements(By.CLASS_NAME, "naac-grade")
                fees = cols[2].find_elements(By.CLASS_NAME, "text-green")
                pkgs = cols[3].find_elements(By.CLASS_NAME, "text-green")
                ranking = cols[5].find_elements(By.CLASS_NAME, "rank-span")

                self.data.append({
                    "CD_Rank": cols[0].text.strip(),
                    "College_Name": cols[1].find_element(By.TAG_NAME, "h3").text.strip(),
                    "College_URL": link,
                    "Location": cols[1].find_element(By.CLASS_NAME, "location").text.strip(),
                    "Approvals": cols[1].find_element(By.CLASS_NAME, "approvals").text.strip(),
                    "NAAC_Grade": naac[0].text.strip() if naac else "",
                    "First_Year_Fees": fees[0].text.strip() if fees else "",
                    "Avg_Package": pkgs[0].text.strip() if pkgs else "",
                    "Highest_Package": pkgs[1].text.strip() if len(pkgs) > 1 else "",
                    "Rating": cols[4].find_element(By.CLASS_NAME, "lr-key").text.strip(),
                    "Reviews": cols[4].find_element(By.CLASS_NAME, "lr-value").text.strip(),
                    "National_Ranking": ranking[0].text.strip() if ranking else ""
                })
            except:
                continue

        driver.quit()
        return pd.DataFrame(self.data)


# ======================================================
# 🧹  Data Normalization Layer
# ======================================================

class CollegeDataCleaner:

    @staticmethod
    def _number(text):
        if pd.isna(text):
            return None
        text = re.sub(r"[₹,$]", "", str(text))
        match = re.search(r"\d+(\.\d+)?", text)
        return float(match.group()) if match else None

    @staticmethod
    def _rating(text):
        if pd.isna(text):
            return None
        match = re.search(r"\d+(\.\d+)?", str(text))
        return float(match.group()) if match else None

    @staticmethod
    def _rank(text):
        if pd.isna(text):
            return None
        match = re.search(r"\d+", str(text).replace(",", ""))
        return int(match.group()) if match else None

    @classmethod
    def normalize(cls, df):
        df["First_Year_Fees"]  = df["First_Year_Fees"].apply(cls._number)
        df["Avg_Package"]      = df["Avg_Package"].apply(cls._number)
        df["Highest_Package"]  = df["Highest_Package"].apply(cls._number)
        df["Rating"]           = df["Rating"].apply(cls._rating)
        df["National_Ranking"] = df["National_Ranking"].apply(cls._rank)
        return df


# ======================================================
# 🧠  Matching Layer
# ======================================================

class CollegeNameMatcher:
    def __init__(self, official_path, sheet_index):
        self.official = pd.read_excel(official_path, sheet_name=sheet_index)
        self.name_col = self._detect("name")
        self.code_col = self._detect("code")

        self.official["clean_name"] = self.official[self.name_col].apply(self._clean)
        self.choices = self.official["clean_name"].tolist()

    def _detect(self, key):
        for col in self.official.columns:
            if key in col.lower():
                return col
        raise ValueError(f"Column containing '{key}' not found")

    def _clean(self, text):
        text = "" if pd.isna(text) else text.lower()
        text = re.sub(r"\(.*?\)|\[.*?\]", "", text)
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def match(self, scraped_df):
        matched = []

        for _, row in scraped_df.iterrows():
            query = self._clean(row["College_Name"])
            _, score, idx = process.extractOne(query, self.choices, scorer=fuzz.token_set_ratio)

            if score == 100:
                official = self.official.iloc[idx]
                matched.append({**row, "college_code": official[self.code_col], "Match_Score": score})

        df = pd.DataFrame(matched)
        return CollegeDataCleaner.normalize(df)


# ======================================================
# 🚀  Pipeline Runner
# ======================================================

class CollegePipeline:
    def __init__(self, scrape_url, official_file, sheet_index):
        self.scraper = CollegeScraper(scrape_url)
        self.matcher = CollegeNameMatcher(official_file, sheet_index)

    def run(self, output_path="final_college_master.csv"):
        scraped = self.scraper.scrape()
        final_df = self.matcher.match(scraped)
        final_df.to_csv(output_path, index=False)
        return final_df
from django.db import transaction
from core.models import College


# ======================================================
# 🗃️  Django Ingestion Service
# ======================================================

class CollegeIngestionService:

    @staticmethod
    @transaction.atomic
    def refresh_colleges():
        pipeline = CollegePipeline(
            scrape_url="https://collegedunia.com/btech/karnataka-colleges?exam_id=61",
            official_file=r"C:\Users\mahes\OneDrive\Desktop\kcet_companion\backend\kcet_backend\core\data\collegedunia_college_names.xlsx",
            sheet_index=3
        )

        df = pipeline.run()

        count = 0
        for _, row in df.iterrows():
            College.objects.update_or_create(
                college_code=row["college_code"],
                defaults={
                    "College_name": row["College_Name"],
                    "location": row["Location"],
                    "approvals": row["Approvals"],
                    "naaccrating": row["NAAC_Grade"],
                    "firstyearfees": row["First_Year_Fees"],
                    "averagepackage": row["Avg_Package"],
                    "highestpackage": row["Highest_Package"],
                    "Rating": row["Rating"],
                    "nationalrank": row["National_Ranking"],
                }
            )
            count += 1

        print(f"✅ Database updated: {count} colleges")
        return count
