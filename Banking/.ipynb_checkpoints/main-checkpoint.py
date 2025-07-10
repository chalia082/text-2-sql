import streamlit as st
from graph import app
from state import AgentState
from core.db_utils import run_query  # ✅ Make sure this file exists

# ✅ Always make this the first Streamlit call
st.set_page_config(page_title="Text-to-SQL Agent", layout="centered")

# 🧠 App UI
st.title("🔷 Text-to-SQL Agent")
st.markdown("Type your natural language question about the database:")

# 🔍 User input
user_input = st.text_input("📝 Query", "")

if user_input:
    with st.spinner("🔄 Processing..."):
        try:
            # ✅ Step 1: Create state and run the agent
            initial_state = AgentState(user_input=user_input)
            final_state_dict = app.invoke(initial_state.dict())
            final_state = AgentState(**final_state_dict)

            # ✅ Step 2: Show generated SQL
            if final_state.generated_sql and final_state.generated_sql.strip():
                st.markdown("### ✅ Generated SQL")
                st.code(final_state.generated_sql, language="sql")

                # ✅ Step 3: Run SQL and show result table
                try:
                    result_df = run_query(final_state.generated_sql)
                    st.markdown("### 📊 Query Result")
                    st.dataframe(result_df)
                except Exception as e:
                    st.error(f"❌ Error running query: {str(e)}")
            else:
                st.markdown("❌ No SQL result available.")

            # ✅ Step 4: Show debug info
            with st.expander("🔍 Debug Info"):
                st.write("**Detected Intent:**", final_state.detected_intent)
                st.write("**Relevant Columns:**", final_state.relevant_columns)
                st.write("**Relevant Tables:**", final_state.relevant_tables)
                st.code(final_state.generated_sql or "❌ No SQL generated", language="sql")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
