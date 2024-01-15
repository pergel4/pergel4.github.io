from stravascraper import create_new_driver, get_this_weeks_total, get_last_weeks_total
import datetime
import json
from jinja2 import Environment, FileSystemLoader

# Constants
CLUB_LEAD_URL = "https://www.strava.com/clubs/495789/leaderboard"
TOTAL_DAYS = 324 # Dagnummer för 19/11

def get_week_nr():
    date_today = datetime.date.today()
    week_today = date_today.isocalendar()[1]
    return week_today

def get_stats():
    # Get strava data
    driver = create_new_driver(CLUB_LEAD_URL)
    week_nr = get_week_nr()
    current_week = get_this_weeks_total(driver)
    if week_nr != 1:
        last_week = get_last_weeks_total(driver)
        new_stats = {str(week_nr-1): last_week, str(week_nr): current_week}
    else:
        last_week = 0
        new_stats = {str(week_nr): current_week}


    # Store strava data
    try:
        with open('stats.json', 'r') as file:
            stats = json.load(file)
            with open('stats_backup.json', 'w') as backup:
                json.dump(stats, backup)
    except Exception as e:
        stats = None

    with open('stats.json', 'w') as file:
        if stats:
            for key, value in new_stats.items():
                stats[key] = round(value,2)
            json.dump(stats, file)
        else:
            json.dump(new_stats, file)

def write_file():
    with open('stats.json', 'r') as file:
        stats = json.load(file)

    km_total = 0
    weeks = []
    km_week = []
    for key, value in stats.items():
        km_total += value
        weeks.append(key)
        km_week.append(value)

    time_now = datetime.datetime.now()
    update = time_now.strftime("%Y-%m-%d %H:%M:%S")
    day_nr = time_now.timetuple().tm_yday
    pct_goal_today = round(day_nr/TOTAL_DAYS*100,2)

    context = {
        "update": update,
        "pct_goal_today": pct_goal_today,
        "km_total": round(km_total,2),
        "x_labels": weeks,
        "km_week": km_week
    }

    template = Environment(loader=FileSystemLoader("./")).get_template("index_temp.html")
    with open('index.html', 'w') as file:
        file.write(template.render(context))

if __name__ == '__main__':
    get_stats()
    write_file()
    

