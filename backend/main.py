from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import router

app = FastAPI(
    title="AI Tutor Multi-Agent System",
    description="A multi-agent tutoring system with specialized agents for different subjects",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Tutor Multi-Agent System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-tutor-backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 