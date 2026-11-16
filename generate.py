import os
from datetime import datetime
import sys
from groq import Groq

# Mengambil API key dari environment GitHub Secrets
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY kosong! Cek kembali GitHub Secrets Anda.")
    sys.exit(1)

# Inisialisasi client resmi Groq
client = Groq(api_key=api_key)

prompt = """
Kamu adalah seorang guru Matematika dan Informatika di MTs (setingkat SMP) yang sangat kreatif, ramah, dan asyik.
Tugasmu adalah membuat 1 materi edukasi singkat atau kuis interaktif (pilih bergantian antara Matematika atau Informatika).
Gunakan analogi dunia nyata yang dekat dengan kehidupan remaja (contoh: game, media sosial, makanan, atau aktivitas sehari-hari).
Bahasanya santai, memotivasi, mudah dipahami anak usia 13-15 tahun, dan tidak kaku.
Sertakan juga 1 pertanyaan latihan seru di akhir materi.
"""

try:
    # Menggunakan model standar Groq yang paling diandalkan saat ini
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Kamu adalah asisten kurikulum guru yang kreatif."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )
    
    ai_content = completion.choices[0].message.content
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"materi_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Materi & Kuis Seru - {today}\n\n")
        f.write(ai_content)
        
    print(f"Berhasil membuat materi: {filename}")

except Exception as e:
    print(f"GAGAL terhubung ke Groq:", str(e))
    sys.exit(1)
