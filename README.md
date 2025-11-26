# AI-Powered Review Classifier & Jira Sync

A modular, local-first web application that automates the analysis of user feedback. It ingests raw data, classifies it using Local LLMs (Ollama), generates structured requirements (SRS/User Stories), and synchronizes directly to Jira Cloud.

## 🚀 Quick Start (Docker)

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

- **Goal:** Classify raw reviews into "Feature Request" or "Bug".
- **Action:**
  1. Click "Functional (FR)".
  2. Select LLM: `mistral` (or as configured).
  3. Select Strategy: `zero-shot`.
  4. Upload `inputs/functional_reviews.txt`.
  5. Click Process Reviews.

### Experiment 2: Non-Functional Requirement (NFR) Classification

- **Goal:** Classify reviews into categories like Performance, Security, Usability.
- **Action:**
  1. Click "Non-Functional (NFR)".
  2. Select Strategy: `role-based`.
  3. Upload `inputs/nfr_dataset.xlsx` (Select the specific review column).
  4. Click Process Reviews.

### Experiment 3: Jira Synchronization

- **Goal:** Convert reviews to User Stories and push to Jira.
- **Action:**
  1. After processing reviews, click "Generate Stories".
  2. Select stories to sync and click "Send to Jira".
  3. Enter credentials (API Token required) and Sync.

## 📂 Legacy / Manual Installation

If you cannot use Docker and prefer to run Python scripts manually on your host machine, please refer to the [Manual Setup Guide](REPLICATION_GUIDE.md).