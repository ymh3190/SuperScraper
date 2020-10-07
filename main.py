# flask는 엄청 가벼운 웹 프레임워크
from flask import Flask, render_template, request,\
    redirect, send_file
from scraper import get_jobs
from exporter import save_to_file

app = Flask("SupperScraper")

db = {}

@app.route("/")
def home():
    return render_template("potato.html")

"""
@는 데코레이터로서, 바로 아래에 있는 함수만을 찾는다.
<username>을 통해서 서로 다른 url들을 제어할 수 있다.
"""
@app.route("/<username>")
def contact(username):
    return f"Hello {username} how are you doing"

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        exsistingJobs = db.get(word)
        if exsistingJobs:
            jobs = exsistingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html",
        searchingBy=word,
        resultsNumber=len(jobs),
        jobs=jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.xlsx")
    except:
        return redirect("/")

app.run()

