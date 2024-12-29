from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pixai import PixaiAPI
import time

# Membuat instance FastAPI
app = FastAPI()

# Menambahkan API Pixai
client = PixaiAPI('eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJsZ2EiOjE3MzU0NjMwMzYsImlhdCI6MTczNTQ2MzA0MywiZXhwIjoxNzM2MDY3ODQzLCJpc3MiOiJwaXhhaSIsInN1YiI6IjE2MjA1NDA2NTgyMzgwNzkxODkiLCJqdGkiOiIxODMwMDMxOTYxMTI4NTU2MDI5In0.Aa9dZu-KMH16UXsYJA6D0VBQelBTqb8QRh69uTRfa9Sro3rQtzIvAqtFUTSRMnOVcf47hs-JlMBxPpEQNJ7U-9P0AN7HgU3VCi9hI-hbN0o2NV8EU7x3ijhiGPhaa1W1hSKCMZS_DjgkvsDTETtZF1D74-sQaqrQ8mHovgw3XgRVRXpT')

@app.get("/")
async def home(request: Request):
    return {"message": "Welcome to PixAi!"}

@app.get("/pixai")
async def generate_image(request: Request, prompt: str = ""):
    if not prompt:
        return JSONResponse(content={"error": "Prompt tidak boleh kosong"}, status_code=400)

    try:
        # Membuat tugas generasi gambar
        startGeneration = client.createGenerationTask(
            prompts=prompt,
            steps='20',
            modelId='1648918127446573124'
        )

        if not startGeneration:
            return JSONResponse(content={"error": "Gagal membuat tugas, respons kosong"}, status_code=500)

        print("Start Generation Response:", startGeneration)

        # Mendapatkan status tugas berdasarkan ID
        time.sleep(5)  # Menunggu beberapa detik agar tugas diproses
        taskStatus = client.getTaskById(startGeneration)

        print("Task Status:", taskStatus)

        if not taskStatus or "http" not in taskStatus:
            return JSONResponse(content={"error": "Gagal mendapatkan URL gambar."}, status_code=500)

        image_url = taskStatus
        print("Image URL:", image_url)

        return JSONResponse(content={"image_url": image_url})

    except Exception as e:
        return JSONResponse(content={"error": f"Terjadi kesalahan: {str(e)}"}, status_code=500)
