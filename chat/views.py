from django.shortcuts import render
from django.conf import settings
from openai import OpenAI
import time
import markdown2
import re
from .models import QnA


client = OpenAI(api_key=settings.OPENAI_API_KEY)

def index(request):
    response_message = ""
    user_input = ""

    thread_id = request.session.get('thread_id')

    if request.method == "POST":
        user_input = request.POST.get('user_input')
        print("user_input: ", user_input)

        # Create an Assistant
        noeldekegpt = client.beta.assistants.retrieve("asst_aXieuBEQXmx4yovAGO7VYzxL")


        if not thread_id:
            # Create a new thread if none exists
            my_thread = client.beta.threads.create()
            thread_id = my_thread.id
            request.session['thread_id'] = thread_id
        else:
            # Use the existing thread
            my_thread = client.beta.threads.retrieve(thread_id=thread_id)


        # Add a Message to a Thread
        client.beta.threads.messages.create(
            thread_id=my_thread.id,
            role="user",
            content=user_input,
        )

        # Run the Assistant
        my_run = client.beta.threads.runs.create(
            thread_id=my_thread.id,
            assistant_id=noeldekegpt.id,
        )

        # Check the status of the run
        while my_run.status in ["queued", "in_progress"]:
            my_run = client.beta.threads.runs.retrieve(
                thread_id=my_thread.id,
                run_id=my_run.id
            )
            time.sleep(0.5)  # A brief pause to prevent rapid polling

            if my_run.status == "completed":
                # Retrieve the Messages added by the Assistant to the Thread
                all_messages = client.beta.threads.messages.list(thread_id=my_thread.id)
                response_message = all_messages.data[0].content[0].text.value
                # Get rid of square brackets (Quellen)
                response_message = re.sub(r'\【.*?\】', '', response_message)
                # Markdown -> HTML
                response_message = markdown2.markdown(response_message)
                
                # Speichern der Frage und Antwort
                qna_record = QnA(question=user_input, answer=response_message)
                qna_record.save()
                
                print(f'{response_message = }')
                break
        # response_message = "answer"


    # Abrufen aller vergangenen QnA-Datensätze
    past_questions = QnA.objects.all().order_by('-timestamp')  # Neueste zuerst
    return render(request, 'chat/index.html', {
        'user_input': user_input,
        'response': response_message,
        'past_questions': past_questions,
        })
