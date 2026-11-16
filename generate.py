import os
import requests
from datetime import datetime
import sys

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY kosong! Cek kembali GitHub Secrets kamu.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

prompt = """
Kamu adalah seorang guru Matematika dan Informatika di MTs (setingkat SMP) yang sangat kreatif, ramah, dan asyik.
Tugasmu adalah membuat 1 materi edukasi singkat atau kuis interaktif (pilih bergantian antara Matematika atau Informatika).
Gunakan analogi dunia nyata yang dekat dengan kehidupan remaja (contoh: game, media sosial, makanan, atau aktivitas sehari-hari).
Bahasanya santai, memotivasi, mudah dipahami anak usia 13-15 tahun, dan tidak kaku.
Sertakan juga 1 pertanyaan latihan seru di akhir materi.
"""

# Menggunakan model standar Groq yang stabil dan aktif
payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": "Kamu adalah asisten kurikulum guru yang kreatif."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.8
}

response = requests.post(API_URL, json=payload, headers=headers)

if response.status_code == 200:
    result = response.json()
    ai_content = result['choices'][0]['message']['content']
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"materi_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Materi & Kuis Seru - {today}\n\n")
        f.write(ai_content)
        
    print(f"Berhasil membuat materi: {filename}")
else:
    print(f"GAGAL menghubungi Groq API (Kode {response.status_code}):")
    print(response.text)
    sys.exit(1)
