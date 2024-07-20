# chat/views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from openai import OpenAI
import time
import markdown2
import re
from .models import QnA
import os
from datetime import datetime
import locale
import random
from django.shortcuts import render

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def chat(request):
    response_message = ""
    user_input = ""

    thread_id = request.session.get("thread_id")

    if request.method == "POST":
        user_input = request.POST.get("user_input")
        print("user_input: ", user_input)
        date_string = f"Heutiges Datum: {datetime.now().strftime('%A, %d. %B %Y, %H:%M')}"

        # Create an Assistant
        noeldekegpt = client.beta.assistants.retrieve("asst_aXieuBEQXmx4yovAGO7VYzxL")

        if not thread_id:
            # Create a new thread if none exists
            my_thread = client.beta.threads.create()
            thread_id = my_thread.id
            request.session["thread_id"] = thread_id
        else:
            # Use the existing thread
            my_thread = client.beta.threads.retrieve(thread_id=thread_id)

        # Add a Message to a Thread
        client.beta.threads.messages.create(
            thread_id=my_thread.id,
            role="user",
            content=date_string + user_input,
        )

        # Run the Assistant
        my_run = client.beta.threads.runs.create(
            thread_id=my_thread.id,
            assistant_id=noeldekegpt.id,
        )

        # Check the status of the run
        while my_run.status in ["queued", "in_progress"]:
            my_run = client.beta.threads.runs.retrieve(
                thread_id=my_thread.id, run_id=my_run.id
            )
            time.sleep(0.5)  # A brief pause to prevent rapid polling

            if my_run.status == "completed":
                # Retrieve the Messages added by the Assistant to the Thread
                all_messages = client.beta.threads.messages.list(thread_id=my_thread.id)
                response_message = all_messages.data[0].content[0].text.value
                # Get rid of square brackets (Quellen)
                response_message = re.sub(r"\【.*?\】", "", response_message)
                # Markdown -> HTML
                response_message = markdown2.markdown(response_message)

                # Save the QnA record
                qna_record = QnA(question=user_input, answer=response_message)
                qna_record.save()

                print(f"{response_message = }")
                break

        return JsonResponse({"message": response_message})

    # Retrieve all past QnA records
    past_questions = QnA.objects.all().order_by("-timestamp")
    return render(
        request,
        "chat.html",
        {
            "user_input": user_input,
            "response": response_message,
            "past_questions": past_questions,
        },
    )

def daily_fundorte(request):
    # Set the locale to German
    locale.setlocale(locale.LC_TIME, "de_DE")
    with open(
        os.path.join(settings.BASE_DIR, "chat", "data", "woist.tsv"), "r"
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
        os.path.join(settings.BASE_DIR, "chat", "data", "milch_daten_2024.txt"), "r"
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

def map(request):
    return render(request, 'map.html')