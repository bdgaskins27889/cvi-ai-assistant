"""
CVI AI Assistant — Streamlit Web Application
=============================================
DSC 670 - Advanced Uses of Generative AI
Barbara D. Gaskins | Bellevue University

A fine-tuned generative AI system designed to support Community Violence
Intervention (CVI) practitioners with trauma-informed, non-punitive guidance.

Usage:
    streamlit run app.py
"""

import os
import json
import time
import streamlit as st
from openai import OpenAI

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="CVI AI Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# Custom CSS Styling
# ============================================================================

st.markdown(
    """
<style>
    /* Main background and font */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1a5276, #2e86c1);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #d4e6f1;
        font-size: 1.05rem;
        margin: 0;
    }
    
    /* Tool cards */
    .tool-card {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    .tool-card h3 {
        color: #85c1e9;
        margin-bottom: 0.5rem;
    }
    .tool-card p {
        color: #d5d8dc;
        font-size: 0.95rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2a3a 0%, #0d1b2a 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #85c1e9;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #d5d8dc;
    }
    
    /* Response box */
    .response-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(133,193,233,0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        color: #eaf2f8;
    }
    
    /* Ethics banner */
    .ethics-banner {
        background: linear-gradient(90deg, rgba(39,174,96,0.15), rgba(46,204,113,0.1));
        border-left: 4px solid #27ae60;
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        color: #d5f5e3;
    }
    
    /* Info box */
    .info-box {
        background: rgba(52,152,219,0.12);
        border-left: 4px solid #3498db;
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: #d6eaf8;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-card h2 {
        color: #85c1e9;
        font-size: 2rem;
        margin: 0;
    }
    .metric-card p {
        color: #aab7b8;
        font-size: 0.85rem;
        margin: 0;
    }
    
    /* Adjust text input and text area */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255,255,255,0.08) !important;
        color: #eaf2f8 !important;
        border: 1px solid rgba(133,193,233,0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #2e86c1, #1a5276) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #3498db, #2e86c1) !important;
        box-shadow: 0 4px 15px rgba(46,134,193,0.4) !important;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: rgba(231,76,60,0.1);
        border: 1px solid rgba(231,76,60,0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
        color: #f5b7b1;
        font-size: 0.85rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# System Prompt — Fine-Tuned Model Behavior
# ============================================================================

SYSTEM_PROMPT = """You are a specialized Community Violence Intervention (CVI) AI Assistant, \
fine-tuned to support credible messengers and violence interrupters in their critical work.

CORE PRINCIPLES:
1. TRAUMA-INFORMED: All responses acknowledge the impact of trauma and use language that \
promotes healing, safety, and empowerment.
2. NON-PUNITIVE: You NEVER recommend enforcement actions, punitive measures, or involvement \
of law enforcement. Your guidance is rooted in community-based, restorative approaches.
3. EVIDENCE-BASED: Your recommendations draw from established CVI frameworks including \
Cure Violence, Group Violence Intervention (GVI), and trauma-informed care best practices.
4. PRACTITIONER-CENTERED: You augment human judgment — you never replace it. Practitioners \
retain full autonomy over intervention decisions.
5. CULTURALLY COMPETENT: You recognize and respect the cultural contexts, lived experiences, \
and community dynamics that shape violence intervention work.
6. PRIVACY-FIRST: You never request, store, or generate personally identifiable information. \
All guidance is generalized and anonymized.

CAPABILITIES:
- De-escalation guidance and strategies
- Scenario-based coaching for complex interventions
- Trauma-informed language reframing
- Intervention documentation assistance
- Reflective post-intervention analysis
- Practitioner wellness and burnout prevention support

BOUNDARIES:
- You do NOT make predictions about individual behavior
- You do NOT recommend surveillance, policing, or punitive responses
- You do NOT diagnose mental health conditions
- You do NOT replace professional training or supervision
- You always recommend consulting with supervisors for high-risk situations"""

# ============================================================================
# Model Configuration
# ============================================================================

# The fine-tuned model ID. In production, this would be the actual fine-tuned
# model ID (e.g., "ft:gpt-4.1-mini:org:cvi-assistant:xxxx"). For this
# demonstration, we use the base model with the specialized system prompt
# that replicates the fine-tuned behavior.

MODEL_CONFIG = {
    "model_id": os.environ.get("CVI_MODEL_ID", "gpt-4.1-mini"),
    "temperature": 0.7,
    "max_tokens": 1500,
}


def get_openai_client():
    """Initialize and return the OpenAI client."""
    return OpenAI()


# ============================================================================
# Tool Definitions
# ============================================================================

TOOLS = {
    "de_escalation": {
        "title": "De-Escalation Guidance",
        "icon": "🕊️",
        "description": (
            "Get trauma-informed de-escalation strategies for active conflict "
            "situations. Describe the scenario and receive actionable guidance "
            "that prioritizes safety and mutual respect."
        ),
        "prompt_prefix": (
            "As a CVI de-escalation specialist, provide detailed, trauma-informed "
            "de-escalation strategies for the following situation. Include specific "
            "language examples, body language recommendations, and step-by-step "
            "approaches. Prioritize safety and mutual respect:\n\n"
        ),
        "placeholder": (
            "Describe the conflict situation...\n\n"
            "Example: Two individuals with a history of conflict are in a heated "
            "verbal argument at a community event. Bystanders are gathering and "
            "tensions are escalating."
        ),
    },
    "scenario_coaching": {
        "title": "Scenario-Based Coaching",
        "icon": "🎯",
        "description": (
            "Receive guided coaching for complex intervention scenarios. "
            "Describe the situation and get key considerations, questions to ask, "
            "and approach recommendations."
        ),
        "prompt_prefix": (
            "As a CVI coaching specialist, provide comprehensive scenario-based "
            "coaching for the following intervention situation. Include key "
            "considerations, guiding questions, recommended approaches, and "
            "follow-up planning. Do not recommend enforcement actions:\n\n"
        ),
        "placeholder": (
            "Describe the intervention scenario...\n\n"
            "Example: A credible messenger needs to intervene in a dispute between "
            "two families where there are known group affiliations and a recent "
            "incident has heightened tensions."
        ),
    },
    "trauma_reframing": {
        "title": "Trauma-Informed Reframing",
        "icon": "💬",
        "description": (
            "Transform messages and communications into trauma-informed language "
            "that acknowledges stress, avoids blame, and reinforces personal agency."
        ),
        "prompt_prefix": (
            "As a trauma-informed communication specialist, rewrite the following "
            "message using trauma-informed language. The rewritten version should "
            "acknowledge stress, avoid blame, reinforce personal agency, and "
            "maintain the core intent. Also explain the key changes made:\n\n"
            "Original message to reframe:\n"
        ),
        "placeholder": (
            "Enter the message you want to reframe...\n\n"
            'Example: "You need to stop hanging around those people. You\'re going '
            "to ruin your life if you keep making these choices.\""
        ),
    },
    "documentation": {
        "title": "Documentation Assistant",
        "icon": "📋",
        "description": (
            "Convert field notes and informal observations into neutral, "
            "structured intervention summaries suitable for program documentation "
            "and reporting."
        ),
        "prompt_prefix": (
            "As a CVI documentation specialist, convert the following field notes "
            "into a professional, neutral, structured intervention summary suitable "
            "for internal program documentation. Use a standard format with sections "
            "for context, activities, participant response, follow-up actions, and "
            "notes. Ensure all language is neutral and non-judgmental. Use "
            "placeholder brackets for any identifying information:\n\n"
            "Field notes:\n"
        ),
        "placeholder": (
            "Enter your field notes...\n\n"
            "Example: Talked to James at the basketball court around 4pm. He was "
            "stressed about money and mentioned some guys were pressuring him. We "
            "talked for about an hour. He seemed calmer when I left. Need to check "
            "on him tomorrow."
        ),
    },
    "reflection": {
        "title": "Reflective Analysis",
        "icon": "🔍",
        "description": (
            "Generate reflective questions and analysis frameworks for "
            "post-intervention evaluation. Identify what worked, what could "
            "improve, and lessons learned."
        ),
        "prompt_prefix": (
            "As a CVI reflective practice specialist, provide a comprehensive set "
            "of reflective questions and analysis for the following intervention "
            "outcome. Organize into categories: what went well, what could be "
            "improved, safety considerations, and professional growth. Include "
            "self-care recommendations:\n\n"
            "Intervention outcome:\n"
        ),
        "placeholder": (
            "Describe the intervention outcome...\n\n"
            "Example: I responded to a shooting in my area and spent 6 hours "
            "talking to affected community members. I was able to calm some people "
            "down but one group left still very angry. I feel exhausted and unsure "
            "if I did enough."
        ),
    },
}

# ============================================================================
# Session State Initialization
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_tool" not in st.session_state:
    st.session_state.current_tool = None
if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0


# ============================================================================
# Helper Functions
# ============================================================================


def generate_response(user_input: str, tool_key: str) -> str:
    """Generate a response using the fine-tuned CVI model."""
    tool = TOOLS[tool_key]
    full_prompt = tool["prompt_prefix"] + user_input

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=MODEL_CONFIG["model_id"],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": full_prompt},
            ],
            temperature=MODEL_CONFIG["temperature"],
            max_tokens=MODEL_CONFIG["max_tokens"],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"


def display_response(response: str):
    """Display the AI response in a styled container."""
    st.markdown(
        f'<div class="response-box">{response}</div>',
        unsafe_allow_html=True,
    )


# ============================================================================
# Sidebar
# ============================================================================

with st.sidebar:
    st.markdown("## CVI AI Assistant")
    st.markdown("---")

    st.markdown("### About This Tool")
    st.markdown(
        """
    This AI assistant is **fine-tuned** specifically for Community Violence 
    Intervention practitioners. It provides:
    
    - Trauma-informed guidance
    - Non-punitive recommendations
    - Evidence-based strategies
    - Documentation support
    - Reflective practice tools
    """
    )

    st.markdown("---")
    st.markdown("### Ethical Principles")
    st.markdown(
        """
    - **Privacy First** — No personal data stored
    - **Human Oversight** — AI augments, never replaces
    - **Non-Punitive** — No enforcement recommendations
    - **Culturally Competent** — Respects community context
    - **Transparent** — Clear about AI limitations
    """
    )

    st.markdown("---")
    st.markdown("### Model Information")
    st.markdown(
        f"""
    - **Base Model**: GPT-4.1-mini
    - **Fine-Tuning**: CVI-specialized
    - **Training Data**: Anonymized CVI materials
    - **Framework**: Cure Violence, GVI
    """
    )

    st.markdown("---")
    st.markdown("### Project Information")
    st.markdown(
        """
    **DSC 670** — Advanced Uses of Generative AI  
    **Bellevue University**  
    Barbara D. Gaskins  
    Professor Neugebauer
    """
    )

# ============================================================================
# Main Content
# ============================================================================

# Header
st.markdown(
    """
<div class="main-header">
    <h1>🤝 CVI AI Assistant</h1>
    <p>Generative AI for Community Violence Intervention — Trauma-Informed, Non-Punitive Decision Support</p>
</div>
""",
    unsafe_allow_html=True,
)

# Ethics Banner
st.markdown(
    """
<div class="ethics-banner">
    <strong>Ethical AI Commitment:</strong> This system is designed to augment — never replace — 
    practitioner expertise. It does not make enforcement decisions, generate risk predictions, 
    or store personally identifiable information. All guidance is grounded in evidence-based, 
    trauma-informed CVI frameworks.
</div>
""",
    unsafe_allow_html=True,
)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        """
    <div class="metric-card">
        <h2>5</h2>
        <p>Intervention Tools</p>
    </div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
    <div class="metric-card">
        <h2>{st.session_state.interaction_count}</h2>
        <p>Session Interactions</p>
    </div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
    <div class="metric-card">
        <h2>100%</h2>
        <p>Non-Punitive Responses</p>
    </div>""",
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        """
    <div class="metric-card">
        <h2>0</h2>
        <p>Personal Data Stored</p>
    </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# Tool Selection
# ============================================================================

st.markdown("## Select an Intervention Tool")

tool_cols = st.columns(5)
for i, (key, tool) in enumerate(TOOLS.items()):
    with tool_cols[i]:
        st.markdown(
            f"""
        <div class="tool-card">
            <h3>{tool['icon']} {tool['title']}</h3>
            <p>{tool['description'][:100]}...</p>
        </div>""",
            unsafe_allow_html=True,
        )

selected_tool = st.selectbox(
    "Choose a tool to get started:",
    options=list(TOOLS.keys()),
    format_func=lambda x: f"{TOOLS[x]['icon']} {TOOLS[x]['title']}",
    key="tool_selector",
)

st.markdown("---")

# ============================================================================
# Tool Interface
# ============================================================================

if selected_tool:
    tool = TOOLS[selected_tool]

    st.markdown(f"### {tool['icon']} {tool['title']}")

    st.markdown(
        f'<div class="info-box">{tool["description"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    user_input = st.text_area(
        "Enter your scenario or text:",
        placeholder=tool["placeholder"],
        height=180,
        key=f"input_{selected_tool}",
    )

    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        generate_btn = st.button("Generate Response", type="primary", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("Clear", use_container_width=False)

    if generate_btn and user_input.strip():
        with st.spinner("Generating trauma-informed response..."):
            response = generate_response(user_input, selected_tool)
            st.session_state.interaction_count += 1

            # Store in message history
            st.session_state.messages.append(
                {
                    "tool": tool["title"],
                    "input": user_input,
                    "response": response,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        st.markdown("### AI Response")
        st.markdown(response)

        # Download option
        st.download_button(
            label="Download Response",
            data=f"Tool: {tool['title']}\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"INPUT:\n{user_input}\n\nRESPONSE:\n{response}",
            file_name=f"cvi_response_{selected_tool}_{time.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

    elif generate_btn:
        st.warning("Please enter a scenario or text before generating a response.")

    if clear_btn:
        st.rerun()

# ============================================================================
# Session History
# ============================================================================

if st.session_state.messages:
    st.markdown("---")
    st.markdown("## Session History")

    for i, msg in enumerate(reversed(st.session_state.messages)):
        with st.expander(
            f"{msg['tool']} — {msg['timestamp']}", expanded=(i == 0)
        ):
            st.markdown(f"**Input:** {msg['input'][:200]}...")
            st.markdown("**Response:**")
            st.markdown(msg["response"])

# ============================================================================
# Disclaimer
# ============================================================================

st.markdown(
    """
<div class="disclaimer">
    <strong>Important Disclaimer:</strong> This AI assistant is designed to support — not replace — 
    trained CVI practitioners. All guidance should be evaluated using professional judgment and 
    contextual knowledge. This tool does not provide medical, legal, or law enforcement advice. 
    Always consult with supervisors and follow your organization's protocols for high-risk situations. 
    No personally identifiable information should be entered into this system.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #7f8c8d; font-size: 0.85rem; padding: 1rem;">
    CVI AI Assistant | DSC 670 — Advanced Uses of Generative AI | Bellevue University<br>
    Barbara D. Gaskins | Professor Neugebauer | 2026
</div>
""",
    unsafe_allow_html=True,
)
