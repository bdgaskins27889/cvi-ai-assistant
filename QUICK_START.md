# 🚀 Quick Start: CVI AI Assistant on Kaggle

Deploy your benchmark to Kaggle in **one single command**.

## 1. Prerequisites
Ensure you have your `kaggle.json` file (from [Kaggle Settings](https://www.kaggle.com/settings/account)) ready.

## 2. Deploy Everything
Run this command in your terminal from the project folder:

```bash
# Make the script executable and run it
chmod +x one_click_deploy.sh && ./one_click_deploy.sh
```

### What this does:
*   Installs all necessary software.
*   Connects to your Kaggle account.
*   Uploads the CVI dataset and benchmark script.
*   Starts the first evaluation run automatically.

## 3. View Results
After a few minutes, check your scores:
```bash
kaggle b r list
```

---
*That's it! Your benchmark is now live and evaluating on Kaggle.*
