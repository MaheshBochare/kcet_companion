import time
import re
import pandas as pd
from rapidfuzz import process, fuzz


# ======================================================
# 🌐 Scraper Layer (LAZY SELENIUM)
# ======================================================

class CollegeScraper:
    def __init__(self, url, wait=6, scroll_pause=1.2):
        self.url = url
        self.wait = wait
        self.scroll_pause = scroll_pause
        self.data = []

    def _init_driver(self):
        # 🔴 LAZY IMPORTS (CRITICAL FIX)
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def scrape(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

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
                "arguments[0].scrollTop += arguments[0].offsetHeight",
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
                    "College_Name": cols[1].find_element(By.TAG_NAME, "h3").text.strip(),
                    "College_URL": link,
                    "Location": cols[1].find_element(By.CLASS_NAME, "location").text.strip(),
                    "Approvals": cols[1].find_element(By.CLASS_NAME, "approvals").text.strip(),
                    "NAAC_Grade": naac[0].text.strip() if naac else "",
                    "First_Year_Fees": fees[0].text.strip() if fees else "",
                    "Avg_Package": pkgs[0].text.strip() if pkgs else "",
                    "Highest_Package": pkgs[1].text.strip() if len(pkgs) > 1 else "",
                    "Rating": cols[4].find_element(By.CLASS_NAME, "lr-key").text.strip(),
                    "National_Ranking": ranking[0].text.strip() if ranking else ""
                })
            except Exception:
                continue

        driver.quit()
        return pd.DataFrame(self.data)


# ======================================================
# 🧠 Matching + Cleaning (UNCHANGED)
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
    def _rank(text):
        if pd.isna(text):
            return None
        match = re.search(r"\d+", str(text).replace(",", ""))
        return int(match.group()) if match else None

    @classmethod
    def normalize(cls, df):
        df["First_Year_Fees"] = df["First_Year_Fees"].apply(cls._number)
        df["Avg_Package"] = df["Avg_Package"].apply(cls._number)
        df["Highest_Package"] = df["Highest_Package"].apply(cls._number)
        df["National_Ranking"] = df["National_Ranking"].apply(cls._rank)
        return df


# ======================================================
# 🚀 Pipeline Runner
# ======================================================

class CollegePipeline:
    def __init__(self, scrape_url, official_file, sheet_index):
        self.scraper = CollegeScraper(scrape_url)
        self.official = pd.read_excel(official_file, sheet_name=sheet_index)

    def run(self):
        scraped = self.scraper.scrape()
        return CollegeDataCleaner.normalize(scraped)
