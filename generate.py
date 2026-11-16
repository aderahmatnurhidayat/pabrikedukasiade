import os
import requests
from datetime import datetime
import sys

# Mengambil API key Gemini dari environment GitHub Secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY kosong! Cek kembali GitHub Secrets Anda.")
    sys.exit(1)

# Endpoint resmi Google Gemini API
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

headers = {
    "Content-Type": "application/json"
}

prompt = """
Kamu adalah seorang guru Matematika dan Informatika di MTs (setingkat SMP) yang sangat kreatif, ramah, dan asyik.
Tugasmu adalah membuat 1 materi edukasi singkat atau kuis interaktif (pilih bergantian antara Matematika atau Informatika).
Gunakan analogi dunia nyata yang dekat dengan kehidupan remaja (contoh: game, media sosial, makanan, atau aktivitas sehari-hari).
Bahasanya santai, memotivasi, mudah dipahami anak usia 13-15 tahun, dan tidak kaku.
Sertakan juga 1 pertanyaan latihan seru di akhir materi.
"""

payload = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

try:
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        ai_content = result['candidates'][0]['content']['parts'][0]['text']
        
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"materi_{today}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Materi & Kuis Seru - {today}\n\n")
            f.write(ai_content)
            
        print(f"Berhasil membuat materi: {filename}")
    else:
        print(f"GAGAL terhubung ke Gemini API (Kode {response.status_code}):")
        print(response.text)
        sys.exit(1)

except Exception as e:
    print(f"Terjadi kesalahan sistem:", str(e))
    sys.exit(1)
