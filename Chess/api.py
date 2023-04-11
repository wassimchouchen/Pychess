import requests
import json
import openai
from transformers import GPT2Tokenizer, GPT2LMHeadModel
openai.api_key = "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" #api key
# My hugging_face API key
headers = {"Authorization": "Bearer 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"} #header of hugging face 


def ASR_WHISPER(payload) :
        """
        this is the api for Whisper openai ASR pretrained model, it consiste of transcribe audio to text what ever the quality of the record
        """
        file = open(payload, "rb")
        response = openai.Audio.transcribe("whisper-1", file)
        return (response["text"]) 

trans_url = "https://api-inference.huggingface.co/models/openai/whisper-tiny"
def transcription(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(trans_url, headers=headers, data=data)
    return response.json()



autotext_url = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
def GPT(payload) :
    """
    this is the api for GPT model, it consiste of text generation 
    """
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=json.dumps(payload),
    max_tokens=4000,
    temperature=0.2,)
    return (response["choices"][0]["text"]) 

def GPT35(payload) :
        """
        this is the api for GPT3.5 model, its an upgrade model for regulat GPT3, trained on more corpus and tuned better
        """
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content":payload }])
        return (response["choices"][0]["message"]["content"]) 



def text_to_audio(payload):
        print("first")
        response = requests.post(autotext_url, headers=headers, json=payload)
        print("second")
        return response.json()