from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import template, chain  # Import from your existing chatbot.py

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlotRequest(BaseModel):
    variable1: str  # cameo_char
    variable2: str  # new_loc
    variable3: str  # new_event

@app.post("/generate-plot")
async def generate_plot(request: PlotRequest):
    try:
        variables = {
            "cameo_char": request.variable1,
            "new_loc": request.variable2,
            "new_event": request.variable3,
        }
        
        result = chain.invoke(variables)
        return {"plot": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)