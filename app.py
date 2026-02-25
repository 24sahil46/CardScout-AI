import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import os
from dotenv import load_dotenv, find_dotenv

# --- INITIALIZATION ---
# 1. Try to get keys from Hugging Face Secrets first
gemini_key = os.getenv("GEMINI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

# 2. If not found (running locally), load from api.env
if not gemini_key or not tavily_key:
    load_dotenv(find_dotenv("api.env"))
    gemini_key = os.getenv("GEMINI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

# 3. Configure Clients
if gemini_key and tavily_key:
    tavily = TavilyClient(api_key=tavily_key)
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Keys missing. Please set them in Hugging Face Settings > Secrets.")
    st.stop()

st.set_page_config(page_title="CardScout AI", page_icon="🕵️", layout="wide")
# --- CUSTOM FINTECH EXECUTIVE THEME (DARK MODE) ---
theme_css = """
<style>
/* Import modern font (Inter) to match the sleek UI */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* 1. Main Background: Deep Cinematic Blue */
[data-testid="stAppViewContainer"] {
    /* Replicates the centered deep blue glow fading into pitch black */
    background: radial-gradient(circle at 50% 50%, #0d3256 0%, #041221 60%, #010408 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: #E2E8F0;
}

/* Makes the top header transparent so the white bar disappears */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}

/* Extra safety to ensure no white bleeds through the edges */
.stApp {
    background-color: #010408 !important;
}

/* 2. Global Text Colors (Forcing white/light gray in dark mode) */
/* FIX: Removed 'span' from this list so we don't break Streamlit's native icons */
h1, h2, h3, h4, h5, p, label, [data-testid="stWidgetLabel"] p {
    color: #F8FAFC !important; 
    font-family: 'Inter', sans-serif !important;
}

/* Bulletproof backup to ensure icons stay as icons */
.material-symbols-rounded, .material-icons {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    font-weight: normal !important;
}

/* 3. The Cards (Containers): Dark elevated plates with BOLD WHITE borders */
div[data-testid="stVerticalBlockBorderWrapper"] > div,
.st-emotion-cache-1r6slb0, .st-emotion-cache-eqffof {
    background-color: rgba(23, 31, 50, 0.4) !important;
    backdrop-filter: blur(12px);
    
    /* FIX: Made border 6px thick (bold) and much brighter white (0.3 opacity) */
    border: 6px solid rgba(255, 255, 255, 0.3) !important; 
    
    border-radius: 16px !important;
    /* Increased shadow slightly to balance the bolder border */
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.8) !important; 
}

/* 4. Sidebar Customization: Solid dark navy */
[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* 5. Primary Buttons: Dark Coloured (Next, Battle Now) */
button[kind="primary"] {
    background-color: #171f32 !important; /* Sleek dark navy */
    color: #F8FAFC !important; /* White text */
    border: 1px solid #3b82f6 !important; /* Glowing blue accent border */
    border-radius: 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}

/* Fix text and icons inside the dark primary button */
button[kind="primary"] p, button[kind="primary"] span {
    color: #F8FAFC !important; 
}

/* Add a subtle blue glow when hovering */
button[kind="primary"]:hover {
    background-color: #1e293b !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
}

/* Fix for the + and - buttons on Number Inputs (Age, Salary, etc.) */
[data-testid="stNumberInputStepDown"], 
[data-testid="stNumberInputStepUp"] {
    background-color: #171f32 !important; /* Matches secondary buttons */
    color: #F8FAFC !important;
}

/* Ensures the actual + and - icons turn white so they are visible */
[data-testid="stNumberInputStepDown"] svg, 
[data-testid="stNumberInputStepUp"] svg {
    fill: #F8FAFC !important;
}

/* 6. Secondary Buttons: Dark pill-shaped (Like the "Download report" button) */
button[kind="secondary"] {
    background-color: #171f32 !important;
    color: #F8FAFC !important;
    border: 1px solid #2a354d !important;
    border-radius: 24px !important;
    transition: all 0.3s ease;
}
button[kind="secondary"]:hover {
    background-color: #1e293b !important;
    border-color: #3b82f6 !important;
}

/* --- 7. UNIFIED INPUTS & BORDERS --- */

/* Main Wrappers (Text typing area and Selectboxes) */
div[data-baseweb="input"] > div, 
div[data-baseweb="select"] > div {
    background-color: #171f32 !important; 
    border: 1px solid #4a5568 !important; /* Unified slate border */
    border-radius: 8px !important;
    box-shadow: none !important; /* Kills the default Streamlit white border glow */
}

/* Force Text Color in Text & Number Inputs to white */
div[data-baseweb="input"] input {
    background-color: transparent !important; 
    color: #F8FAFC !important; 
}

/* Make placeholder text ("Enter your name") visible in text inputs */
div[data-baseweb="input"] input::placeholder {
    color: #F8FAFC !important; 
    opacity: 0.6 !important; /* Slightly dimmed so it looks like a placeholder */
}

/* Force Number Input + and - buttons to match the exact same border */
[data-testid="stNumberInputStepDown"], 
[data-testid="stNumberInputStepUp"] {
    background-color: #171f32 !important; 
    color: #F8FAFC !important;
    border: 1px solid #4a5568 !important; /* Matches the selectbox border exactly */
    border-radius: 8px !important;
}

/* Add a cool blue highlight when a user clicks/hovers the + or - buttons */
[data-testid="stNumberInputStepDown"]:hover, 
[data-testid="stNumberInputStepUp"]:hover {
    background-color: #2a354d !important;
    border: 1px solid #3b82f6 !important; /* Glowing blue accent */
}

/* Force Text Color in Selectboxes to be bright white */
div[data-baseweb="select"] div, 
div[data-baseweb="select"] span {
    color: #F8FAFC !important;
}
div[data-baseweb="select"] > div {
    background-color: #171f32 !important;
}
div[data-baseweb="select"] svg {
    fill: #F8FAFC !important;
}

/* --- RESTORED FIX: THE DROPDOWN MENU POPOVER --- */
/* Force every layer of the floating menu to be dark navy */
div[data-baseweb="popover"] > div, 
div[data-baseweb="popover"] > div > div,
ul[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #171f32 !important; 
    border-radius: 8px !important;
}

/* The actual list items (Salaried, Business Owner, etc.) */
li[role="option"] {
    background-color: #171f32 !important;
    color: #F8FAFC !important;
}

/* Highlight on hover/select */
li[role="option"]:hover, 
li[role="option"][aria-selected="true"],
li[role="option"]:focus {
    background-color: #2a354d !important;
    color: #FFFFFF !important;
}

/* --- RESTORED FIX: MULTISELECT TAGS (PAGE 2) --- */
/* Ensures selected items in the Bank/Rewards boxes look like proper dark mode chips */
span[data-baseweb="tag"] {
    background-color: #2a354d !important;
    color: #F8FAFC !important;
    border: 1px solid #3b82f6 !important; 
}
span[data-baseweb="tag"] span, 
span[data-baseweb="tag"] svg {
    color: #F8FAFC !important;
    fill: #F8FAFC !important;
}

/* 8. Info Box & Accents: Neon vibes */
[data-testid="stInfo"] {
    background-color: rgba(6, 182, 212, 0.1) !important;
    border-left-color: #06B6D4 !important; /* Neon Cyan */
}
[data-testid="stInfo"] p {
    color: #06B6D4 !important;
}

/* Make Dashboard Metric numbers pop with Neon Green */
[data-testid="stMetricValue"] {
    color: #10B981 !important; 
}

/* --- 9. STATUS & LOADING WIDGETS (Page 3 Fix) --- */
/* Force the 'Scouting in progress' box to be dark navy */
[data-testid="stStatusWidget"] > div, 
[data-testid="stExpander"] {
    background-color: #171f32 !important; 
    border: 1px solid #4a5568 !important; 
    border-radius: 8px !important;
}

/* Ensure the text and icons inside the status box stay bright white */
[data-testid="stStatusWidget"] summary,
[data-testid="stStatusWidget"] summary p,
[data-testid="stStatusWidget"] summary span,
[data-testid="stStatusWidget"] div[data-testid="stText"],
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #F8FAFC !important;
}

/* Make sure the little spinning loading wheel adopts the white/blue theme */
[data-testid="stStatusWidget"] [data-testid="stSpinner"] circle {
    stroke: #06B6D4 !important; /* Neon Cyan spinner */
}
/* --- 10. DIALOG & POPUP FIX (Battleground Dark Mode) --- */
/* Forces the popup container and the battleground text to be readable */
div[data-testid="stDialog"] div[role="dialog"] {
    background-color: #0b121e !important; /* Deep Midnight Blue */
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
}

/* Fixes the "invisible" text inside the dialog */
div[data-testid="stDialog"] .stMarkdown, 
div[data-testid="stDialog"] .stMarkdown p, 
div[data-testid="stDialog"] .stMarkdown span,
div[data-testid="stDialog"] .stMarkdown li,
div[data-testid="stDialog"] h1, 
div[data-testid="stDialog"] h2, 
div[data-testid="stDialog"] h3 {
    color: #FFFFFF !important;
    opacity: 1 !important; /* Forces the text to be solid, not faint */
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Style the comparison table inside the popup to be dark with borders */
div[data-testid="stDialog"] table {
    background-color: #171f32 !important;
    color: #F8FAFC !important;
    border: 1px solid #4a5568 !important;
    border-radius: 8px !important;
}

div[data-testid="stDialog"] th {
    background-color: #1e293b !important;
    color: #06B6D4 !important; /* Neon Cyan Headers */
}

/* Ensure the 'Close Analysis' button area doesn't turn white */
div[data-testid="stDialog"] [data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}
/* --- 11. TABLE ENHANCEMENTS (Card Name Highlighting) --- */
/* Highlights the Card Names in the top row of comparison tables */
table th {
    color: #06B6D4 !important; /* Neon Cyan for professional pop */
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background-color: rgba(6, 182, 212, 0.05) !important; /* Subtle glow effect */
    border-bottom: 2px solid #06B6D4 !important; /* Defines the header more sharply */
}

/* Ensures the feature labels (left column) and data (other cells) stay bright white */
table td {
    color: #F8FAFC !important;
    font-size: 0.95rem !important;
    opacity: 1 !important;
}

/* Forces the "Scouting" status bar to be dark */
div[data-testid="status_bar"] {
    background-color: #0b121e !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    color: #ffffff !important;
    box-shadow: none !important;
}

/* Colors the spinner and magnifying glass Neon Cyan */
div[data-testid="status_bar"] svg {
    fill: #06B6D4 !important;
}

/* Ensures text inside the dark bar is white */
div[data-testid="status_bar"] div {
    color: #ffffff !important;
}



</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)


# Navigation Logic
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- PAGE 1: PROFILE SCOUT ---
if st.session_state.step == 1:
    # Get current data for pre-filling
    data = st.session_state.user_data
    
    # Centering Logic: Create 3 columns, put content in the middle one
    _, center_column, _ = st.columns([1, 2, 1]) 
    
    with center_column:
        # Wrap the entire page content in a single card
        with st.container(border=True):
            st.markdown("""
        <style>
        @keyframes glow {
            0% { text-shadow: 0 0 10px rgba(6, 182, 212, 0.2), 0 0 20px rgba(6, 182, 212, 0.1); }
            50% { text-shadow: 0 0 20px rgba(6, 182, 212, 0.5), 0 0 30px rgba(16, 185, 129, 0.3); }
            100% { text-shadow: 0 0 10px rgba(6, 182, 212, 0.2), 0 0 20px rgba(6, 182, 212, 0.1); }
        }
        .glow-text {
            font-size: 5.5rem; 
            font-weight: 900; 
            margin-bottom: 0; 
            padding-bottom: 0; 
            background: linear-gradient(90deg, #06B6D4, #10B981); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            animation: glow 3s ease-in-out infinite;
            filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.5));
        }
        </style>
        
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 class="glow-text">🕵️ CardScout</h1>
            <p style="font-size: 1.1rem; color: #94a3b8; letter-spacing: 2px; font-weight: 500; margin-top: 5px; opacity: 0.9;">
                SMART DECISIONS, SMARTER REWARDS.
            </p>
        </div>
    """, unsafe_allow_html=True)
            st.info("Step 1: Basic Information")
            
            # Pre-filled inputs using data.get()
            name = st.text_input("What should we call you?", value=data.get('name', ""), placeholder="Enter your name")
            age = st.number_input("Age", min_value=18, max_value=75, value=data.get('age', 18))
            
            # Occupation Logic with index persistence
            occ_options = ["Salaried", "Self-employed Professional (Doc/CA)", "Business Owner", "Student", "Other..."]
            prev_occ = data.get('occ')
            # Calculate index: if prev_occ is not in list (like None), index is None to show placeholder
            occ_index = occ_options.index(prev_occ) if prev_occ in occ_options else None
            
            occ_choice = st.selectbox(
                "Professional Profile",
                options=occ_options,
                index=occ_index,
                placeholder="Select Profile...",
            )
            
            if occ_choice == "Other...":
                occ = st.text_input("Please specify your occupation:", value=data.get('occ', "") if prev_occ not in occ_options else "")
            else:
                occ = occ_choice

            # Tenure with index persistence
            tenure_options = ["Less than 6 Months", "6 - 12 Months", "1 - 2 Years", "More than 2 Years"]
            prev_tenure = data.get('tenure', "Less than 6 Months")
            tenure_index = tenure_options.index(prev_tenure) if prev_tenure in tenure_options else 0
            tenure = st.selectbox("Employment Stability", tenure_options, index=tenure_index)

            income = st.number_input("Monthly In-hand Salary (₹)", min_value=10000, value=data.get('income', 50000), step=5000)
            
            # Credit Radio with index persistence
            credit_options = ["< 700", "700 - 750", "> 750","Don't Know"]
            prev_credit = data.get('credit', "< 700")
            credit_index = credit_options.index(prev_credit) if prev_credit in credit_options else 0
            credit = st.radio("Estimated Credit Score", credit_options, index=credit_index, horizontal=True)

            st.divider()
            
            # Minimalist 'Next' Button now inside the card
            col1, col2 = st.columns([5, 1])
            if col2.button("Next", icon=":material/arrow_forward:"):
                # ADDED VALIDATION: Ensure a profile is selected before moving to Page 2
                if not name: 
                    st.error("Please enter your name.")
                elif occ_choice is None:
                    st.error("Please select a Professional Profile to proceed.")
                elif occ_choice == "Other..." and not occ:
                    st.error("Please specify your occupation.")
                else:
                    st.session_state.user_data.update({
                        "name": name, 
                        "age": age, 
                        "occ": occ, 
                        "tenure": tenure,
                        "income": income, 
                        "credit": credit
                    })
                    st.session_state.step = 2
                    st.rerun()

# --- PAGE 2: REWARDS BLUEPRINT ---
elif st.session_state.step == 2:
    data = st.session_state.user_data
    _, center_column, _ = st.columns([1, 2, 1])
    
    with center_column:
        # Wrap the entire page content in a single card
        with st.container(border=True):
            st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h4 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0; padding-bottom: 0;">
            📊 <span style="background: linear-gradient(90deg, #3b82f6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent !important;">Expense Blueprint</span>
        </h4>
    </div>
""", unsafe_allow_html=True)
            
            st.info("Step 2: Map your primary spending categories to help in calculating your maximum potential rewards.")
            
            # Initialize spend values from existing data if possible
            spend_values = data.get('spending_categories', {})

            st.markdown("### 🔍 Select Main Preferences")
            
            categories = {
                "Travel & Forex": "t_in",
                "Online Shopping": "s_in",
                "Lifestyle (Dining & Movies)": "l_in",
                "Essentials (Groceries & Quick Commerce)": "e_in",
                "Utilities & Rent": "u_in",
                "Transport (Fuel & UPI)": "tr_in"
            }

            for label, key in categories.items():
                if st.checkbox(label, key=f"cb_{key}", value=label in spend_values):
                    spend_values[label] = st.number_input(
                        f"Monthly {label} Spend (₹)", min_value=0, value=spend_values.get(label, 2000), step=500, key=key
                    )

            st.divider()
            st.markdown("### ➕ Custom Categories")
            
            if "custom_rows" not in st.session_state:
                st.session_state.custom_rows = 0

            for i in range(st.session_state.custom_rows):
                col1, col2 = st.columns([2, 1])
                custom_name = col1.text_input(f"Category Name {i+1}", key=f"cust_name_{i}")
                custom_amt = col2.number_input(f"Spend (₹)", min_value=0, value=1000, step=500, key=f"cust_amt_{i}")
                if custom_name:
                    spend_values[custom_name] = custom_amt

            if st.button("Add Other Category", icon=":material/add:"):
                st.session_state.custom_rows += 1
                st.rerun()

            st.divider()
            st.markdown("### 🏦 Banking & Existing Cards")
            bank_col, card_col = st.columns(2)
            
            with bank_col:
                existing_bank = st.multiselect(
                    "Current Bank Relation(s)",
                    ["HDFC", "ICICI", "SBI", "Axis", "Kotak", "Other"],
                    default=data.get('existing_banks', []),
                    help="Bank where you already have a Savings/Salary account."
                )
            
            with card_col:
                has_card = st.radio("Do you own a credit card?", ["No", "Yes"], index=1 if data.get('existing_card', "None") != "None" else 0, horizontal=True)
                if has_card == "Yes":
                    current_card_name = st.text_input("Enter the name of your current card:", value=data.get('existing_card', ""))
                else:
                    current_card_name = "None"

            st.divider()
            st.markdown("### 🎯 Reward Type Priority")

            reward_type = st.multiselect(
                "How do you prefer to be rewarded?",
                ["Direct Cashback", "Air Miles & Travel", "Reward Points (Shopping)", "Premium Lounge Access"],
                default=data.get('reward_type', []) 
            )

            st.divider()
            st.markdown("### 💰 Fee Preference") 
            pref_options = ["Lifetime Free (LTF) Only", "High Rewards (Willing to pay fees)", "Any"]
            prev_pref = data.get('pref', "Any")
            pref_index = pref_options.index(prev_pref) if prev_pref in pref_options else 2
            pref = st.radio("Select your priority:", pref_options, index=pref_index, horizontal=True, label_visibility="collapsed")

            st.divider()
            col_back, col_next = st.columns([1, 5])
            
            if col_back.button("Back", icon=":material/arrow_back:"):
                st.session_state.step = 1
                st.rerun()
                
            if col_next.button("Next", type="primary", icon=":material/arrow_forward:"):
                st.session_state.user_data.update({
                    "spending_categories": spend_values,
                    "existing_banks": existing_bank,
                    "existing_card": current_card_name,
                    "reward_type": reward_type,
                    "pref": pref
                })
                # Set step and RERUN immediately to clear this UI
                st.session_state.step = 3
                st.rerun()
                
# --- PAGE 3: THE PODIUM & AI DASHBOARD ---
elif st.session_state.step == 3:
    data = st.session_state.user_data
    spends = data.get('spending_categories', {})
    
    # 1. Wide Layout Title
    _, center_column, _ = st.columns([0.5, 3, 0.5])
    
    with center_column:
        # RENDER TITLE FIRST - This ensures the dark background is active
        st.markdown("""
            <div style="text-align: center; margin-bottom: 25px;">
                <h4 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 0; padding-bottom: 0; white-space: nowrap;">
                    🧭 <span style="background: linear-gradient(90deg, #3b82f6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent !important;">
                        CardScout's Intelligence Hub
                    </span>
                </h4>
            </div>
        """, unsafe_allow_html=True)

        # 2. THE ULTIMATE FIX: Buffered & Manually Darkened Status Bar
        if "final_recommendation" not in st.session_state:
            import time
            # Forces the dark dashboard layout to "settle" first
            time.sleep(0.1) 
            
            
            status_container = st.empty()
            with status_container.status("🔍 Analyzing your financial roadmap...", expanded=True) as status_bar:
                try:
                    query = f"Best cards India 2026 for {data['occ']} with {data['income']} income."
                    web_data = tavily.search(query=query, search_depth="advanced")
                    prompt = f"Advisor Mode. User Profile: {data}. Web Context: {web_data}. Provide Top 5 Recommendations."
                    response = model.generate_content(prompt)
                    
                    st.session_state.final_recommendation = response.text
                    status_bar.update(label="✅ Roadmap Generated!", state="complete", expanded=False)
                    
                    # Clean up the UI entirely after completion
                    status_container.empty()
                    st.rerun() 
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
                    st.stop()

    # 1. SIDEBAR SNAPSHOT
    with st.sidebar:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(6, 182, 212, 0.1)); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-bottom: 20px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 5px;">👤</div>
                <div style="color: #F8FAFC; font-weight: 700; font-size: 1.2rem; letter-spacing: 0.5px;">{data.get('name', 'User').upper()}</div>
                <div style="display: inline-block; background: #06B6D4; color: #0b121e; font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 20px; text-transform: uppercase; margin-top: 5px;">Verified Profile</div>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("👤 Profile Snapshot")
        with st.container(border=True):
            st.write(f"**Name:** {data.get('name', 'User')}")
            st.write(f"**Age:** {data.get('age', 'N/A')}")
            st.write(f"**Occupation:** {data.get('occ', 'N/A')}")
            st.write(f"**Stability:** {data.get('tenure', 'N/A')}")
            st.write(f"**Monthly Income:** ₹{data.get('income', 0):,}")
            st.write(f"**Credit Score:** {data.get('credit', 'N/A')}")
        
        st.subheader("🏦 Financial Context")
        with st.container(border=True):
            banks = data.get('existing_banks', [])
            st.write(f"**Relation Banks:** {', '.join(banks) if banks else 'None'}")
            st.write(f"**Current Card:** {data.get('existing_card', 'None')}")
            st.write(f"**Reward Pref:** {', '.join(data.get('reward_type', ['None']))}")
            st.write(f"**Fee Pref:** {data.get('pref', 'Any')}")

        if spends:
            st.subheader("📊 Spending Focus")
            with st.container(border=True):
                for cat, amt in spends.items():
                    st.write(f"**{cat}:** ₹{amt:,}")

        st.divider()
        if st.button("Edit Profile", icon=":material/edit:", use_container_width=True):
            if "final_recommendation" in st.session_state:
                del st.session_state.final_recommendation
            st.session_state.step = 1
            st.rerun()

    # --- BATTLEGROUND POPUP ---
    @st.dialog("⚔️ Card Battle: Peer-to-Peer Analysis", width="large")
    def battle_popup(entered_card, original_recommendation, user_context):
        st.write(f"### 🏆 Our Top Pick vs. {entered_card}")
        with st.spinner("Analyzing battle metrics..."):
            battle_prompt = f"Expert Advisor Mode. Profile: {user_context}. Original podium: {original_recommendation}. Compare {entered_card} against the #1 card and explain why our pick is better."
            try:
                response = model.generate_content(battle_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
        if st.button("Close Analysis", use_container_width=True):
            st.rerun()

    col_rewards, col_odds, col_battle = st.columns(3, gap="medium")

    with col_rewards:
        with st.container(border=True):
            st.subheader("💰 Reward Potential")
            total_monthly_spend = sum(spends.values()) if spends else 0
            annual_savings = (total_monthly_spend * 0.03) * 12 
            st.metric(label="Total Annual Savings", value=f"₹{int(annual_savings):,}", delta="Optimized Rewards")
            st.info(f"On ₹{int(total_monthly_spend):,} monthly spend.")

    with col_odds:
        with st.container(border=True):
            st.subheader("🎯 Approval Odds")
            score = data.get('credit', '< 700')
            tenure = data.get('tenure', 'Less than 6 Months')
            odds, status, color = ("35%", "Challenging", "inverse") if score == "< 700" else \
                                  ("95%", "Excellent", "normal") if score == "> 750" and "More than" in tenure else \
                                  ("65%", "Moderate", "normal")
            st.metric(label="Likelihood for Top Pick", value=odds, delta=status, delta_color=color)
            st.progress(int(odds.replace("%","")) / 100)
            st.caption(f"Based on {score} score & {tenure} tenure.")

    with col_battle:
        with st.container(border=True):
            st.subheader("🤖 The Battleground")
            st.write("Compare cards vs. Our Top pick.")
            user_card = st.text_input("Enter card name:", key="battle_input")
            if st.button("Battle Now", type="primary", use_container_width=True):
                if user_card:
                    battle_popup(user_card, st.session_state.final_recommendation, data)

    # --- THE STRATEGIC ROADMAP SECTION ---
    st.markdown("---")
    if "final_recommendation" in st.session_state:
        st.markdown(f"""
            <div style="margin-top: 10px; margin-bottom: 5px;">
                <h2 style="color: #F8FAFC; font-size: 2rem; font-weight: 700; border-left: 5px solid #06B6D4; padding-left: 15px; line-height: 1.2;">
                    Strategic Credit Acquisition Roadmap
                </h2>
                <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 5px; margin-left: 20px; opacity: 0.8;">
                    Personalized card selection optimized for {data.get('name', 'your')} financial profile and goals.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        name = data.get('name', 'User')
        clean_report = st.session_state.final_recommendation.strip()
        clean_report = clean_report.replace(f"Top 5 Podium Recommendations for {name}", "")
        clean_report = clean_report.replace(f"for {name}", "") 
        clean_report = clean_report.replace("### Top 5 Podium Recommendations", "")
        st.markdown(clean_report.strip())

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    if c1.button("Start New Scout", use_container_width=True, icon=":material/refresh:"):
        if "final_recommendation" in st.session_state:
            del st.session_state.final_recommendation
        st.session_state.step = 1
        st.rerun()


    # --- PDF GENERATOR ---
    pdf_output = None
    try:
        from fpdf import FPDF
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.set_margins(10, 10, 10); pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "CardScout AI: Strategic Report", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        raw_text = st.session_state.final_recommendation.replace("₹", "Rs.").replace("**", "").replace("*", "")
        lines = raw_text.split('\n')
        table_data = []; in_table = False
        
        for line in lines:
            line_str = line.strip()
            if line_str.count('|') >= 2:
                in_table = True
                if '---' in line_str: continue 
                cells = [c.strip() for c in line_str.strip('|').split('|')]
                if cells: table_data.append(cells)
            else:
                if in_table and len(table_data) > 0:
                    max_cols = max(len(r) for r in table_data)
                    for r in table_data:
                        while len(r) < max_cols: r.append("")
                    try:
                        pdf.set_font("helvetica", size=7)
                        with pdf.table(text_align="LEFT", width=277) as table:
                            for i, row_data in enumerate(table_data):
                                pdf.set_font("helvetica", "B" if i == 0 else "", 7)
                                row = table.row()
                                for cell_data in row_data: row.cell(cell_data)
                    except Exception:
                        pdf.set_font("helvetica", size=9)
                        for r in table_data:
                            pdf.multi_cell(0, 6, " | ".join([c for c in r if c]))
                            pdf.ln(1)
                    pdf.ln(5); table_data = []; in_table = False
                
                pdf.set_font("helvetica", size=10)
                if line_str == "": pdf.ln(4)
                else: pdf.multi_cell(0, 6, line_str)
        pdf_output = bytes(pdf.output())
    except Exception:
        try:
            from fpdf import FPDF
            emergency_pdf = FPDF(); emergency_pdf.add_page(); emergency_pdf.set_font("Arial", size=12)
            emergency_pdf.multi_cell(0, 10, st.session_state.final_recommendation.replace("₹", "Rs."))
            pdf_output = bytes(emergency_pdf.output())
        except: pdf_output = None

    if pdf_output:
        c2.download_button("📥 Download Report", data=pdf_output, file_name=f"CardScout_{data.get('name')}.pdf", mime="application/pdf", use_container_width=True)
    else:
        c2.button("⚠️ PDF Error", disabled=True, use_container_width=True)
        
    c3.button("Share with Expert", use_container_width=True, icon=":material/share:", disabled=True)





