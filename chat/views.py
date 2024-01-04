from django.shortcuts import render
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def index(request):
    response_message = ""
    user_input = ""
    
    # Read the handbook file
    with open('chat/handbuch.txt', 'r') as file:
        handbuch = file.read()
    
    with open('chat/rules.txt', 'r') as file:
        rules = file.read()

    if request.method == "POST":
        user_input = request.POST.get('user_input')

        # Combining handbook context with user input
        combined_input = rules + "\n\n" + handbuch + "\n\nQuery:\n" + user_input

        try:
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages = [
                    {'role': 'user', 'content': combined_input}
                ],
                temperature = 0  )
            response_message = completion.choices[0].message.content

        except Exception as e:
            response_message = f"An error occurred: {str(e)}"

    return render(request, 'chat/index.html', {'user_input': user_input, 'response': response_message})