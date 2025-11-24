import uvicorn
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal, Job, init_db
from modules.config_manager import config_manager

# --- Models ---
class SubmitJobRequest(BaseModel):
    reviews: List[str]
    requirement_type: str
    llm_choice: str
    prompt_strategy: str

class GenerateRequest(BaseModel):
    reviews_input: str 
    llm_choice: str
    prompt_strategy: str

class JiraSyncRequest(BaseModel):
    stories: List[str]
    jira_domain: str
    jira_email: str
    jira_token: str
    project_key: str

# --- App Setup ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# SERVE FRONTEND FILES
if os.path.exists("frontend"):
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def read_index():
    return FileResponse("review_classifier.html")

@app.on_event("startup")
def startup_event():
    init_db()
    config_manager.load_config()

# --- Endpoints ---
@app.get("/config_options")
async def get_config():
    if not config_manager.loaded: raise HTTPException(503, "Config not loaded")
    return {
        "llm_options": list(config_manager.llm_map.keys()),
        "fr_strategies": list(config_manager.prompts["FR"].keys()),
        "nfr_strategies": list(config_manager.prompts["NFR"].keys()),
        "srs_strategies": list(config_manager.prompts["SRS"].keys()),
        "user_story_strategies": list(config_manager.prompts["USER_STORIES"].keys())
    }

@app.post("/submit_job")
async def submit_job(req: SubmitJobRequest):
    db = SessionLocal()
    db.query(Job).delete()
    job = Job(total_reviews=len(req.reviews), original_reviews_json=json.dumps(req.reviews), requirement_type=req.requirement_type, llm_choice=config_manager.get_backend_llm(req.llm_choice), prompt_strategy=req.prompt_strategy)
    db.add(job); db.commit(); db.refresh(job); db.close()
    return {"job_id": job.id, "status": job.status, "total_reviews": job.total_reviews}

@app.post("/generate_srs")
async def generate_srs(req: GenerateRequest):
    db = SessionLocal()
    job = Job(total_reviews=1, original_reviews_json=json.dumps([req.reviews_input]), requirement_type="SRS", llm_choice=config_manager.get_backend_llm(req.llm_choice), prompt_strategy=req.prompt_strategy)
    db.add(job); db.commit(); db.refresh(job); db.close()
    return {"job_id": job.id, "status": job.status}

@app.post("/generate_user_stories")
async def generate_us(req: GenerateRequest):
    db = SessionLocal()
    job = Job(total_reviews=1, original_reviews_json=json.dumps([req.reviews_input]), requirement_type="USER_STORIES", llm_choice=config_manager.get_backend_llm(req.llm_choice), prompt_strategy=req.prompt_strategy)
    db.add(job); db.commit(); db.refresh(job); db.close()
    return {"job_id": job.id, "status": job.status}

@app.post("/sync_jira")
async def sync_jira(req: JiraSyncRequest):
    db = SessionLocal()
    payload = {"config": {"domain": req.jira_domain, "email": req.jira_email, "token": req.jira_token, "project": req.project_key}, "stories": req.stories}
    job = Job(total_reviews=len(req.stories), original_reviews_json=json.dumps(payload), requirement_type="JIRA_SYNC", llm_choice="N/A", prompt_strategy="N/A")
    db.add(job); db.commit(); db.refresh(job); db.close()
    return {"job_id": job.id, "status": job.status, "total_reviews": len(req.stories)}

@app.post("/cancel_job")
async def cancel():
    db = SessionLocal(); db.query(Job).delete(); db.commit(); db.close()
    return {"msg": "Cancelled"}

@app.get("/check_status")
async def check_status(job_id: int):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()
    if not job: raise HTTPException(404, "Job not found")
    
    orig, res = [], []
    if job.status in ["COMPLETED", "RUNNING"]:
        try:
            if job.requirement_type == "JIRA_SYNC": orig = json.loads(job.original_reviews_json).get("stories", [])
            elif job.original_reviews_json: orig = json.loads(job.original_reviews_json)
            if job.results_json: res = json.loads(job.results_json)
        except: pass
        
    return {"job_id": job.id, "status": job.status, "completed": job.completed_reviews, "total": job.total_reviews, "original_reviews": orig, "results": res}

if __name__ == "__main__":
    print("Starting Server on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)