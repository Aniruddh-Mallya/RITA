# Experiment Replication Guide

This document provides step-by-step instructions to replicate the Requirement Classification and Generation experiment using the provided dataset.

## 1. Environment Setup

### A. Install Prerequisites

Ensure you have the following installed:

1. **Python 3.8 or higher**
2. **Ollama** (Download from [ollama.com](https://ollama.com))

### B. Prepare the LLM

Open your terminal and pull the model used in this experiment (e.g., Mistral):

```bash
ollama pull mistral
ollama serve
```

Keep this terminal window open to run the LLM server.

### C. Application Startup

1. Open a new terminal in the project folder and install python dependencies:

```bash
pip install fastapi uvicorn sqlalchemy requests
```

2. Start the API Server:

```bash
python api.py
```

3. Open a third terminal window and start the Worker Process:

```bash
python worker.py
```

4. Open your web browser and go to: `http://localhost:8001/`

## 2. Replication Steps

### Experiment 1: Functional Requirement (FR) Classification

**Goal:** Classify raw user reviews into Feature Requests or Bugs.

1. **Input Data:** Locate the file `inputs/functional_reviews.txt` in this repository.
2. **UI Action:**
   - On the main screen, click the "Functional (FR)" button.
   - **LLM Choice:** Select `mistral` (or your target model).
   - **Strategy:** Select `zero-shot`.
   - **Upload:** Drag and drop `inputs/functional_reviews.txt`.
   - Click "Process Reviews".
3. **Observation:** Watch the logs at the bottom of the screen. You will see the system processing reviews one by one.
4. **Result:** A table will appear showing the raw review and the predicted label (e.g., "Bug", "Feature").

### Experiment 2: Non-Functional Requirement (NFR) Classification

**Goal:** Classify reviews into Performance, Usability, Security, etc.

1. **Input Data:** Locate the file `inputs/nfr_dataset.xlsx` in this repository.
2. **UI Action:**
   - Click "Start Over" or refresh the page.
   - Click the "Non-Functional (NFR)" button.
   - **LLM Choice:** Select `mistral`.
   - **Strategy:** Select `role-based`.
   - **Upload:** Drag and drop `inputs/nfr_dataset.xlsx`.
   - **Column Selection:** Select the column containing the review text (e.g., "Review_Text") from the dropdown.
   - Click "Process Reviews".
3. **Result:** The table will display NFR categories (e.g., "Performance", "Usability").

### Experiment 3: User Story Generation & Jira Sync

**Goal:** Convert classified reviews into agile user stories and push to Jira.

1. **Prerequisite:** Complete Experiment 1 or 2 so you have classified results on screen.
2. **Generation:**
   - Click the "Generate Stories" button.
   - Confirm the prompt. The system will generate a list of formatted user stories (e.g., "As a user, I want...").
3. **Jira Sync (Optional):**
   - Select the checkboxes for the stories you wish to sync.
   - Click "Send to Jira".
   - Enter your Jira credentials (Domain, Email, API Token, Project Key).
   - **Note:** An API Token is required, not a password.
   - Click "Sync".
4. **Verification:** Log in to your Jira project to verify the new tickets have been created.

## 3. Troubleshooting

- **"Connecting to API..." spinner never stops:** Ensure `python api.py` is running.
- **"Job Failed" error:** Check the terminal running `python worker.py`. It usually indicates Ollama is not running or the model is not pulled.
- **Jira Sync fails:** Verify your API token permissions and that the Project Key (e.g., "KAN") exists in your Jira instance.