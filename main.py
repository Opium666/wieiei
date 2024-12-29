from fastapi import FastAPI
from pixai import PixaiAPI
from fastapi import FastAPI
from pixai import PixaiAPI
from fastapi.responses import JSONResponse

app = FastAPI()

client = PixaiAPI('eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJsZ2EiOjE3MzU0NjMwMzYsImlhdCI6MTczNTQ2MzA0MywiZXhwIjoxNzM2MDY3ODQzLCJpc3MiOiJwaXhhaSIsInN1YiI6IjE2MjA1NDA2NTgyMzgwNzkxODkiLCJqdGkiOiIxODMwMDMxOTYxMTI4NTU2MDI5In0.Aa9dZu-KMH16UXsYJA6D0VBQelBTqb8QRh69uTRfa9Sro3rQtzIvAqtFUTSRMnOVcf47hs-JlMBxPpEQNJ7U-9P0AN7HgU3VCi9hI-hbN0o2NV8EU7x3ijhiGPhaa1W1hSKCMZS_DjgkvsDTETtZF1D74-sQaqrQ8mHovgw3XgRVRXpT')

@app.get("/pixai")
async def generate_image(prompt: str):
    startGeneration = client.createGenerationTask(
        prompts=prompt,
        steps='28',
        modelId='1607921862771379570'
    )

    if startGeneration is None:
        return JSONResponse(status_code=500, content={"error": "Failed to create generation task."})
    
    imageurl = client.getTaskById(startGeneration)

    if not imageurl:
        return JSONResponse(status_code=500, content={"error": "Failed to retrieve image."})
    
    return {"image_url": imageurl}
