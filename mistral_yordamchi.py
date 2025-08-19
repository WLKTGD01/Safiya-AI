# Synchronous Example
from mistralai import Mistral

def mistral_kpt(user):
    with Mistral(
        api_key='fXEf24hfVLvmIEHRvilwOKN6hPpSET7b',
    ) as mistral:

        res = mistral.chat.complete(model="mistral-small-latest", messages=[
            {
                "content": user,
                "role": "user",
            },
        ], stream=False)

    # Handle response
        return res
