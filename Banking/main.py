import streamlit as st
from graph import create_graph
from state import AgentState
from core.db_utils import run_query
import numpy as np
from prompts.sql_generator_few_shot_prompts import FewShotPrompt
from core.embedding_loader import load_embedding_model

# ✅ Always make this the first Streamlit call
st.set_page_config(page_title="Text-to-SQL Agent", layout="centered")

app = create_graph()

# Inject minimal CSS for a clean, modern look
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #007bff; color: white; border-radius: 6px;}
    .stTextInput>div>input {border-radius: 8px;}
    .stDataFrame {border-radius: 8px; overflow: hidden;}
    .card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .subtitle {
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧠 App UI
st.markdown("""
# 🔷 Text-to-SQL Agent
<div class="subtitle">Ask questions about your banking database and get instant answers with SQL transparency.</div>
""", unsafe_allow_html=True)

# Use columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100px; width: 100%;'>
        <label style='font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; text-align: center; width: 100%;'>Enter your natural language query:</label>
    </div>
    """, unsafe_allow_html=True)
    # Custom CSS for larger text area
    st.markdown(
        """
        <style>
        textarea {
            font-size: 1.1rem !important;
            padding: 0.75rem 1rem !important;
            border-radius: 8px !important;
            width: 100% !important;
            min-width: 350px;
            max-width: 100%;
            min-height: 100px !important;
            resize: vertical !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    user_input = st.text_area("", "", key="nl_query", height=100)
    clear = st.button("Clear")
    if clear:
        st.rerun()

# Add custom CSS for navy blue table headers and index
st.markdown(
    """
    <style>
    .stDataFrame thead tr th {
        background-color: #001f4d !important;
        color: white !important;
    }
    .stDataFrame tbody th {
        background-color: #001f4d !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with col2:
    if user_input:
        with st.spinner("🔄 Processing..."):
            try:
                # ✅ Step 1: Create state and run the agent
                initial_state = AgentState(user_input=user_input)
                final_state_dict = app.invoke(initial_state.dict())
                final_state = AgentState(**final_state_dict)

                # ✅ Step 2: Show generated SQL (no empty box above)
                if final_state.generated_sql and final_state.generated_sql.strip():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### ✅ Generated SQL")
                    st.code(final_state.generated_sql, language="sql")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # ✅ Step 3: Run SQL and show result table
                    try:
                        result_df = run_query(final_state.generated_sql)
                        if result_df.empty:
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.warning("No data found in the database for this query.")
                            st.info("**Possible reason:** The table(s) involved may be empty, or the query filters are too strict.")
                            suggestion = suggest_similar_question(user_input)
                            st.markdown(f"**Try a similar question:**\n> {suggestion}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown("### 📊 Query Result")
                            st.dataframe(result_df)
                            st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.error(f"❌ Error running query: {str(e)}")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("❌ No SQL result available.")
                    st.markdown('</div>', unsafe_allow_html=True)

                # ✅ Step 4: Show debug info
                with st.expander("🔍 Debug Info"):
                    st.write("**Detected Intent:**", final_state.detected_intent)
                    st.write("**Relevant Columns:**", final_state.relevant_columns)
                    st.write("**Relevant Tables:**", final_state.relevant_tables)
                    st.code(final_state.generated_sql or "❌ No SQL generated", language="sql")

            except Exception as e:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.error(f"Unexpected error: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
