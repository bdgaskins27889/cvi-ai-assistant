# OpenAI API Key Guide for the CVI AI Assistant

## What Is an OpenAI API Key?

An OpenAI API key is a unique password-like string that allows your application to communicate with OpenAI's AI models (like GPT-4.1-mini, which powers your CVI AI Assistant). Think of it as a secure credential that tells OpenAI, "This request is coming from Barbara's account, and she has permission to use the AI."

Every time a user clicks "Generate Response" in your Streamlit app, the app sends the user's input to OpenAI's servers, which process it through the fine-tuned model and send back the AI-generated guidance. The API key authenticates that request.

## How It Works in Your App

The flow is straightforward:

1. A CVI practitioner types a scenario into your Streamlit app.
2. Your app sends that text to OpenAI's API along with your API key.
3. OpenAI verifies the key, processes the request through the AI model, and returns a response.
4. Your app displays the trauma-informed guidance to the practitioner.

In your `app.py` code, this happens in the line:

```python
client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")))
```

The app first checks Streamlit Secrets (for cloud deployment), then checks environment variables (for local development).

## How Much Does It Cost?

OpenAI charges based on usage (how many words/tokens your app processes), not a flat monthly fee. For the model your app uses (GPT-4.1-mini), the pricing is very affordable:

| What You Pay For | Cost |
|---|---|
| Input tokens (what the user types + system prompt) | ~$0.40 per 1 million tokens |
| Output tokens (the AI's response) | ~$1.60 per 1 million tokens |

To put this in perspective, 1 million tokens is roughly 750,000 words. A typical interaction with your CVI app uses about 500-1,000 tokens total. That means approximately 1,000 to 2,000 interactions would cost about $1.00. For a class project and portfolio demo, you would likely spend less than $1-5 total.

OpenAI also provides new accounts with free credits to get started.

## Step-by-Step: How to Get Your API Key

### Step 1: Create an OpenAI Account

1. Go to [https://platform.openai.com/signup](https://platform.openai.com/signup)
2. Sign up with your email (`bdgaskins27889@gmail.com`), Google account, or Microsoft account.
3. Verify your email address.
4. You may need to verify your phone number.

### Step 2: Add a Payment Method (Required)

1. After signing in, go to [https://platform.openai.com/settings/organization/billing/overview](https://platform.openai.com/settings/organization/billing/overview)
2. Click **"Add payment method"**.
3. Enter a credit or debit card.
4. Set a **monthly spending limit** (recommended: $5-10 for a class project) to avoid any surprises.

Note: OpenAI may offer free trial credits for new accounts. Even without free credits, your project will cost very little.

### Step 3: Generate Your API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **"Create new secret key"**.
3. Give it a name: `CVI AI Assistant`
4. Click **"Create secret key"**.
5. **IMPORTANT: Copy the key immediately!** It starts with `sk-` and you will NOT be able to see it again after closing the dialog.
6. Save it somewhere secure (a password manager, a private note, etc.).

### Step 4: Use the Key in Your App

**For local development** (running on your own computer):

```bash
export OPENAI_API_KEY="sk-your-key-here"
streamlit run app.py
```

**For Streamlit Cloud deployment:**

1. Go to your app on [share.streamlit.io](https://share.streamlit.io).
2. Click the three dots (⋮) on your app, then **Settings**.
3. Click **Secrets**.
4. Paste:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```
5. Click **Save**. Your app will restart automatically.

## Security Best Practices

Your API key is like a password. Follow these rules to keep it safe:

1. **Never commit it to GitHub.** Your `.gitignore` file is already configured to prevent this.
2. **Never share it publicly.** Do not paste it in emails, chat messages, or documents.
3. **Use Streamlit Secrets** for cloud deployment (not hardcoded in your code).
4. **Set spending limits** on your OpenAI account to prevent unexpected charges.
5. **Rotate keys** if you suspect one has been compromised. You can delete old keys and create new ones at any time.

## Troubleshooting

| Issue | Solution |
|---|---|
| "Invalid API key" error | Double-check that you copied the full key (starts with `sk-`). Make sure there are no extra spaces. |
| "Insufficient quota" error | Add a payment method or check your spending limits at platform.openai.com. |
| "Rate limit exceeded" error | You are sending too many requests too quickly. Wait a moment and try again. |
| App works locally but not on Streamlit Cloud | Make sure you added the key in Streamlit Cloud Settings > Secrets. |

## Summary

The OpenAI API key is the bridge between your Streamlit app and the AI model that powers it. Getting one takes about 5 minutes, costs are minimal for a class project (likely under $5 total), and your app is already configured to use it securely through either environment variables or Streamlit Secrets.
