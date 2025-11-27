# AI-Powered Requirements Engineering Tool for SRS Generation

A modular, local-first web application that automates the analysis of user feedback. It ingests raw data, classifies it using Local LLMs (Ollama), generates structured requirements (SRS/User Stories), and synchronizes directly to Jira Cloud.

## 🚀 Quick Start 

This is the recommended way to run the application. It ensures all dependencies and databases are configured automatically.

### 1. Prerequisites

- **Docker Desktop** (Installed and running)
- **Ollama** (Installed on your host machine) → [Download here](https://ollama.com)

### 2. Setup & Run

Open your terminal in this project folder and run these three commands:

#### Step A: Download AI Models

This script reads `prompts_config.json` and automatically pulls the required models (Mistral, Llama, etc.) to your local Ollama.

```bash
python model_setup.py
```

#### Step B: Launch the App

This builds the container and starts the API and Worker services.

```bash
docker-compose up --build
```

#### Step C: Access the UI

Open your browser to: **http://localhost:8001/**

## 🧪 Experiments & Usage

Once the app is running (Step C above), follow these steps to replicate our experiments.

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

## 📂 Legacy / Manual Installation

If you cannot use Docker and prefer to run Python scripts manually on your host machine, please refer to the [Manual Setup Guide](docs/MANUAL_SETUP.md).
