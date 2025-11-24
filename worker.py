import time
import json
import sqlalchemy.exc 
from database import SessionLocal, Job, init_db
from modules.config_manager import config_manager
from modules.llm_client import LLMClient
from modules.jira_client import JiraClient

def process_job(db: SessionLocal, job: Job):
    print(f"[WORKER] Starting job {job.id}...")
    try:
        job.status = "RUNNING"
        db.commit()

        req_type = job.requirement_type
        
        # --- Prompt Strategy Fallback ---
        prompt_template = config_manager.get_prompt(req_type, job.prompt_strategy)
        if not prompt_template and req_type in ["SRS", "USER_STORIES"]:
            print(f"[WORKER-WARN] Strategy '{job.prompt_strategy}' missing. Fallback to zero-shot.")
            prompt_template = config_manager.get_prompt(req_type, "zero-shot")
            
        if not prompt_template and req_type != "JIRA_SYNC":
            job.status = "FAILED"; db.commit(); return

        # --- A: CLASSIFICATION (Granular Updates) ---
        if req_type in ["FR", "NFR"]:
            reviews = json.loads(job.original_reviews_json)
            results = []
            
            for i, review in enumerate(reviews):
                if not db.query(Job).filter(Job.id == job.id).first(): return
                
                classification = LLMClient.classify_review(review, job.llm_choice, prompt_template)
                results.append(classification)

                # CRITICAL: Update DB after EACH review so frontend progress bar moves smoothly
                job.completed_reviews = i + 1
                job.results_json = json.dumps(results)
                db.commit() 

        # --- B: GENERATION ---
        elif req_type in ["SRS", "USER_STORIES"]:
            try:
                raw = json.loads(job.original_reviews_json)
                combined = raw[0] if isinstance(raw, list) and raw else str(raw)
            except: combined = job.original_reviews_json

            res = LLMClient.generate_text(combined, job.llm_choice, prompt_template)
            job.results_json = json.dumps([res])
            job.completed_reviews = job.total_reviews
            db.commit()

        # --- C: JIRA SYNC (Granular Updates) ---
        elif req_type == "JIRA_SYNC":
            data = json.loads(job.original_reviews_json)
            config = data.get("config", {})
            stories = data.get("stories", [])
            results = []

            for i, story in enumerate(stories):
                if not db.query(Job).filter(Job.id == job.id).first(): return
                
                resp = JiraClient.create_issue(config['domain'], config['email'], config['token'], config['project'], summary=story[:200], description=story)
                results.append(f"Created {resp.get('key')}" if resp.get('success') else "Failed")
                
                job.completed_reviews = i + 1
                job.results_json = json.dumps(results)
                db.commit()
                time.sleep(0.5) # Slow down for Jira API rate limits

        job.status = "COMPLETED"
        db.commit()
        print(f"[WORKER] Job {job.id} COMPLETED.")

    except Exception as e:
        print(f"[WORKER-ERROR] {e}")
        db.rollback()
        try: job.status = "FAILED"; db.commit() 
        except: pass

def main():
    init_db()
    if config_manager.load_config():
        print("[WORKER] Watching...")
        while True:
            db = SessionLocal()
            job = db.query(Job).filter(Job.status == "QUEUED").order_by(Job.id).first()
            if job: process_job(db, job)
            else: time.sleep(1)
            db.close()

if __name__ == "__main__":
    main()