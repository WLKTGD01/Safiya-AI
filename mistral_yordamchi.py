from mistralai import Mistral

def mistral_kpt(user):
    api_key='fXEf24hfVLvmIEHRvilwOKN6hPpSET7b'
    model = 'mistral-large-latest'
    client = Mistral(api_key=api_key)
    responce = client.chat.complete(
        model=model,
        messages=[
                {"role": "system", 
                "content": "Your name is Yordamchi AI, you were created by Normurodov Jasur Ibragimovich"
                },
                {"role": "user", 
                "content": user
                }
            ]
        )
    return responce.choices[0].message.content


# print(mistral_kpt('Salom ai'))