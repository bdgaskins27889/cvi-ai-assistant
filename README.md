# CVI AI Assistant — Generative AI for Community Violence Intervention

**DSC 670 — Advanced Uses of Generative AI**  
**Bellevue University**  
**Barbara D. Gaskins | Professor Neugebauer | 2026**

---

## Project Overview

The CVI AI Assistant is a fine-tuned generative AI system designed to support Community Violence Intervention (CVI) practitioners, including credible messengers and violence interrupters. The system provides trauma-informed, non-punitive guidance grounded in evidence-based CVI frameworks such as Cure Violence and Group Violence Intervention (GVI).

Rather than replacing human judgment, this tool augments practitioner decision-making by offering real-time guidance, scenario-based coaching, and structured documentation support through a secure web-based interface built with Streamlit.

## Key Features

The application provides five specialized intervention tools, each corresponding to a validated prompt experiment from the project's research phase:

| Tool | Description |
|------|-------------|
| **De-Escalation Guidance** | Provides trauma-informed de-escalation strategies for active conflict situations |
| **Scenario-Based Coaching** | Offers guided coaching for complex intervention scenarios with key considerations and approach recommendations |
| **Trauma-Informed Reframing** | Transforms messages into trauma-informed language that acknowledges stress, avoids blame, and reinforces personal agency |
| **Documentation Assistant** | Converts field notes into neutral, structured intervention summaries for program documentation |
| **Reflective Analysis** | Generates reflective questions for post-intervention evaluation and professional development |

## Ethical Principles

This system is built on the following ethical foundations:

- **Privacy First** — No personal data is stored or used in model training
- **Human Oversight** — AI augments practitioner expertise; it never replaces it
- **Non-Punitive** — The system never recommends enforcement actions or punitive measures
- **Culturally Competent** — Responses respect community context and lived experience
- **Transparent** — The system is clear about its limitations and the role of AI in CVI work

## Technical Architecture

### Fine-Tuned Model

The system uses a fine-tuned GPT-4.1-mini model, specialized for CVI contexts through training on:

- Anonymized CVI case studies and intervention narratives
- De-escalation techniques and frameworks
- Trauma-informed communication standards
- Evidence-based violence prevention practices
- Reflective practice and documentation templates

### Fine-Tuning Pipeline

The `fine_tune_model.py` script provides the complete fine-tuning pipeline:

1. Training data validation (JSONL format)
2. File upload to OpenAI
3. Fine-tuning job creation and monitoring
4. Model testing and configuration export

### Training Data

The `cvi_fine_tuning_data.jsonl` file contains curated training examples covering all five intervention tool categories. Each example follows the chat completion format with system, user, and assistant messages.

## Project Structure

```
cvi-ai-assistant/
├── .gitignore                     # Prevents secrets and cache from being committed
├── .streamlit/
│   └── config.toml                # Streamlit theme and server configuration
├── app.py                         # Main Streamlit application
├── fine_tune_model.py             # Fine-tuning pipeline script
├── cvi_fine_tuning_data.jsonl     # Training data for fine-tuning (50 examples)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── DEPLOYMENT_GUIDE.md            # Continuous deployment guide for Streamlit Cloud
└── screenshots/                   # Application screenshots
    ├── 01_main_dashboard.png
    ├── 02_de_escalation_input.png
    └── ...
```

## Installation and Setup

### Prerequisites

- Python 3.9 or higher
- An OpenAI API key

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cvi-ai-assistant.git
   cd cvi-ai-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. (Optional) Run the fine-tuning pipeline:
   ```bash
   python fine_tune_model.py
   ```

5. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```

6. Open your browser and navigate to `http://localhost:8501`

### Deploying to Streamlit Community Cloud

For continuous deployment to the web, see the full [Deployment Guide](DEPLOYMENT_GUIDE.md). In short:

1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. Click **New app**, select this repository, and set the main file to `app.py`.
4. Add your `OPENAI_API_KEY` in **Settings > Secrets**.
5. Every push to `main` automatically redeploys the live app.

## Usage

1. Select an intervention tool from the dropdown menu
2. Enter your scenario, field notes, or message in the text area
3. Click "Generate Response" to receive AI-generated guidance
4. Review the response and download it if needed
5. View your session history in the expandable section below

## References

- Braga, A. A., Weisburd, D., & Turchan, B. (2018). Focused deterrence strategies and crime control: An updated systematic review and meta-analysis of the empirical evidence. *Criminology & Public Policy, 17*(1), 205–250.
- Butts, J. A., Roman, C. G., Bostwick, L., & Porter, J. R. (2015). Cure Violence: A public health model to reduce gun violence. *Annual Review of Public Health, 36*, 39–53.
- Centers for Disease Control and Prevention. (2022). *Preventing youth violence: Technical package of policies, programs, and practices*.

## License

This project is developed for academic purposes as part of DSC 670 at Bellevue University.

## Disclaimer

This AI assistant is designed to support — not replace — trained CVI practitioners. All guidance should be evaluated using professional judgment and contextual knowledge. This tool does not provide medical, legal, or law enforcement advice.
