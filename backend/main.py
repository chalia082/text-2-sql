import streamlit as st
from graph import app
from state import AgentState
from core.db_utils import run_query  # ✅ Make sure this file exists
import numpy as np
from core.embedding_loader import load_embedding_model
from core.config_loader import load_config

# Load configuration
config = load_config()

# ✅ Always make this the first Streamlit call
st.set_page_config(
    page_title=config["settings"]["page_title"], 
    layout=config["settings"]["page_layout"]
)

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

# Helper function for suggesting similar questions
def suggest_similar_question(user_input: str) -> str:
    """Suggest a similar question based on the user input."""
    suggestions = {
        "account": "Show me all accounts with their balances",
        "customer": "List all customers and their account information",
        "loan": "Show me all loans and their details",
        "transaction": "Display recent transactions",
        "branch": "Show branch information and performance"
    }
    
    user_lower = user_input.lower()
    for keyword, suggestion in suggestions.items():
        if keyword in user_lower:
            return suggestion
    
    return "Show me all accounts with their balances"

with col2:
    if user_input:
        with st.spinner("🔄 Processing..."):
            try:
                # ✅ Step 1: Create state and run the agent
                initial_state = AgentState(user_input=user_input)
                final_state_dict = app.invoke(initial_state.dict())
                final_state = AgentState(**final_state_dict)

                # ✅ Debug info section
                with st.expander("🐞 Debug Info (Click to expand)"):
                    st.markdown("**Detected Intent:**")
                    st.code(final_state.detected_intent or "None", language="text")
                    
                    debug_info = getattr(final_state, 'debug_info', None)
                    if debug_info:
                        st.markdown("**User Query:**")
                        st.code(debug_info.get('user_query', ''), language="markdown")
                        if debug_info.get('reason'):
                            st.markdown("**Reason:**")
                            st.info(debug_info.get('reason', ''))
                        if debug_info.get('prompt'):
                            st.markdown("**Prompt sent to LLM:**")
                            st.code(debug_info.get('prompt', ''), language="markdown")
                        if debug_info.get('sql'):
                            st.markdown("**Generated SQL:**")
                            st.code(debug_info.get('sql', ''), language="sql")
                        if debug_info.get('llm_exception'):
                            st.markdown("**LLM Exception:**")
                            st.error(debug_info['llm_exception'])
                    else:
                        st.info("No debug information available. This might happen if the SQL generation step was skipped.")
                        if final_state.detected_intent in ["greet", "fallback"]:
                            st.warning(f"Intent '{final_state.detected_intent}' detected - SQL generation was skipped.")

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
                            # Add Get Insights button
                            if st.button("Get Insights"):
                                from graph import app, AgentState
                                state = AgentState(user_input=user_input, query_result=result_df)
                                from nodes.insights import insights_node
                                insights_state = insights_node.invoke(state)
                                st.markdown("---")
                                st.markdown("#### 💡 Insights")
                                st.info(insights_state.explanation)
                            # Add Visualize button
                            if st.button("Visualize"):
                                from graph import AgentState
                                from nodes.visualization import visualization_node
                                state = AgentState(user_input=user_input, query_result=result_df)
                                vis_state = visualization_node.invoke(state)
                                import json
                                try:
                                    # Split LLM response into explanation and JSON
                                    suggestion_lines = vis_state.suggestions.split('\n', 1)
                                    explanation = suggestion_lines[0].strip()
                                    suggestion_json = suggestion_lines[1].strip() if len(suggestion_lines) > 1 else '{}'
                                    suggestion = json.loads(suggestion_json)
                                    chart_type = suggestion.get("chart_type")
                                    top_n = suggestion.get("top_n")
                                    df_to_plot = result_df
                                    # Use top_n if suggested and value column is present
                                    if top_n and isinstance(top_n, int):
                                        if chart_type in ["bar", "line"] and suggestion.get("y"):
                                            df_to_plot = df_to_plot.sort_values(suggestion["y"], ascending=False).head(top_n)
                                        elif chart_type == "pie" and suggestion.get("values"):
                                            df_to_plot = df_to_plot.sort_values(suggestion["values"], ascending=False).head(top_n)
                                    st.markdown("---")
                                    st.markdown(f"#### 📈 Visualization: {chart_type.title()} Chart")
                                    st.info(explanation)
                                    if chart_type == "bar" and suggestion.get("x") and suggestion.get("y"):
                                        st.bar_chart(df_to_plot.set_index(suggestion["x"])[suggestion["y"]])
                                    elif chart_type == "line" and suggestion.get("x") and suggestion.get("y"):
                                        st.line_chart(df_to_plot.set_index(suggestion["x"])[suggestion["y"]])
                                    elif chart_type == "pie" and suggestion.get("labels") and suggestion.get("values"):
                                        import matplotlib.pyplot as plt
                                        fig, ax = plt.subplots()
                                        ax.pie(df_to_plot[suggestion["values"]], labels=df_to_plot[suggestion["labels"]], autopct='%1.1f%%')
                                        st.pyplot(fig)
                                    else:
                                        st.warning("LLM suggested an unsupported or incomplete chart format.")
                                except Exception as e:
                                    st.error(f"Visualization suggestion failed: {str(e)}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.error(f"❌ Query execution failed: {str(e)}")
                        st.markdown('</div>', unsafe_allow_html=True)

                # ✅ Step 4: Show validation errors if any
                elif final_state.validation_error:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.error(f"❌ SQL Validation Error: {final_state.validation_error}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # ✅ Step 5: Show execution errors if any
                elif final_state.execution_error:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.error(f"❌ Execution Error: {final_state.execution_error}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # ✅ Step 6: Show general errors if any
                elif final_state.error:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.error(f"❌ Error: {final_state.error}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # ✅ Step 7: Show final output if available
                elif final_state.final_output:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### 📊 Result")
                    st.markdown(final_state.final_output)
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
