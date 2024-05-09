from stravascraper import create_new_driver, log_in, get_this_weeks_total, get_last_weeks_total
import datetime
import json
from jinja2 import Environment, FileSystemLoader

# Constants
STRAVA_URL = "https://www.strava.com/"
CLUB_LEAD_URL = "https://www.strava.com/clubs/495789/leaderboard"
TOTAL_DAYS = 258 # Dagnummer för 14/9 (160-jubileum)
GOAL_DISTANCE = 32200

def get_week_nr():
    date_today = datetime.date.today()
    week_today = date_today.isocalendar()[1]
    return week_today

def get_stats():
    # Get strava data
    driver = create_new_driver(CLUB_LEAD_URL)
    log_in(driver, CLUB_LEAD_URL)
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

    # Fixa variabler till html-fil
    km_total = 0
    weeks = []
    km_week = []
    real_tot_week = [GOAL_DISTANCE]
    goal_tot_week = [GOAL_DISTANCE]
    for key, value in stats.items():
        km_total += value
        weeks.append(key)
        km_week.append(value)
        goal_tot_week.append(round(GOAL_DISTANCE - int(key)*7/TOTAL_DAYS * GOAL_DISTANCE,2))
        real_tot_week.append(round(real_tot_week[int(key)-1]-value,2))

    time_now = datetime.datetime.now()
    day_nr = time_now.timetuple().tm_yday
    pct_days_past = day_nr/TOTAL_DAYS
    pct_goal_today = round(pct_days_past*100,2)
    pct_total_today = round(km_total/GOAL_DISTANCE*100,2)
    km_goal = round(pct_days_past * GOAL_DISTANCE,2)

    update = time_now.strftime("%Y-%m-%d %H:%M:%S")

    # Skapa dict för html-variabler
    context = {
        "km_total": round(km_total,2),
        "km_goal": round(km_goal,2),
        "pct_total_today": pct_total_today,
        "pct_goal_today": pct_goal_today,
        "line_chart_weeks": ['0']+weeks,
        "week_nr": weeks,
        "km_week": km_week,
        "real_tot_week": real_tot_week,
        "goal_tot_week": goal_tot_week,
        "update": update
    }

    # Sätt ihop html-fil
    template = Environment(loader=FileSystemLoader("./")).get_template("index_temp.html")
    with open('index.html', 'w') as file:
        file.write(template.render(context))

if __name__ == '__main__':
    get_stats()
    write_file()
    

