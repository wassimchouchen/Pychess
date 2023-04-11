import tempfile
from Chess import api
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
import requests
import os
import random





@csrf_exempt
def GPT(request):
    """
    this function execute the gpt3 api
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        response = api.GPT(text)
        return HttpResponse(response)
    
@csrf_exempt
def GPT_turbo(request):
    """
    this function execute the gpt35 api
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        response = api.GPT35(text)
        return HttpResponse(response)
    
    
@csrf_exempt
def transcribe_v1(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        with open('record.wav', 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        result = api.ASR_WHISPER('record.wav')
        return JsonResponse({'result': result})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def transcribe_v2(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        with open('record.wav', 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        result = api.transcription('record.wav')
        return JsonResponse({'result': result})
    return JsonResponse({'error': 'Invalid request method'})




autotext_url = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
headers = {"Authorization": "Bearer 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"}
@csrf_exempt
def text_to_audio_vieww(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get("txt", "")
        payload = {"inputs": text}
        response = requests.post(autotext_url, headers=headers, json=payload)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(response.content)
            filename = f.name
        with open(filename, 'rb') as f:
            audio_content = f.read()
        os.unlink(filename)
        return HttpResponse(audio_content, content_type='audio/wav')
    
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def audio_to_audio(request):
    """
    this function took the user audio, it transcibe it throw asr model, them the transcription go throw the GPT model, then the response of 
    the LLM go to "text_to_audio" to produce audio response model so the response to the user become audio
    """
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        with open('record.wav', 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        user_t = api.ASR_WHISPER('record.wav')
        t_response = api.GPT(user_t)
        payload = {"inputs": t_response}
        response = requests.post(autotext_url, headers=headers, json=payload)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(response.content)
            filename = f.name
        with open(filename, 'rb') as f:
            audio_content = f.read()
        os.unlink(filename)
        return HttpResponse(audio_content, content_type='audio/wav')
    
    return JsonResponse({'error': 'Invalid request method'})




with open("quiz.json") as f:
    quiz_data = json.load(f)

random.shuffle(quiz_data)
current_question_index = 0

@csrf_exempt
def send_question(request):
    """
    Send a quiz question to the frontend.
    """
    global current_question_index
    if request.method == "GET":
        if current_question_index < len(quiz_data):
            question = quiz_data[current_question_index]["question"]
            options = quiz_data[current_question_index]["options"]
            current_question_index += 1
            response_data = {
                "question": question,
                "options": options
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse("", content_type="application/json")
    else:
        return HttpResponse(status=405)

@csrf_exempt
def check_answer(request):
    """
    Verify if the submitted answer is correct and return the result.
    """
    if request.method == "POST":
        answer = request.POST.get("answer")
        if current_question_index > 0 and current_question_index <= len(quiz_data):
            correct_answer = quiz_data[current_question_index - 1]["answer"]
            result = (answer == correct_answer)
            response_data = {
                "result": result
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse("", content_type="application/json")
    else:
        return HttpResponse(status=405)