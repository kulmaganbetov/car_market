from django.shortcuts import render
from shop.models import Product
from contact.forms import SubscriberForm
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home_page(request):
    products = Product.objects.all()[:8]
    forms = SubscriberForm()
    if request.method == 'POST':
        forms = SubscriberForm(request.POST)
        if forms.is_valid():
            forms.save()
    context = {
        'products': products,
        'forms': forms
    }
    return render(request, 'home.html', context)



openai.api_key = "OPENAI_API_KEY"

@csrf_exempt
def ask_ai(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты автомобильный эксперт. Ты отвечаешь **только** на вопросы, связанные с машинами "
                        "(марки, модели, характеристики, сравнение, советы и т.д.). "
                        "Если вопрос не связан с машинами — откажись вежливо и скажи, что отвечаешь только про автомобили. "
                        "Также ты всегда указываешь фейковую цену автомобиля в тенге. Пример: 'Эта модель стоит около 7 500 000 ₸'."
                    )
                },
                {"role": "user", "content": question}
            ]
        )

        answer = response['choices'][0]['message']['content']
        return JsonResponse({'answer': answer})
