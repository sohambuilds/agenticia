from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import router
from utils import setup_logging
import logging

# Setup logging first
setup_logging()
logger = logging.getLogger("main")

app = FastAPI(
    title="AI Tutor Multi-Agent System",
    description="A multi-agent tutoring system with specialized agents for different subjects",
    version="1.0.0"
)

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
    logger.info("Root endpoint accessed")
    return {"message": "AI Tutor Multi-Agent System API", "status": "operational"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "ai-tutor-backend"}

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("🚀 AI Tutor Multi-Agent System starting up...")
    logger.info("✅ Agents: TutorAgent, MathAgent, PhysicsAgent")
    logger.info("✅ Tools: CalculatorTool, PhysicsConstantsTool")
    logger.info("✅ API endpoints: /api/chat, /api/agents, /api/health")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("🛑 AI Tutor Multi-Agent System shutting down...")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 