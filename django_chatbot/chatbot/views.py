from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize conversation history with a system message
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def home(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        res = ask_openai(message)
        return JsonResponse({'message':message, 'response':res })
    return render(request,"chatbot/chatbot.html")


def ask_openai(user_message):    
    conversation_history.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    conversation_history.append({"role": "assistant", "content": response.choices[0].message['content']})
    print(conversation_history)
    return response.choices[0].message['content']
