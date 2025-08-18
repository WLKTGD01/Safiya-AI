import json
import requests

# API kalitlar faylini o'qish
def load_keys(filename="api_keys.json"):
    with open(filename, "r") as f:
        return json.load(f)

# API kalitlar faylini yangilash
def save_keys(data, filename="api_keys.json"):
    with open(filename, "w") as f:
        json.dump(data, f)

# Hozirgi kalitni olish
def get_current_key():
    data = load_keys()
    return data["api_keys"][data["current_index"]], data

# Keyingi kalitga o'tish
def switch_to_next_key(data):
    data["current_index"] = (data["current_index"] + 1) % len(data["api_keys"])
    save_keys(data)
    return data["api_keys"][data["current_index"]]

# API chaqiruv funksiyasi
def query_mistral(prompt):
    key, data = get_current_key()
    headers = {"Authorization": f"Bearer {key}"}
    payload = {
        "model": "mistral-small",  # yoki boshqa model nomi
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    # Kalit noto'g'ri bo'lsa - avtomatik almashtirish
    if response.status_code in [401, 403]:
        print("⚠️ API kaliti eskirgan. Yangi kalitga o'tmoqdaman...")
        new_key = switch_to_next_key(data)
        headers["Authorization"] = f"Bearer {new_key}"
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload
        )

    if response.ok:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Xatolik: {response.status_code} - {response.text}"

# Foydalanish:
javob = query_mistral("Assalomu alaykum, siz kim siz?")
print(javob)
