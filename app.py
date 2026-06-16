"""
CVI AI Assistant — Streamlit Web Application
=============================================
DSC 670 - Advanced Uses of Generative AI
Barbara D. Gaskins | Bellevue University

A fine-tuned generative AI system designed to support Community Violence
Intervention (CVI) practitioners with trauma-informed, non-punitive guidance.

HYBRID MODE:
    - Demo Mode: Works immediately with pre-built, expert-crafted responses.
    - Live AI Mode: Automatically activates when an OpenAI API key is provided.

Usage:
    streamlit run app.py
"""

import os
import json
import time
import streamlit as st

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
    
    /* Mode badge */
    .mode-badge-demo {
        background: linear-gradient(90deg, rgba(243,156,18,0.2), rgba(241,196,15,0.15));
        border: 1px solid rgba(243,156,18,0.4);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin: 0.5rem 0;
        color: #f9e79f;
        font-size: 0.9rem;
    }
    .mode-badge-live {
        background: linear-gradient(90deg, rgba(39,174,96,0.2), rgba(46,204,113,0.15));
        border: 1px solid rgba(39,174,96,0.4);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin: 0.5rem 0;
        color: #abebc6;
        font-size: 0.9rem;
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

MODEL_CONFIG = {
    "model_id": os.environ.get("CVI_MODEL_ID", "gpt-4.1-mini"),
    "temperature": 0.7,
    "max_tokens": 1500,
}

# ============================================================================
# Demo Responses — Pre-Built Expert-Crafted CVI Guidance
# ============================================================================

DEMO_RESPONSES = {
    "de_escalation": {
        "default": """## De-Escalation Guidance

### Immediate Assessment
Before approaching, take a moment to assess the environment for safety. Identify exits, bystanders, and any objects that could escalate the situation. Regulate your own breathing — you cannot de-escalate others if your own nervous system is activated.

### Step-by-Step Approach

**Step 1: Establish Presence Without Threat**
- Approach from the side, not head-on. Keep your hands visible and your posture open.
- Maintain a calm, steady voice. Speak slightly slower than normal.
- Example language: *"Hey, I see you. I'm here. Nobody's in trouble."*

**Step 2: Acknowledge the Emotion**
- Validate what the person is feeling without agreeing with harmful actions.
- Example: *"I can see you're upset, and I get it. Something happened that got you to this point. Let's talk about it."*
- Avoid phrases like "calm down" or "you need to stop" — these escalate rather than de-escalate.

**Step 3: Create Separation**
- If two parties are in conflict, work to create physical and emotional distance.
- Example: *"Let me talk to you over here for a second. Just you and me. Give me two minutes."*
- Engage bystanders to help redirect the other party if a second interrupter is not available.

**Step 4: Redirect Toward Future**
- Shift the conversation from the immediate conflict to future consequences and goals.
- Example: *"I know you're heated right now, but think about tomorrow. Think about your kids, your mom. Is this worth what comes next?"*

**Step 5: Offer a Concrete Next Step**
- Give the person something actionable to do that moves them away from the conflict.
- Example: *"Let me give you a ride. Let's go get something to eat and figure this out."*

### Body Language Recommendations
- Keep your body at a 45-degree angle (non-confrontational)
- Nod slowly to show active listening
- Mirror their energy level slightly, then gradually bring it down
- Never cross your arms or point

### Safety Reminders
- If weapons are visible, do NOT approach — prioritize your own safety
- Always have an exit strategy
- Consult with your supervisor after any high-risk interaction

*This guidance is based on Cure Violence and trauma-informed de-escalation frameworks. Always use your professional judgment and knowledge of the individuals and community context.*""",
        "samples": {
            "heated argument": """## De-Escalation Guidance: Heated Verbal Argument

### Situation Analysis
A heated verbal argument in a public setting with bystanders gathering creates a high-risk environment where the presence of an audience can intensify the conflict. The priority is to reduce the audience, separate the parties, and lower emotional intensity.

### Immediate Actions

**1. Manage the Crowd First**
- Address bystanders calmly: *"Hey everybody, give them some space. Let me handle this."*
- Reducing the audience removes the social pressure to perform toughness.

**2. Approach the More Receptive Party**
- Identify which individual appears more open to dialogue and approach them first.
- Use their name if you know it: *"[Name], let me talk to you for a second. Come walk with me."*

**3. Use Empathic Listening**
- Let them vent without interrupting for the first 30-60 seconds.
- Respond with: *"I hear you. That's a lot to deal with. Tell me what happened from the beginning."*

**4. Reframe the Situation**
- Help them see the bigger picture: *"I know this feels like everything right now, but you've got too much going for you to let this moment define what happens next."*

**5. Facilitate Resolution or Separation**
- If both parties are willing: *"Can we sit down — all of us — and talk this through? No judgment, just conversation."*
- If not: *"Let's take a break. I'll check on the other person. Let's reconnect tomorrow when things are cooler."*

### Key Principles Applied
- **Trauma-Informed**: Recognizes that the anger may be rooted in deeper pain or past experiences
- **Non-Punitive**: No threats, no ultimatums, no involvement of authorities
- **Community-Based**: Leverages existing relationships and trust

*Always follow your organization's safety protocols and debrief with your supervisor after the interaction.*"""
        }
    },
    "scenario_coaching": {
        "default": """## Scenario-Based Coaching

### Assessment Framework
When approaching any complex intervention scenario, use the **REACH** framework:

- **R — Relationships**: What existing relationships do you have with the parties involved? Who else in the community has influence?
- **E — Environment**: Where and when is the safest setting for this intervention? What environmental factors could help or hinder?
- **A — Assess Risk**: What is the current threat level? Are there weapons involved? Is there an imminent timeline?
- **C — Community Resources**: What services, supports, or safe spaces can you connect people to?
- **H — History**: What is the history between the parties? Are there prior incidents, group dynamics, or unresolved conflicts?

### Guiding Questions to Ask Yourself
1. *"What is the underlying need driving this conflict?"* — Often it is respect, safety, resources, or grief.
2. *"Who has the most influence with each party?"* — Identify credible messengers who can reach each side.
3. *"What does a successful outcome look like?"* — Define it before you intervene so you can measure progress.
4. *"What is my role versus what requires a team approach?"* — You do not have to do this alone.
5. *"Am I regulated enough to do this work right now?"* — Check in with yourself honestly.

### Recommended Approach
1. **Gather intelligence through trusted community contacts** — not surveillance, but relationship-based information gathering.
2. **Make initial contact in a neutral, low-pressure setting** — a barbershop, a basketball court, a restaurant.
3. **Listen first, advise second** — spend at least 70% of the first interaction listening.
4. **Identify concrete needs** — housing, employment, mental health support, relocation assistance.
5. **Create a follow-up plan** — schedule the next check-in before you leave.

### Follow-Up Planning
- Check in within 24-48 hours after initial contact
- Connect to at least one concrete resource within the first week
- Document interactions using neutral, non-identifying language
- Debrief with your team and supervisor regularly

*This coaching framework draws from Group Violence Intervention (GVI) and Cure Violence methodologies. Adapt all recommendations to your specific community context.*""",
        "samples": {
            "gang_recruitment": """## Scenario-Based Coaching: Addressing Gang Recruitment\n\n### Situation Analysis\nA young person is expressing interest in joining a gang, driven by perceived needs for belonging, protection, or economic opportunity. This is a critical intervention point to offer alternatives and reinforce positive pathways.\n\n### Guiding Questions for the Practitioner\n1.  **What unmet needs is the young person trying to fulfill by considering gang involvement?** (e.g., safety, family, income, identity)\n2.  **Who are their positive influences?** Can these individuals be leveraged to support alternative choices?\n3.  **What are the realistic risks and consequences of gang involvement?** How can these be communicated without fear-mongering?\n4.  **What are their strengths and interests?** How can these be channeled into constructive activities or opportunities?\n\n### Recommended Approach\n1.  **Build Trust and Rapport**: Approach with genuine curiosity and empathy. Avoid judgment or lecturing. Start by listening to their perspective and validating their feelings.\n2.  **Explore Underlying Motivations**: Gently probe what draws them to the gang. Is it a sense of family, protection, or financial gain? Acknowledge these desires as valid human needs.\n3.  **Offer Concrete Alternatives**: Connect them to pro-social groups, mentorship programs, job training, educational opportunities, or recreational activities that can fulfill those same needs in a safe, constructive way.\n4.  **Share Lived Experience (if applicable)**: If you have personal experience with gang involvement or similar challenges, share your story of transformation and the positive outcomes of choosing a different path.\n5.  **Discuss Realities, Not Just Dangers**: Talk about the daily realities, restrictions, and long-term consequences of gang life, including trauma, incarceration, and loss of life, but frame it as empowering them with information to make informed choices.\n6.  **Reinforce Personal Agency**: Emphasize that they have the power to choose their path and that support is available for whatever positive direction they decide to take.\n\n### Follow-Up\n-   Maintain consistent, non-judgmental contact.\n-   Connect them to at least one tangible resource or positive activity within a week.\n-   Debrief with your supervisor to discuss strategies and personal well-being.\n\n*This guidance emphasizes meeting unmet needs and offering viable alternatives within a trauma-informed framework, aligning with CVI principles.*"""
        }
    },
    "trauma_reframing": {
        "default": """## Trauma-Informed Reframing

### Original vs. Reframed Language

Below is a demonstration of how to transform common messages into trauma-informed language that acknowledges stress, avoids blame, and reinforces personal agency.

---

**Original:** *"You need to stop hanging around those people. You're going to ruin your life if you keep making these choices."*

**Reframed:** *"I care about you and where your life is headed. I know the people around you feel like family — that bond is real. But I also see how much potential you have, and I want to make sure you have the chance to explore all your options. Can we talk about what you want your future to look like?"*

### Key Changes Explained

| Original Element | Issue | Reframed Approach |
|---|---|---|
| "You need to stop" | Directive and controlling | Expresses care and concern instead |
| "those people" | Dismissive of relationships | Acknowledges the bond while expanding perspective |
| "ruin your life" | Fear-based, shaming | Focuses on potential and possibility |
| "these choices" | Blaming, judgmental | Shifts to exploring options and agency |

### Principles Applied

1. **Lead with Care**: Start by expressing genuine concern rather than criticism.
2. **Acknowledge Reality**: Validate their experience and relationships rather than dismissing them.
3. **Focus on Strengths**: Highlight what they have going for them, not what they are doing wrong.
4. **Invite Dialogue**: End with a question that gives them agency rather than a command.
5. **Future-Oriented**: Point toward possibilities rather than dwelling on past mistakes.

### Additional Reframing Examples

| Instead of... | Try... |
|---|---|
| "You're throwing your life away" | "You have so much ahead of you — let's talk about what you want to build" |
| "If you don't change, you'll end up dead or in jail" | "I've seen what happens in these situations, and I don't want that for you because you matter" |
| "Why do you keep doing this?" | "Help me understand what's going on. I want to support you" |
| "You're being stupid" | "I know you're smart enough to see the bigger picture here" |

*Trauma-informed communication recognizes that behavior is often a response to unresolved pain, unmet needs, or survival strategies. Reframing is not about being soft — it is about being effective.*""",
        "samples": {}
    },
    "documentation": {
        "default": """## Intervention Documentation Summary

---

**Document Type:** Field Intervention Summary  
**Date:** [Date of Interaction]  
**Interrupter ID:** [Staff ID]  
**Location Type:** Community setting (outdoor)  
**Duration:** Approximately 60 minutes  

---

### Context
Outreach worker made contact with [Participant A] at a known community gathering location during routine outreach rounds. Participant presented as visibly stressed and disclosed concerns related to financial pressures. Participant also indicated that external individuals were applying social pressure related to these financial concerns.

### Intervention Activities
1. **Initial Engagement:** Outreach worker initiated conversation using rapport-based approach. Participant was receptive to dialogue.
2. **Active Listening:** Outreach worker provided extended active listening (approximately 40 minutes) to allow participant to express concerns fully.
3. **Needs Assessment:** Identified primary stressors as financial instability and peer pressure from external influences.
4. **Resource Discussion:** Discussed available community resources including employment assistance programs, financial literacy workshops, and emergency support services.
5. **Safety Planning:** Conducted informal safety assessment. No immediate threats identified, but ongoing monitoring recommended.

### Participant Response
Participant demonstrated increased calm over the course of the interaction. Body language shifted from tense and guarded to more open and relaxed. Participant expressed appreciation for the outreach worker's time and willingness to listen. Participant verbally agreed to a follow-up meeting.

### Follow-Up Actions
- [ ] Schedule follow-up contact within 24 hours
- [ ] Connect participant with employment assistance program
- [ ] Coordinate with team regarding ongoing outreach to this individual
- [ ] Monitor community dynamics related to reported peer pressure

### Notes
- Interaction occurred during routine outreach; no critical incident triggered this contact
- Participant has been engaged in program services previously and has an established rapport with outreach team
- No identifying information about third parties was disclosed or recorded
- Outreach worker to debrief with supervisor regarding reported peer pressure dynamics

---

*This summary follows program documentation standards. All identifying information has been replaced with placeholder brackets. This document is for internal program use only and should be stored according to organizational data security protocols.*""",
        "samples": {}
    },
    "reflection": {
        "default": """## Reflective Post-Intervention Analysis

### What Went Well
- **Presence and Availability:** You showed up when the community needed you. Being present for six hours demonstrates deep commitment and is itself an intervention.
- **Emotional Regulation:** Maintaining calm in a chaotic, emotionally charged environment is a significant professional skill. The fact that you were able to help some community members de-escalate shows your techniques are effective.
- **Relationship Maintenance:** By staying and engaging, you reinforced trust with the community. People will remember that you were there.

### Areas for Growth
- **Team Coordination:** Consider whether additional team members could have been called in to share the emotional and physical load. A six-hour solo response is unsustainable.
- **Structured Follow-Up:** Develop a follow-up protocol for the group that left angry. Their departure does not mean the intervention failed — it means the next phase of outreach needs to begin.
- **Setting Boundaries:** Reflect on whether there was a point where you could have transitioned responsibility to another team member or community resource.

### Reflective Questions
1. *"What was the moment I felt most effective, and what was I doing differently in that moment?"*
2. *"The group that left angry — what do I know about what they need? Who in my network can reach them?"*
3. *"Am I measuring my success by an impossible standard? Is 'calming some people down' actually a significant achievement in this context?"*
4. *"What would I tell a colleague who described this exact same situation to me?"*
5. *"What did I learn about this community today that I did not know before?"*

### Safety Considerations
- Assess whether the group that left angry poses a retaliation risk
- Coordinate with your team to monitor the situation over the next 48-72 hours
- Identify community leaders who can serve as additional points of contact

### Self-Care Recommendations
- **Immediate:** You described feeling exhausted. Honor that. Rest is not optional — it is a professional requirement for this work.
- **Within 24 Hours:** Debrief with a trusted colleague or supervisor. Do not process this alone.
- **This Week:** Engage in at least one activity that is purely restorative — something that fills your cup.
- **Ongoing:** Consider whether you have a regular self-care practice. Vicarious trauma is cumulative, and this work requires intentional recovery.

### Reframing Your Self-Doubt
The thought *"I'm unsure if I did enough"* is common among dedicated practitioners. Consider this reframe: **You responded to a shooting. You stayed for six hours. You helped people in their worst moment. That is not "not enough" — that is extraordinary.** The work is not finished, but your contribution today was meaningful and real.

*This reflective analysis is based on trauma-informed supervision frameworks. Discuss these reflections with your supervisor and use them to inform your ongoing professional development.*""",
        "samples": {}
    },
}

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
# API Key Detection — Hybrid Mode Logic
# ============================================================================


def get_api_key():
    """Retrieve the OpenAI API key from Streamlit secrets or environment."""
    # Check Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    # Fall back to environment variable (for local development)
    return os.environ.get("OPENAI_API_KEY", "")


def is_live_mode():
    """Check if a valid API key is available for live AI mode."""
    key = get_api_key()
    return bool(key and key.startswith("sk-") and len(key) > 20)


# ============================================================================
# Response Generation — Hybrid Mode
# ============================================================================


def generate_demo_response(user_input: str, tool_key: str) -> str:
    """Return a pre-built expert-crafted response for demo mode."""
    tool_responses = DEMO_RESPONSES.get(tool_key, {})

    # Check if user input matches any sample scenarios
    user_lower = user_input.lower()
    for keyword, response in tool_responses.get("samples", {}).items():
        if keyword in user_lower:
            return response

    # Return the default response for this tool
    return tool_responses.get("default", "Demo response not available for this tool.")


def generate_live_response(user_input: str, tool_key: str) -> str:
    """Generate a response using the live OpenAI API with the fine-tuned model."""
    tool = TOOLS[tool_key]
    full_prompt = tool["prompt_prefix"] + user_input

    try:
        from openai import OpenAI

        client = OpenAI(api_key=get_api_key())
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
        return (
            f"**Live AI Error:** {str(e)}\n\n"
            f"Falling back to demo mode...\n\n---\n\n"
            f"{generate_demo_response(user_input, tool_key)}"
        )


def generate_response(user_input: str, tool_key: str) -> str:
    """Generate a response using live AI or demo mode based on API key availability."""
    if is_live_mode():
        return generate_live_response(user_input, tool_key)
    else:
        return generate_demo_response(user_input, tool_key)


# ============================================================================
# Sidebar
# ============================================================================

with st.sidebar:
    st.markdown("## CVI AI Assistant")
    st.markdown("---")

    # Mode indicator
    if is_live_mode():
        st.markdown(
            '<div class="mode-badge-live"><strong>LIVE AI MODE</strong><br>'
            "Connected to fine-tuned GPT-4.1-mini model</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="mode-badge-demo"><strong>DEMO MODE</strong><br>'
            "Showing expert-crafted sample responses.<br>"
            "Add an OpenAI API key to activate live AI.</div>",
            unsafe_allow_html=True,
        )

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
    - **Mode**: {"Live AI" if is_live_mode() else "Demo (Pre-Built Responses)"}
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

# Mode Banner
if is_live_mode():
    st.markdown(
        """
    <div class="ethics-banner">
        <strong>Live AI Mode Active:</strong> Connected to the fine-tuned GPT-4.1-mini model. 
        All responses are generated in real-time using the CVI-specialized AI system.
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
    <div class="ethics-banner">
        <strong>Demo Mode Active:</strong> Displaying expert-crafted sample responses that demonstrate 
        the system's capabilities. These responses are based on the same CVI frameworks used to 
        fine-tune the AI model. To activate live AI responses, add an OpenAI API key in the 
        app settings or Streamlit Cloud Secrets.
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
    mode_label = "Live AI" if is_live_mode() else "Demo"
    st.markdown(
        f"""
    <div class="metric-card">
        <h2>{mode_label}</h2>
        <p>Current Mode</p>
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

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    with col_btn1:
        generate_btn = st.button(
            "Generate Response", type="primary", use_container_width=True
        )
    with col_btn2:
        demo_btn = st.button(
            "Show Demo Response", use_container_width=True
        )
    with col_btn3:
        clear_btn = st.button("Clear", use_container_width=False)

    # Generate response (live or demo based on mode)
    if generate_btn and user_input.strip():
        with st.spinner(
            "Generating trauma-informed response..."
            if is_live_mode()
            else "Loading expert-crafted response..."
        ):
            response = generate_response(user_input, selected_tool)
            st.session_state.interaction_count += 1

            # Store in message history
            st.session_state.messages.append(
                {
                    "tool": tool["title"],
                    "input": user_input,
                    "response": response,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "mode": "Live AI" if is_live_mode() else "Demo",
                }
            )

        st.markdown("### AI Response")
        if not is_live_mode():
            st.info(
                "This is a pre-built demo response showcasing the system's "
                "capabilities. Add an OpenAI API key to get personalized, "
                "real-time AI responses tailored to your specific scenario."
            )
        st.markdown(response)

        # Download option
        st.download_button(
            label="Download Response",
            data=f"Tool: {tool['title']}\n"
            f"Mode: {'Live AI' if is_live_mode() else 'Demo'}\n"
            f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"INPUT:\n{user_input}\n\nRESPONSE:\n{response}",
            file_name=f"cvi_response_{selected_tool}_{time.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

    elif generate_btn:
        st.warning("Please enter a scenario or text before generating a response.")

    # Show demo response button (always shows demo regardless of mode)
    if demo_btn:
        with st.spinner("Loading demo response..."):
            demo_response = generate_demo_response(
                user_input if user_input.strip() else "", selected_tool
            )
            st.session_state.interaction_count += 1

        st.markdown("### Demo Response")
        st.info(
            "This is a pre-built expert-crafted response demonstrating the "
            "system's trauma-informed approach."
        )
        st.markdown(demo_response)

    if clear_btn:
        st.rerun()

# ============================================================================
# Session History
# ============================================================================

if st.session_state.messages:
    st.markdown("---")
    st.markdown("## Session History")

    for i, msg in enumerate(reversed(st.session_state.messages)):
        mode_tag = f" [{msg.get('mode', 'N/A')}]" if 'mode' in msg else ""
        with st.expander(
            f"{msg['tool']}{mode_tag} — {msg['timestamp']}", expanded=(i == 0)
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
