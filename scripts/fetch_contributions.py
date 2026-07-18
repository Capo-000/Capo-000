import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

USERNAME = "Capo-000"
URL = f"https://github.com/users/{USERNAME}/contributions"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "data", "contributions.json")

resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
cells = soup.find_all("td", class_="ContributionCalendar-day")

days = []
for cell in cells:
    date = cell.get("data-date")
    count = int(cell.get("data-level", 0))
    if date:
        days.append({"date": date, "count": count})

days.sort(key=lambda d: d["date"])

total = sum(d["count"] for d in days)
current_streak = 0
longest_streak = 0
streak = 0
today = datetime.now().strftime("%Y-%m-%d")

for d in reversed(days):
    if d["count"] > 0:
        streak += 1
    else:
        if streak > longest_streak:
            longest_streak = streak
        streak = 0
        if d["date"] == today:
            break

if streak > longest_streak:
    longest_streak = streak

if days and days[-1]["count"] > 0:
    current_streak = streak

best_day = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

monthly = {}
for d in days:
    ym = d["date"][:7]
    monthly[ym] = monthly.get(ym, 0) + d["count"]

data = {
    "username": USERNAME,
    "total": total,
    "current_streak": current_streak,
    "longest_streak": longest_streak,
    "best_day": best_day,
    "monthly": monthly,
    "days": days,
}

with open(OUT, "w") as f:
    json.dump(data, f, indent=2)
print(f"Saved {OUT} ({len(days)} days, {total} contributions)")
