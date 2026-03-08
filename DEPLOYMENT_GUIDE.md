# Continuous Deployment Guide — CVI AI Assistant on Streamlit Community Cloud

**Barbara D. Gaskins | DSC 670 — Advanced Uses of Generative AI | Bellevue University**

This guide walks you through setting up continuous deployment for the CVI AI Assistant on Streamlit Community Cloud. Once configured, every time you push code changes to your GitHub repository, the live application will automatically update within seconds.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Step 1 — Create a GitHub Repository](#2-step-1--create-a-github-repository)
3. [Step 2 — Push Your Project Files to GitHub](#3-step-2--push-your-project-files-to-github)
4. [Step 3 — Deploy on Streamlit Community Cloud](#4-step-3--deploy-on-streamlit-community-cloud)
5. [Step 4 — Add Your OpenAI API Key as a Secret](#5-step-4--add-your-openai-api-key-as-a-secret)
6. [Step 5 — Verify the Live Application](#6-step-5--verify-the-live-application)
7. [Step 6 — Continuous Deployment Workflow](#7-step-6--continuous-deployment-workflow)
8. [Troubleshooting](#8-troubleshooting)
9. [Repository Structure Reference](#9-repository-structure-reference)

---

## 1. Prerequisites

Before you begin, make sure you have the following:

| Requirement | Details |
|---|---|
| **GitHub Account** | A free account at [github.com](https://github.com) |
| **Git** | Installed on your local machine ([download here](https://git-scm.com/downloads)) |
| **OpenAI API Key** | Your API key from [platform.openai.com](https://platform.openai.com/api-keys) |
| **Streamlit Community Cloud Account** | Free account at [share.streamlit.io](https://share.streamlit.io) (sign in with GitHub) |
| **Project Files** | The `cvi_ai_app` folder containing `app.py`, `requirements.txt`, and all supporting files |

---

## 2. Step 1 — Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new) and sign in.
2. Fill in the repository details:
   - **Repository name**: `cvi-ai-assistant`
   - **Description**: `Generative AI for Community Violence Intervention — Trauma-Informed, Non-Punitive Decision Support`
   - **Visibility**: Select **Public** (required for the free tier of Streamlit Community Cloud, and great for your portfolio)
   - **Initialize this repository with**: Leave all checkboxes **unchecked** (we will push our existing files)
3. Click **Create repository**.
4. Keep this page open — you will need the repository URL in the next step.

---

## 3. Step 2 — Push Your Project Files to GitHub

Open a terminal on your local machine, navigate to the project folder, and run the following commands. Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

```bash
# Navigate to the project folder
cd cvi_ai_app

# Initialize a new Git repository
git init

# Add all project files
git add .

# Create the first commit
git commit -m "Initial commit: CVI AI Assistant — DSC 670 Final Project"

# Set the main branch
git branch -M main

# Connect to your GitHub repository
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/cvi-ai-assistant.git

# Push the code to GitHub
git push -u origin main
```

After running these commands, refresh your GitHub repository page. You should see all your project files listed there.

### Important: The `.gitignore` file

The included `.gitignore` file is configured to prevent sensitive files from being committed to GitHub. In particular, it excludes `.streamlit/secrets.toml`, which is where API keys would be stored locally. **Never commit API keys to GitHub.**

---

## 4. Step 3 — Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and click **Sign in with GitHub**.
2. Authorize Streamlit to access your GitHub account if prompted.
3. Once signed in, click the **New app** button in the upper right corner.
4. Fill in the deployment form:

   | Field | Value |
   |---|---|
   | **Repository** | `YOUR_GITHUB_USERNAME/cvi-ai-assistant` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` |

5. Click **Advanced settings** (optional but recommended):
   - **Python version**: Select `3.11` (or the latest available)
6. Click **Deploy!**

Streamlit Community Cloud will now:
- Clone your repository
- Install the packages listed in `requirements.txt`
- Launch your Streamlit application
- Assign it a public URL (e.g., `https://your-username-cvi-ai-assistant-app-xxxxx.streamlit.app`)

The first deployment may take 2-3 minutes. You will see a progress log during this time.

---

## 5. Step 4 — Add Your OpenAI API Key as a Secret

Your application requires an OpenAI API key to function. Streamlit Community Cloud provides a secure way to store secrets that are **never exposed in your code or repository**.

1. In the Streamlit Community Cloud dashboard, find your deployed app.
2. Click the **three-dot menu** (kebab menu) on your app card, then click **Settings**.
3. In the Settings panel, click the **Secrets** tab.
4. Paste the following into the secrets editor:

   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
   ```

   If you are using a custom fine-tuned model, also add:

   ```toml
   CVI_MODEL_ID = "ft:gpt-4.1-mini:your-org:cvi-assistant:your-model-id"
   ```

5. Click **Save**.

Your app will automatically reboot with the new secrets loaded. Streamlit Cloud injects these values as environment variables, which your `app.py` reads via `os.environ.get()`.

### How Secrets Work

Streamlit Community Cloud secrets are:
- **Encrypted at rest** and in transit
- **Never visible** in your repository or deployment logs
- **Injected as environment variables** at runtime
- **Accessible only to you** (the app owner)

This means your `app.py` code does not need any changes — it already reads the API key from the environment using `OpenAI()`, which automatically picks up `OPENAI_API_KEY`.

---

## 6. Step 5 — Verify the Live Application

1. Once the deployment is complete, Streamlit will display your app's public URL.
2. Open the URL in your browser.
3. Test the application:
   - Select **De-Escalation Guidance** from the dropdown.
   - Enter a test scenario (e.g., "Two individuals with a history of conflict are in a heated verbal argument at a community basketball court.").
   - Click **Generate Response**.
   - Verify that the AI generates a trauma-informed, step-by-step response.
4. Test each of the five tools to confirm they all work correctly.

**Your app is now live and publicly accessible.** You can share this URL in your GitHub README, your resume, and your portfolio.

---

## 7. Step 6 — Continuous Deployment Workflow

This is the key benefit of Streamlit Community Cloud: **every push to your `main` branch automatically triggers a redeployment**. There is nothing additional to configure — it works out of the box.

### How It Works

```
You edit code locally
        |
        v
git add . && git commit -m "Update feature"
        |
        v
git push origin main
        |
        v
GitHub receives the push
        |
        v
Streamlit Community Cloud detects the change
        |
        v
App automatically rebuilds and redeploys (30-60 seconds)
        |
        v
Live app is updated — no downtime
```

### Making Changes

Whenever you want to update your application, follow this simple workflow:

```bash
# 1. Make your code changes in app.py (or any file)

# 2. Stage the changes
git add .

# 3. Commit with a descriptive message
git commit -m "Add new trauma-informed reframing examples"

# 4. Push to GitHub
git push origin main
```

Within 30-60 seconds, your live application will reflect the changes. Streamlit Community Cloud watches your repository and automatically redeploys when it detects a new commit on the `main` branch.

### Example: Adding a New Tool

If you want to add a sixth intervention tool (e.g., "Community Resource Mapping"), you would:

1. Add the new tool definition to the `TOOLS` dictionary in `app.py`.
2. Add corresponding training examples to `cvi_fine_tuning_data.jsonl`.
3. Update the metric card from "5" to "6" in `app.py`.
4. Commit and push:
   ```bash
   git add .
   git commit -m "Add Community Resource Mapping tool"
   git push origin main
   ```
5. The live app updates automatically.

### Branch-Based Development (Optional)

For more complex changes, you can use feature branches to test before deploying:

```bash
# Create a feature branch
git checkout -b feature/new-tool

# Make your changes and commit
git add .
git commit -m "WIP: New community resource mapping tool"

# Push the feature branch (this does NOT trigger redeployment)
git push origin feature/new-tool

# When ready, merge into main (this DOES trigger redeployment)
git checkout main
git merge feature/new-tool
git push origin main
```

---

## 8. Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|---|---|---|
| **App shows "Error" on startup** | Missing API key | Add `OPENAI_API_KEY` in Settings > Secrets |
| **App crashes after push** | Syntax error in code | Check the app logs in the Streamlit Cloud dashboard |
| **Dependencies not installing** | Missing package in `requirements.txt` | Add the package and push again |
| **App is slow to respond** | OpenAI API latency | This is normal; responses typically take 5-15 seconds |
| **"App is sleeping"** | Free tier apps sleep after inactivity | Visit the URL to wake it up (takes ~30 seconds) |
| **Changes not appearing** | Browser cache | Hard refresh with `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac) |

### Viewing Logs

1. Go to your Streamlit Community Cloud dashboard.
2. Click on your app.
3. Click **Manage app** (bottom-right corner of the running app).
4. Select **Logs** to view real-time application logs.

### Rebooting the App

If the app is in a bad state:
1. Go to your Streamlit Community Cloud dashboard.
2. Click the three-dot menu on your app card.
3. Click **Reboot**.

---

## 9. Repository Structure Reference

After completing all steps, your GitHub repository should look like this:

```
cvi-ai-assistant/
├── .gitignore                     # Prevents secrets and cache from being committed
├── .streamlit/
│   └── config.toml                # Streamlit theme and server configuration
├── app.py                         # Main Streamlit application (664 lines)
├── fine_tune_model.py             # Fine-tuning pipeline script
├── cvi_fine_tuning_data.jsonl     # Training data (50 examples)
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── DEPLOYMENT_GUIDE.md            # This deployment guide
└── screenshots/                   # Application screenshots
    ├── 01_main_dashboard.png
    ├── 02_de_escalation_input.png
    ├── 03_de_escalation_response.png
    ├── 04_ai_response_view.png
    ├── 05_response_detail.png
    └── 06_sidebar_view.png
```

---

## Summary

With Streamlit Community Cloud, continuous deployment is automatic and requires no additional CI/CD configuration. The workflow is straightforward:

1. **Edit** your code locally.
2. **Commit** and **push** to the `main` branch on GitHub.
3. **Streamlit Cloud** detects the change and redeploys automatically.
4. **Your live app** updates within 30-60 seconds.

This setup gives you a professional, portfolio-ready deployment that demonstrates both your technical skills and your ability to deliver a production-quality application. The live URL can be shared directly with potential employers, included in your resume, and referenced in your GitHub profile.

---

*CVI AI Assistant | DSC 670 — Advanced Uses of Generative AI | Bellevue University*
*Barbara D. Gaskins | Professor Neugebauer | 2026*
