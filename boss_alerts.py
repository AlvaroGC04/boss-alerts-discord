import time
import datetime
import pytz
import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("No se encontró la variable de entorno DISCORD_WEBHOOK_URL")

# Lista de jefes a notificar
BOSSES = ["Sangoon", "Uturi", "Bulgasal", "Golden Pig King"]

# Zona horaria Colombia
tz_cot = pytz.timezone("America/Bogota")

# Horarios de los jefes por región y día (COT)
boss_schedule = {
    "NA": {
        "Mon": ["14:00 Golden Pig King", "16:00 Offin Tett", "16:00 Golden Pig King Sangoon",
                "20:15 Golden Pig King Sangoon", "21:00 Bulgasal Uturi"],
        "Tue": ["14:00 Uturi", "16:00 Golden Pig King Sangoon", "20:15 Bulgasal Uturi", "21:00 Golden Pig King Sangoon"],
        "Wed": ["14:00 Sangoon", "16:00 Bulgasal Uturi", "20:15 Golden Pig King Sangoon", "21:00 Bulgasal Uturi"],
        "Thu": ["14:00 Bulgasal", "16:00 Golden Pig King Sangoon", "20:15 Bulgasal Uturi", "21:00 Golden Pig King Uturi"],
        "Fri": ["14:00 Golden Pig King", "16:00 Sangoon Uturi", "20:15 Golden Pig King Bulgasal", "21:00 Bulgasal Uturi"],
        "Sat": ["14:00 Sangoon Bulgasal", "16:00 -"],
        "Sun": ["14:00 Golden Pig King Bulgasal", "16:00 Sangoon Uturi"]
    },
    "EU": {
        "Mon": ["15:00 Golden Pig King", "17:00 Offin Tett", "21:15 Golden Pig King Sangoon", "22:00 Bulgasal Uturi"],
        "Tue": ["15:00 Uturi", "17:00 Golden Pig King Sangoon", "21:15 Bulgasal Uturi", "22:00 Golden Pig King Sangoon"],
        "Wed": ["15:00 Sangoon", "17:00 Bulgasal Uturi", "21:15 Golden Pig King Sangoon", "22:00 Bulgasal Uturi"],
        "Thu": ["15:00 Bulgasal", "17:00 Golden Pig King Sangoon", "21:15 Bulgasal Uturi", "22:00 Golden Pig King Uturi"],
        "Fri": ["15:00 Golden Pig King", "17:00 Sangoon Uturi", "21:15 Golden Pig King Bulgasal", "22:00 Bulgasal Uturi"],
        "Sat": ["15:00 Sangoon Bulgasal"],
        "Sun": ["15:00 Golden Pig King Bulgasal", "17:00 Sangoon Uturi"]
    },
    "ASIA": {
        "Mon": ["10:30 Bulgasal", "06:00 Sangoon Bulgasal", "09:30 Golden Pig King Sangoon"],
        "Tue": ["10:30 Sangoon", "06:00 Golden Pig King Uturi", "09:30 Bulgasal Uturi"],
        "Wed": ["10:30 Golden Pig King", "06:00 Uturi", "09:30 Golden Pig King Sangoon"],
        "Thu": ["10:30 Uturi", "06:00 Sangoon Golden Pig King", "09:30 Bulgasal Uturi"],
        "Fri": ["10:30 Sangoon", "06:00 Golden Pig King Bulgasal", "09:30 Golden Pig King Bulgasal"],
        "Sat": ["10:30 Bulgasal", "06:00 Uturi"],
        "Sun": ["10:30 Golden Pig King", "06:00 Golden Pig King Sangoon", "09:30 Golden Pig King Sangoon"]
    }
}

def send_discord_message(region, boss_name, spawn_time):
    message = f"⏰ **{region}**: {boss_name} spawnea a las {spawn_time} (COT) — ¡Faltan 5 minutos!"
    payload = {"content": message}
    requests.post(WEBHOOK_URL, json=payload)

while True:
    now = datetime.datetime.now(tz_cot)
    current_day = now.strftime("%a")
    current_time = now.strftime("%H:%M")

    for region, schedule in boss_schedule.items():
        if current_day in schedule:
            for event in schedule[current_day]:
                try:
                    spawn_time, *bosses = event.split()
                    spawn_dt = datetime.datetime.strptime(spawn_time, "%H:%M").replace(
                        year=now.year, month=now.month, day=now.day, tzinfo=tz_cot
                    )
                    if 0 <= (spawn_dt - now).total_seconds() <= 300:  # 5 minutos antes de su spawn original
                        for boss in bosses:
                            if boss in BOSSES:
                                send_discord_message(region, boss, spawn_time)
                except ValueError:
                    continue

    time.sleep(60)
