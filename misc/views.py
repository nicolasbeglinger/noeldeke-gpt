from django.shortcuts import render
import os
import locale
import random
from django.conf import settings
from datetime import datetime

def starting_page(request):
    return render(request, "starting_page.html")

def daily_fundorte(request):
    # Set the locale to German
    locale.setlocale(locale.LC_TIME, "de_DE")
    with open(
        os.path.join(settings.BASE_DIR, "misc", "data", "woist.tsv"), "r"
    ) as f:
        data = f.readlines()
        new_list = []
        for line in data:
            line = line.strip()
            if not "\t" in line:
                line += "\tNA"

            new_list.append(line.split("\t"))
    
    date_time_str = datetime.now().strftime("%Y%m%d")
    date_time_int = int(date_time_str)

    random.seed(date_time_int)
    random.shuffle(new_list)



    return render(
        request,
        "daily_fundorte.html",
        {"fundorte": new_list[:5]})


def milchkalender(request):
    # Set the locale to German
    locale.setlocale(locale.LC_TIME, "de_DE")

    with open(
        os.path.join(settings.BASE_DIR, "misc", "data", "milch_daten_2024.txt"), "r"
    ) as f:
        data = f.readlines()[1:]
        data = [d.strip() for d in data]

    future_milk_dates = []
    # Compare dates
    for date_str in data:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.date() > datetime.now().date():
            future_milk_dates.append(date_obj.date().strftime("%A, %d. %B %Y"))

    current_date = datetime.now().strftime("%A, %d. %B %Y")

    return render(
        request,
        "milchkalender.html",
        {"future_milk_dates": future_milk_dates[:5], "current_date": current_date},
    )
