# chat/views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from openai import OpenAI
import time
import markdown2
import re
from .models import QnA
from datetime import datetime
from django.shortcuts import render

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def chat(request):
    response_message = ""
    user_input = ""

    thread_id = request.session.get("thread_id")

    if request.method == "POST":
        user_input = request.POST.get("user_input")
        save_flag = request.POST.get("save_flag")

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

            status = my_run.status
            match status:
                case "failed":
                    raise Warning(my_run)

                case "completed":
                    # Retrieve the Messages added by the Assistant to the Thread
                    all_messages = client.beta.threads.messages.list(thread_id=my_thread.id)
                    response_message = all_messages.data[0].content[0].text.value
                    # Get rid of square brackets (Quellen)
                    response_message = re.sub(r"\【.*?\】", "", response_message)
                    # Markdown -> HTML
                    response_message = markdown2.markdown(response_message)

                    if save_flag == "save":
                        # Save the QnA record
                        qna_record = QnA(question=user_input, answer=response_message)
                        qna_record.save()

                    print(f"{response_message = }")
                    break

                case _:
                    continue

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
