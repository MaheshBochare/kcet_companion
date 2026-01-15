import re
import pandas as pd 
from rapidfuzz import process, fuzz

import numpy as np
import logging as logger
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
class CollegeDataCleaner:

    @staticmethod
    def _number(text):
        if pd.isna(text): 
            return None
        text = re.sub(r"[₹,$]", "", str(text))
        m = re.search(r"\d+(\.\d+)?", text)
        return float(m.group()) if m else None

    @staticmethod
    def _rating(text):
        if pd.isna(text): 
            return None
        m = re.search(r"\d+(\.\d+)?", str(text))
        return float(m.group()) if m else None

    @staticmethod
    def _rank(text):
        if pd.isna(text): 
            return None
        m = re.search(r"\d+", str(text).replace(",", ""))
        return int(m.group()) if m else None

    @classmethod
    def normalize(cls, df):
        df["First_Year_Fees"] = df["First_Year_Fees"].apply(cls._number)
        df["Avg_Package"] = df["Avg_Package"].apply(cls._number)
        df["Highest_Package"] = df["Highest_Package"].apply(cls._number)
        df["Rating"] = df["Rating"].apply(cls._rating)
        df["National_Ranking"] = df["National_Ranking"].apply(cls._rank)
        return df
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

            result = process.extractOne(query, self.choices, scorer=fuzz.token_set_ratio)
            if not result:
                continue

            _, score, idx = result

            # ✅ KEEP ONLY PERFECT MATCHES
            if score == 100:
                official = self.official.iloc[idx]

                matched.append({
                    **row,
                    "college_code": official[self.code_col],
                    "Match_Score": 100
                })

        df = pd.DataFrame(matched)
        return CollegeDataCleaner.normalize(df)

class CollegeScraper:
    def __init__(self, url, wait=6, scroll_pause=1.2):
        self.url = url
        self.wait = wait
        self.scroll_pause = scroll_pause
        self.data = []

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
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

            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scroll_container
            )
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
                    "NAAC_Grade": naac[0].text.strip() if naac else None,
                    "First_Year_Fees": fees[0].text.strip() if fees else None,
                    "Avg_Package": pkgs[0].text.strip() if pkgs else None,
                    "Highest_Package": pkgs[1].text.strip() if len(pkgs) > 1 else None,
                    "Rating": cols[4].find_element(By.CLASS_NAME, "lr-key").text.strip(),
                    "Reviews": cols[4].find_element(By.CLASS_NAME, "lr-value").text.strip(),
                    "National_Ranking": ranking[0].text.strip() if ranking else None
                })

            except Exception:
                continue

        driver.quit()
        return pd.DataFrame(self.data)
