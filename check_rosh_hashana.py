import json
from datetime import datetime
from convertdate import hebrew

# ---- CONFIG ----
INPUT_FILE = 'apocalyptic_events.json'  # adjust path to your file
TOLERANCE_DAYS = 2  # number of days around Rosh Hashanah to allow

# ---- FUNCTIONS ----
def rosh_hashanah_for_year(year):
    """Return datetime of Rosh Hashanah (1 Tishrei) for the given Gregorian year."""
#    hebrew_year = year + 3760  # Hebrew year offset
#    gdate = hebrew.to_gregorian(hebrew_year, 7, 1)  # Tishrei=7
#    return datetime(*gdate)
    goldenNumber = (year % 19) + 1
    

# ---- MAIN ----
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = []
for item in data:
    try:
        event_date = datetime.fromisoformat(item['date'])
    except Exception:
        continue

    rh_date = rosh_hashanah_for_year(event_date.year)
    diff_days = abs((event_date - rh_date).days)
    print ("RH date: " + rh_date.strftime("%B %d, %Y") + ", event date: " + event_date.strftime("%B %d, %Y") + ", " + str(diff_days) + " day(s)\n")
    if diff_days <= TOLERANCE_DAYS:
        matches.append({
            'event_date': event_date.strftime('%Y-%m-%d'),
            'claimants': item['claimants'],
            'rosh_hashanah': rh_date.strftime('%Y-%m-%d'),
            'days_diff': diff_days,
            'description': item['description'][:80] + '...'
        })

# ---- OUTPUT ----
print(f"Events within ±{TOLERANCE_DAYS} days of Rosh Hashanah:")
for m in matches:
    print(f"{m['event_date']} (RH: {m['rosh_hashanah']}, diff {m['days_diff']} days) "
          f"- {m['claimants']} | {m['description']}")
