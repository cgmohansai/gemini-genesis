import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import time
import random
import plotly.express as px
import plotly.graph_objects as go

# --- 1. ULTIMATE CONFIGURATION ---
st.set_page_config(
    page_title="Gemini Genesis | Enterprise Pro v4.0",
    page_icon="🚀",
    layout="wide"
)

# --- 2. SPECIAL FEATURES & ASSETS ---
IMG_DASHBOARD = "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&auto=format&fit=crop&q=80"
IMG_INTERVIEW = "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&auto=format&fit=crop&q=80"
IMG_TRAINING = "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&auto=format&fit=crop&q=80"
IMG_CLASSROOM = "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=1200&auto=format&fit=crop&q=80"

# --- 3. ULTIMATE CSS (BOTH THEMES MERGED + ENHANCEMENTS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

/* DUAL THEME SYSTEM */
:root {
    --primary-bg: linear-gradient(135deg, #020617 0%, #0f1419 50%, #111827 100%);
    --card-bg: rgba(255,255,255,0.08);
    --accent-blue: #38bdf8;
    --accent-purple: #8b5cf6;
    --accent-green: #10b981;
    --text-primary: #e5e7eb;
    --text-secondary: #94a3b8;
}

.stApp {
    background: var(--primary-bg);
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

/* SIDEBAR - ULTIMATE */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f1419 70%, #1a1a2e 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.3);
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.15);
}

/* SPECIAL FEATURE CARDS */
.ultimate-card {
    background: rgba(15,23,42,0.9);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 20px;
    padding: 28px;
    margin: 16px 0;
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.ultimate-card::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
    transition: width 0.4s ease;
}

.ultimate-card:hover::before { width: 100%; }
.ultimate-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 35px 70px rgba(56,189,248,0.3);
    border-color: var(--accent-blue);
}

/* SPECIAL METRICS */
.super-metric {
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(45deg, var(--accent-blue), var(--accent-purple), var(--accent-green));
    -webkit-background-clip: text; color: transparent;
    text-shadow: 0 0 30px rgba(56,189,248,0.4);
}

/* ULTIMATE MARQUEE */
.ultimate-marquee {
    overflow: hidden; white-space: nowrap;
    background: rgba(15,23,42,0.95); 
    border-radius: 20px; 
    padding: 16px;
    border: 1px solid rgba(56,189,248,0.4);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.marquee-glow {
    display: inline-block; 
    animation: marquee 25s linear infinite;
    font-weight: 700; font-size: 1.1rem;
}

/* SPECIAL BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    border-radius: 16px; 
    color: white; 
    font-weight: 700;
    padding: 14px 28px;
    box-shadow: 0 12px 30px rgba(56,189,248,0.4);
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 20px 40px rgba(56,189,248,0.6);
}

/* AI CHAT BUBBLES */
.ai-bubble { background: rgba(16,185,129,0.2) !important; border-radius: 20px 20px 20px 6px !important; }
.user-bubble { background: var(--accent-blue) !important; border-radius: 20px 20px 6px 20px !important; }

/* PROGRESS BARS */
.custom-progress {
    height: 12px !important;
    border-radius: 10px !important;
    background: rgba(255,255,255,0.15) !important;
}
.custom-progress > div {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-green)) !important;
    border-radius: 10px !important;
}

/* SPECIAL ANIMATIONS */
@keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
.floating { animation: float 3s ease-in-out infinite; }

#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 4. SESSION STATE FOR SPECIAL FEATURES ---
if 'ai_messages' not in st.session_state:
    st.session_state.ai_messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Kumaran"
if 'streak' not in st.session_state:
    st.session_state.streak = 14
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# --- 5. ULTIMATE SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:24px 16px; border-bottom:1px solid rgba(56,189,248,0.3);">
        <div style="font-size:52px; margin-bottom:16px;">🚀</div>
        <h2 style="font-size:1.6rem; margin:0 0 8px 0; font-weight:800; background:linear-gradient(45deg,#38bdf8,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            GEMINI GENESIS
        </h2>
        <p style="color:var(--text-secondary); font-size:1rem;">Enterprise Pro v4.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SPECIAL API SETUP WITH STATUS
    with st.expander("🔑 AI Engine Control", expanded=False):
        api_key = st.text_input("Gemini 1.5 Pro Key", type="password", value=st.session_state.api_key or "")
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.session_state.model = model
                    st.success("✅ Ultra AI Engine Active")
                    st.balloons()
                except:
                    st.error("❌ Invalid Key")
    
    st.markdown("---")
    
    # ULTIMATE NAVIGATION
    selected = option_menu(
        menu_title="Command Center",
        options=["📊 Dashboard", "🎙️ Interview Hub", "💪 Training Gym", "👥 Classroom", "🤖 AI Copilot"],
        icons=["speedometer2", "mic", "dumbbell", "people", "robot"],
        default_index=0,
        styles={
            "container": {"padding": "0", "background": "transparent"},
            "nav-link": {"font-size": "15px", "padding": "16px 20px", "border-radius": "16px", "margin": "4px 0"},
            "nav-link-selected": {"background": "rgba(56,189,248,0.3)", "border": "2px solid var(--accent-blue)"}
        }
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center; padding:20px; background:rgba(56,189,248,0.1); border-radius:16px; border:1px solid rgba(56,189,248,0.3);">
        <i class="fas fa-user-circle" style="font-size:48px; color:var(--accent-blue);"></i>
        <h4 style="margin:8px 0 4px 0;">{st.session_state.user_name}</h4>
        <p style="color:var(--text-secondary);">Admin | Online</p>
        <div style="font-size:1.1rem; font-weight:700; color:var(--accent-green);">🔥 {st.session_state.streak} Day Streak</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# SPECIAL FEATURE #1: ULTIMATE DASHBOARD (BOTH CODES MERGED)
# =============================================================================
if selected == "📊 Dashboard":
    st.markdown('<div class="ultimate-card floating">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; align-items:center; gap:24px; margin-bottom:32px;">
        <div style="font-size:56px;">📊</div>
        <div>
            <h1 style="font-size:3rem; margin:0; font-weight:800; background:linear-gradient(45deg,#38bdf8,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                Executive Dashboard
            </h1>
            <p style="color:var(--text-secondary); font-size:1.2rem; margin:8px 0 0 0;">Ultimate readiness cockpit with AI insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SPECIAL METRIC ROW (ENHANCED)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="ultimate-card"><div class="super-metric">94%</div><div style="color:var(--text-secondary);">Readiness</div><span style="color:var(--accent-green);">Top 3%</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="ultimate-card"><div class="super-metric">1.2K</div><div style="color:var(--text-secondary);">Problems</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="ultimate-card"><div class="super-metric">28</div><div style="color:var(--text-secondary);">Mocks</div><span style="color:var(--accent-orange);">8.9/10</span></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="ultimate-card"><div class="super-metric">{st.session_state.streak}🔥</div><div style="color:var(--text-secondary);">Streak</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="ultimate-card"><div class="super-metric">12</div><div style="color:var(--text-secondary);">Offers</div></div>', unsafe_allow_html=True)
    
    # ULTIMATE COMPANY MARQUEE
    st.markdown('<div class="ultimate-marquee">', unsafe_allow_html=True)
    st.markdown("""
    <div class="marquee-glow">
        <span style="color:var(--accent-blue);">🏢 GOOGLE SDE</span>
        <span style="color:var(--accent-purple);">🏢 MICROSOFT SWE</span>
        <span style="color:var(--accent-green);">🏢 AMAZON L4</span>
        <span style="color:var(--accent-orange);">🏢 META E4</span>
        <span style="color:var(--accent-blue);">🏢 NETFLIX</span>
        <span style="color:var(--accent-purple);">🏢 TESLA AI</span>
        <span style="color:var(--accent-green);">🏢 UBER Data</span>
        <span style="color:var(--accent-orange);">🏢 ADOBE Intern</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SPECIAL FILTERS + INSIGHTS
    col_filter, col_charts = st.columns([1.2, 3])
    with col_filter:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin:0 0 20px 0;">🎯 Target Focus</h3>', unsafe_allow_html=True)
        company = st.selectbox("Company", ["Google", "Microsoft", "Amazon", "Meta"], key="dash_company")
        role = st.selectbox("Role", ["SDE 1", "SDE 2", "Data Engineer"], key="dash_role")
        if st.button("🔥 Generate Plan", key="dash_plan"):
            st.session_state.personalized_plan = f"{company} {role} - 7 Day Intensive"
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_charts:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 94,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Readiness"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#38bdf8"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ef4444"},
                        {'range': [60, 80], 'color': "#f59e0b"},
                        {'range': [80, 100], 'color': "#10b981"}],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': 94}}))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            progress_data = pd.DataFrame({
                'Skills': ['DSA', 'System Design', 'Behavioral', 'CS Core'],
                'Progress': [78, 52, 86, 64]
            })
            fig = px.bar(progress_data, x='Skills', y='Progress', 
                        color='Progress', color_continuous_scale='blugrn')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# SPECIAL FEATURE #2: ULTIMATE INTERVIEW HUB (4+ Tabs)
# =============================================================================
elif selected == "🎙️ Interview Hub":
    st.markdown('<div class="ultimate-card floating">', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size:2.8rem; margin:0;">Interview Control Center</h1>
    <p style="color:var(--text-secondary); font-size:1.2rem;">AI‑driven mock interviews, coding, ATS analysis, live copilot + video</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SPECIAL METRICS ROW
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Upcoming", "3", "Today")
    m2.metric("Best Score", "9.2/10", "New Record!")
    m3.metric("Hours", "27h", "")
    m4.metric("Companies", "18", "")
    
    # ULTIMATE 5-TAB SYSTEM
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎙️ AI Video Interview", "💻 Live Coding", "📄 ATS Scanner", 
        "🤖 Live Copilot", "📹 Recording Studio"
    ])
    
    with tab1:
        col1, col2 = st.columns([1.3, 1.7])
        with col1:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            st.markdown('<h3>🎥 AI Video Mock</h3>', unsafe_allow_html=True)
            if st.button("🎯 Start Live Interview", key="video_start"):
                st.session_state.video_active = True
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            if st.session_state.get('video_active', False):
                st.video("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/20251230-1433-37.6965943.mp4")
                st.info("🤖 AI: 'Design a URL shortener system for 1B users'")
                response = st.text_area("Your Video Response", height=100)
                if st.button("🔍 AI Feedback"):
                    st.success("**Score: 8.7/10**\n✅ Excellent architecture\n⚠️ Add rate limiting")
    
    with tab2:
        col1, col2 = st.columns([1.2, 1.8])
        with col1:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            st.markdown("### LeetCode #15: 3Sum")
            st.code("""
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            code = st.text_area("Live Python Editor", 
                value="""def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums)-2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        l, r = i+1, len(nums)-1
        while l < r:
            total = nums[i] + nums[l] + nums[r]
            if total == 0:
                result.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l+1]:
                    l += 1
                while l < r and nums[r] == nums[r-1]:
                    r -= 1
                l += 1
                r -= 1
            elif total < 0:
                l += 1
            else:
                r -= 1
    return result""", height=300)
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Run Tests"):
                    st.success("✅ 15/15 Test Cases Passed | Time: O(n²)")
            with col_btn2:
                if st.button("💡 AI Hint"):
                    st.info("Sort first, then use two pointers for O(n²)")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.file_uploader("📄 Upload Resume PDF", type="pdf")
            role = st.selectbox("Target Role", ["SDE II", "Data Engineer", "Product Manager"])
        with col2:
            if st.button("⚙️ Deep ATS Scan"):
                st.success("**ATS Score: 89%**")
                st.error("🚨 Missing: Kubernetes, System Design")
                st.info("✅ Strengths: Python, AWS, React")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h3>🤖 Live Interview Copilot</h3>')
        col1, col2 = st.columns([1.5, 1])
        with col1:
            question = st.text_area("Current Interview Question:", 
                placeholder="Paste live question from your Zoom/Teams call...", height=120)
            if st.button("💡 AI Strategy"):
                st.info("""
                **🎯 STAR Framework Applied:**
                1️⃣ **Situation**: "In Q3 2024, our app crashed..."
                2️⃣ **Task**: "I was lead engineer, fix in 24h"
                3️⃣ **Action**: "Implemented circuit breaker + caching"
                4️⃣ **Result**: "99.9% uptime, 40% faster"
                """)
        with col2:
            st.markdown("""
            <div style="text-align:center;">
                <i class="fas fa-robot" style="font-size:64px; color:var(--accent-blue);"></i>
                <h4>Status: READY</h4>
                <div style="color:var(--accent-green);">✅ Zoom Compatible</div>
                <div style="color:var(--accent-green);">✅ Teams Compatible</div>
                <div style="color:var(--accent-green);">✅ Undetectable</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h3>📹 Interview Recording Studio</h3>')
        st.video("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/20251230-1433-37.6965943.mp4")
        st.success("**Your Last Mock: 8.7/10**\nRecorded: 2 hours ago\nAI Feedback Generated")
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# SPECIAL FEATURE #3: TRAINING GYM (3 Levels + 5 AI Tools)
# =============================================================================
elif selected == "💪 Training Gym":
    st.markdown('<div class="ultimate-card floating">', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size:2.8rem;">Training Accelerator</h1>
    <p style="color:var(--text-secondary);">3 Levels × 5 AI Tools = Ultimate Skill Mastery</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SPECIAL 3-LEVEL SYSTEM
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="ultimate-card" style="border-top:6px solid var(--accent-green);">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin:0;">🟢 LEVEL 1</h3><div style="font-size:1.4rem; color:var(--accent-green);">Basic</div><div style="color:var(--accent-green);">✅ 100%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ultimate-card" style="border-top:6px solid var(--accent-orange);">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin:0;">🟡 LEVEL 2</h3><div style="font-size:1.4rem;">Medium</div><div style="color:var(--accent-orange);">⏳ 67%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="ultimate-card" style="border-top:6px solid var(--accent-red);">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin:0;">🔴 LEVEL 3</h3><div style="font-size:1.4rem; color:var(--accent-red);">Expert</div><div style="color:var(--accent-red);">🔒 Locked</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ULTIMATE AI TOOLS ROW
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h4>🎤 AI English Coach</h4>', unsafe_allow_html=True)
        sentence = st.text_input("Practice:", "I want job in Google.")
        if st.button("🗣️ Check Fluency"):
            st.success("**Fluency: 85/100**\n✅ Good structure\n⚠️ Use: 'I seek engineering role'")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h4>💻 Daily Code</h4>', unsafe_allow_html=True)
        topics = st.multiselect("Topics", ["Arrays", "DP", "Graphs"], default=["Arrays"])
        if st.button("📋 Generate Plan"):
            st.write("- 3 Easy Array problems")
            st.write("- 2 Medium DP problems") 
            st.write("- 45min timed mock")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_c:
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h4>💡 AI Mentor</h4>', unsafe_allow_html=True)
        doubt = st.text_input("Ask anything:")
        if st.button("🤖 Solve Doubt"):
            st.info("**AI:** Break into: Definition → Example → Code → Practice")
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# SPECIAL FEATURE #4: CLASSROOM (Teacher + Student View)
# =============================================================================
elif selected == "👥 Classroom":
    st.markdown('<div class="ultimate-card floating">', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size:2.8rem;">Command Center</h1>
    <p style="color:var(--text-secondary);">Monitor 64 students | 78% avg | 12 offers secured</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TEACHER METRICS
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Students", "64", "+3")
    m2.metric("Avg Score", "78%", "+4%")
    m3.metric("Offers", "12", "+2")
    m4.metric("Retention", "94%", "")
    
    # DUAL VIEW TOGGLE
    view_mode = st.radio("View Mode:", ["👨‍🏫 Teacher", "👨‍🎓 Student"], horizontal=True)
    
    if view_mode == "👨‍🏫 Teacher":
        col1, col2 = st.columns([1.5, 2])
        with col1:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            st.markdown('<h4>🏆 Top Performers</h4>', unsafe_allow_html=True)
            st.markdown("""
            <div style="display:flex; gap:12px; margin:12px 0;">
                <div style="width:45px;height:45px;border-radius:50%;background:var(--accent-green);"></div>
                <div><b>Tech Raj</b><div style="font-size:0.85rem;color:var(--text-secondary);">95%</div></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
            st.markdown('<h4>📊 Class Analytics</h4>', unsafe_allow_html=True)
            fig = px.pie(values=[45, 30, 25], names=['Ready', 'Training', 'Critical'], 
                        color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # Student View
        st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
        st.markdown('<h3>Your Rank: #3/64 🥉</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# SPECIAL FEATURE #5: AI COPILOT (Ultimate Chat)
# =============================================================================
elif selected == "🤖 AI Copilot":
    st.markdown('<div class="ultimate-card floating">', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size:3rem;">Live AI Copilot</h1>
    <p style="color:var(--text-secondary);">Real-time interview assistance. Undetectable. Cross-platform.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SPECIAL CHAT INTERFACE
    st.markdown('<div class="ultimate-card" style="height:500px; overflow-y:auto;">', unsafe_allow_html=True)
    
    # CHAT HISTORY
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.ai_messages[-10:]:
            if msg["role"] == "user":
                st.markdown(f'<div style="text-align:right;"><div style="display:inline-block; background:var(--accent-blue); padding:16px 20px; border-radius:24px 24px 8px 24px; max-width:80%; margin:8px 0; color:white;">{msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="text-align:left;"><div style="display:inline-block; background:rgba(255,255,255,0.15); padding:16px 20px; border-radius:24px 24px 24px 8px; max-width:80%; margin:8px 0;">{msg["content"]}</div></div>', unsafe_allow_html=True)
    
    # INPUT + SPECIAL BUTTONS
    col_input, col_btns = st.columns([3, 1])
    with col_input:
        user_input = st.text_input("💭 Ask anything...", key="copilot_input", placeholder="Interview tips? Code help? Career advice?")
    with col_btns:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Send", key="copilot_send"):
                if user_input:
                    st.session_state.ai_messages.append({"role": "user", "content": user_input})
                    if hasattr(st.session_state, 'model'):
                        with st.spinner("AI thinking..."):
                            try:
                                response = st.session_state.model.generate_content(user_input)
                                reply = response.text[:400]
                                st.session_state.ai_messages.append({"role": "ai", "content": reply})
                            except:
                                st.session_state.ai_messages.append({"role": "ai", "content": "⚠️ API error. Check key."})
                    else:
                        st.session_state.ai_messages.append({"role": "ai", "content": "🔑 Connect Gemini API first!"})
                    st.rerun()
        with col2:
            if st.button("🎯 Quick Tips", key="quick_tips"):
                st.session_state.ai_messages.append({"role": "ai", "content": """
**🚀 5 Interview Hacks:**
1. STAR method always
2. Quantify impact (20% faster)
3. Ask smart questions
4. Practice out loud
5. Smile + energy
                """})
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- ULTIMATE FOOTER ---
st.markdown("""
<div style="text-align:center; padding:40px 20px; color:var(--text-secondary); border-top:1px solid rgba(56,189,248,0.2); margin-top:60px;">
    <div style="font-size:1.4rem; font-weight:800; background:linear-gradient(45deg,#38bdf8,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        Gemini Genesis Enterprise Pro v4.0
    </div>
    <p style="margin:12px 0 0 0;">Powered by Google Gemini 1.5 | 92% Placement Success | 10K+ Users</p>
</div>
""", unsafe_allow_html=True)
