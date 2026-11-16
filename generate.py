import os
from datetime import datetime
import sys
from google import genai

# Mengambil API key Gemini dari environment GitHub Secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY kosong! Cek kembali GitHub Secrets Anda.")
    sys.exit(1)

# Inisialisasi client resmi Google GenAI
client = genai.Client(api_key=api_key)

prompt = """
Kamu adalah seorang guru Matematika dan Informatika di MTs (setingkat SMP) yang sangat kreatif, ramah, dan asyik.
Tugasmu adalah membuat 1 materi edukasi singkat atau kuis interaktif (pilih bergantian antara Matematika atau Informatika).
Gunakan analogi dunia nyata yang dekat dengan kehidupan remaja (contoh: game, media sosial, makanan, atau aktivitas sehari-hari).
Bahasanya santai, memotivasi, mudah dipahami anak usia 13-15 tahun, dan tidak kaku.
Sertakan juga 1 pertanyaan latihan seru di akhir materi.
"""

try:
    # Menggunakan model standar yang paling stabil
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    ai_content = response.text
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"materi_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Materi & Kuis Seru - {today}\n\n")
        f.write(ai_content)
        
    print(f"Berhasil membuat materi: {filename}")

except Exception as e:
    print(f"GAGAL terhubung ke Gemini API:", str(e))
    sys.exit(1)
