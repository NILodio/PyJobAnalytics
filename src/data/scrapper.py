import json
import logging
import os
import random
import re
import time
from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup


class JobScrapper(object):
    def __init__(self, output_filepath=None):
        # get values from .env file
        self.BASE_URL = os.getenv("BASE_URL")
        self.KEYWORDS = json.loads(os.getenv("KEYWORDS"))
        self.BASE_URL_JOBS = os.getenv("BASE_URL_JOBS")
        self.logger = logging.getLogger(__name__)
        self.pages = os.getenv("PAGES")
        self.output_filepath = 'data/raw' if not output_filepath else output_filepath
        self.job_title = []
        self.job_company_name = []
        self.job_salary = []
        self.job_address = []
        self.job_department = []
        self.job_type = []
        self.job_desc = []
        self.job_emp_qn = []
        self.job_posting_time = []
        self.job_url = []

    def save_data(self, df, name="jobs.csv"):
        output_filepath = os.path.join(self.output_filepath, name)
        df.to_csv(output_filepath, index=False)
        self.logger.info("Data saved to: %s", output_filepath)

    def begin_scrap(self):
        self.logger.info("Scrapping process started!")
        self.logger.info("Scraping for %s pages", self.pages)
        for keyword in self.KEYWORDS:
            self.logger.info("Scraping for keyword: %s", keyword)
            url_ = self.BASE_URL + "-in-" + keyword
            i = 1
            while True:
                r = requests.get(url_ + "?page={}".format(i))
                time.sleep(random.randint(1, 3))
                if r.status_code == 200:
                    soup = BeautifulSoup(r.content, "html.parser")
                    job_list = soup.find_all(
                        "a", {"data-automation": "job-list-view-job-link"}
                    )
                    if not job_list or int(self.pages) == i:
                        break
                    for job in job_list:
                        job_link = self.BASE_URL_JOBS + job["href"]
                        self.scrape_job_desc(job_link)
                self.logger.info("Scraping page: %s", i)
                i += 1
            self.logger.info('Scraping for keyword "%s" completed', keyword)
        self.logger.info("Scrapping process Done!")

        df = pd.DataFrame(
            {
                "job_title": self.job_title,
                "job_company_name": self.job_company_name,
                "job_salary": self.job_salary,
                "job_address": self.job_address,
                "job_department": self.job_department,
                "job_type": self.job_type,
                "job_desc": self.job_desc,
                "job_emp_qn": self.job_emp_qn,
                "job_posting_time": self.job_posting_time,
                "job_url": self.job_url,
            }
        )
        self.save_data(df)

    def scrape_job_desc(self, job_url):
        response = requests.get(job_url)
        time.sleep(random.randint(1, 3))
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            self.job_title.append(
                soup.find(
                    "h1",
                    class_="y735df0 _1iz8dgs4y _94v4w0 _94v4wl _1wzghjf4 _94v4wp _94v4w21",
                ).text.strip()
                if soup.find(
                    "h1",
                    class_="y735df0 _1iz8dgs4y _94v4w0 _94v4wl _1wzghjf4 _94v4wp _94v4w21",
                )
                else "N/A."
            )
            self.job_company_name.append(
                soup.find(
                    "span",
                    class_="y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w21 _1wzghjf4 _94v4wd",
                ).text.strip()
                if soup.find(
                    "span",
                    class_="y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w21 _1wzghjf4 _94v4wd",
                )
                else "N/A"
            )
            info = soup.find_all("span", class_="y735df0 _1iz8dgs4y _1iz8dgsr")
            if len(info) > 3:
                self.job_salary.append(info[3].text.strip())
            else:
                self.job_salary.append("N/A")
            self.job_address.append(info[0].text.strip())
            self.job_department.append(info[1].text.strip())
            self.job_type.append(info[2].text.strip())
            self.job_desc.append(
                soup.find("div", class_="y735df0 _1pehz540").text.strip()
                if soup.find("div", class_="y735df0 _1pehz540")
                else "N/A"
            )
            self.job_emp_qn.append(
                soup.find(
                    "ul", class_="y735df0 y735df3 _1akoxc50 _1akoxc56"
                ).text.strip()
                if soup.find("ul", class_="y735df0 y735df3 _1akoxc50 _1akoxc56")
                else "N/A"
            )
            self.job_posting_time.append(
                self.get_date(
                    soup.find_all(
                        "span",
                        class_="y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w22 _1wzghjf4 _94v4wa",
                    )[-1].text.strip()
                )
                if soup.find(
                    "span",
                    class_="y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w22 _1wzghjf4 _94v4wa",
                )
                else "N/A"
            )
            self.job_url.append(job_url)
        else:
            raise Exception("Could not connect")

    def get_date(self, s):
        match = re.search(r"(\d+)([hdwm])", s)
        if match:
            num = int(match.group(1))
            duration = match.group(2)
            now = datetime.now()
            if duration == "h":
                posted_date = now - timedelta(hours=num)
            elif duration == "d":
                posted_date = now - timedelta(days=num)
            elif duration == "w":
                posted_date = now - timedelta(weeks=num)
            elif duration == "m":
                posted_date = now - timedelta(days=num * 30)
            else:
                raise ValueError("Invalid duration specifier")

            return posted_date.strftime("%Y-%m-%d")
        else:
            raise ValueError("Invalid date posted format")
