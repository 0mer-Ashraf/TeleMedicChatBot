import streamlit as st

def landing_page():
    """
    Renders the landing page of the TeleMedicine app
    """
    # st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    
    # Hero section
    st.markdown("<h1 class='hero-title'>TeleMedicine AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Your Personal Health Companion</p>", unsafe_allow_html=True)
    
    # App description
    st.markdown("<h2>How TeleMedicine Can Help You</h2>", unsafe_allow_html=True)
    st.markdown("<p>TeleMedicine provides instant medical guidance through an AI-powered assistant. Simply describe your symptoms, and our assistant will help identify possible conditions and recommend next steps.</p>", unsafe_allow_html=True)
    
    # Features section
    st.markdown("<div class='features-container'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔍</div>
            <h3>Symptom Analysis</h3>
            <p>Describe your symptoms and get possible explanations based on medical knowledge.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🌐</div>
            <h3>Bilingual Support</h3>
            <p>Communicate in English or Spanish with our AI assistant.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⚕️</div>
            <h3>Health Guidance</h3>
            <p>Receive recommended next steps and when to seek professional medical help.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class='disclaimer'>
        <p><strong>Important:</strong> TeleMedicine is not a replacement for professional medical advice. 
        Always consult with a qualified healthcare provider for diagnosis and treatment.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Sign In to Get Started", type="primary", key="signin_btn"):
            st.session_state.page = "login"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Custom CSS for the landing page
    st.markdown(
        """
        <style>
        .stButton button {
            background-color: #f05454 !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 1.1rem !important;
            border-radius: 5px !important;
            transition: all 0.3s ease !important;
        }
        .stButton button:hover {
            background-color: #e03434 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }
        .centered-container {
            max-width: 1200px;
            margin: auto;
            padding: 2rem;
            text-align: center;
        }
        .hero-title {
            font-size: 3.5rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            color: #7f8c8d;
            margin-bottom: 3rem;
        }
        .app-description {
            text-align: left;
            margin-bottom: 3rem;
        }
        .features-container {
            margin: 2rem 0;
        }
        .feature-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            height: 100%;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .disclaimer {
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            border-radius: 4px;
            margin-top: 2rem;
        }
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .feature-card {
                width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
