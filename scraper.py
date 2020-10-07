import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
    last_page = int(pages[-2].get_text(strip=True))
    return last_page

def extract_job(html):
    title = html.find("div", {"class": "grid--cell fl1"}).find('h2').find('a')["title"]
    company, location = html.find("div", {"class": "grid--cell fl1"}).find('h3').find_all("span", recursive=False) #span안의 span 탐색 방지
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\r").strip("\n")
    job_id = html['data-jobid']
    return {'title': title, 'company': company, 'location': location,
            "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scraping SO: Page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
