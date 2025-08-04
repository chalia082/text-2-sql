import streamlit as st
import pandas as pd
import time
from graph import create_graph
from state import AgentState
from core.db_utils import run_query

st.set_page_config(page_title="Text-to-SQL Batch Evaluation Dashboard", layout="wide")
st.title("Text-to-SQL Batch Evaluation Dashboard")

# Upload or enter questions
uploaded_file = st.file_uploader("Upload questions (txt or csv)", type=["txt", "csv"])
questions = []
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        questions = df.iloc[:, 0].dropna().astype(str).tolist()
    else:
        questions = uploaded_file.read().decode().splitlines()
        questions = [q.strip() for q in questions if q.strip()]
else:
    questions_text = st.text_area("Or paste questions (one per line):")
    if questions_text:
        questions = [q.strip() for q in questions_text.splitlines() if q.strip()]
        

app = create_graph()

# Batch evaluation function
def batch_evaluate(questions):
    results = []
    for q in questions:
        start = time.time()
        initial_state = AgentState(user_input=q)
        final_state_dict = app.invoke(initial_state.dict())
        final_state = AgentState(**final_state_dict)
        end = time.time()
        duration = end - start
        intent_success = final_state.detected_intent is not None
        sql_success = bool(final_state.generated_sql and final_state.generated_sql.strip())
        validation_success = final_state.validation_passed is True
        execution_success = final_state.execution_error is None
        if final_state.detected_intent == 'ask_question':
            overall_success = intent_success and sql_success and validation_success and execution_success
        else:
            overall_success = intent_success
        # Extract relevant tables/columns
        picked_tables = final_state.relevant_tables if final_state.relevant_tables else []
        picked_columns = final_state.relevant_columns if final_state.relevant_columns else []
        results.append({
            "question": q,
            "detected_intent": final_state.detected_intent,
            "picked_tables": ", ".join(picked_tables),
            "picked_columns": ", ".join(picked_columns),
            "generated_sql": final_state.generated_sql,
            "validation_passed": final_state.validation_passed,
            "execution_error": final_state.execution_error,
            "final_output": final_state.final_output,
            "time_taken": duration,
            "error": final_state.error,
            "intent_success": intent_success,
            "sql_success": sql_success,
            "validation_success": validation_success,
            "execution_success": execution_success,
            "overall_success": overall_success
        })
    return results

# Run batch evaluation and display results
eval_results = []
if questions and st.button("Run Batch Evaluation"):
    with st.spinner("Running batch evaluation..."):
        eval_results = batch_evaluate(questions)
    results_df = pd.DataFrame(eval_results)
    st.dataframe(results_df)

    # Filter for ask_question only for node accuracy
    ask_df = results_df[results_df['detected_intent'] == 'ask_question']
    fallback_df = results_df[results_df['detected_intent'] == 'fallback']
    greet_df = results_df[results_df['detected_intent'] == 'greet']

    # Summary stats
    st.markdown("### Summary")
    st.write(f"Total questions: {len(results_df)}")
    st.write(f"Average time per query: {results_df['time_taken'].mean():.2f} seconds")
    st.write(f"Intent detected: {results_df['intent_success'].mean()*100:.1f}%")
    sql_acc = ask_df['sql_success'].mean()*100 if not ask_df.empty else 0
    val_acc = ask_df['validation_success'].mean()*100 if not ask_df.empty else 0
    exec_acc = ask_df[ask_df['validation_success'] == True]['execution_success'].mean()*100 if not ask_df.empty else 0
    st.write(f"SQL generated (ask_question only): {sql_acc:.1f}%")
    st.write(f"Validation passed (ask_question only): {val_acc:.1f}%")
    st.write(f"Execution success (ask_question only): {exec_acc:.1f}%")
    overall_acc = results_df['overall_success'].mean()*100
    st.write(f"Overall accuracy: {overall_acc:.1f}%")

    # Bar chart for node accuracies
    chart_data = pd.DataFrame({
        'Accuracy (%)': [results_df['intent_success'].mean()*100, sql_acc, val_acc, exec_acc, overall_acc]
    }, index=['Intent', 'SQL Generation', 'Validation', 'Execution', 'Overall'])
    st.markdown("### Node-wise and Overall Accuracy")
    st.bar_chart(chart_data)

    # Show most common picked tables/columns
    st.markdown("### Most Common Picked Tables and Columns")
    if not ask_df.empty:
        all_tables = ", ".join(ask_df['picked_tables'].dropna())
        all_columns = ", ".join(ask_df['picked_columns'].dropna())
        table_counts = pd.Series([t.strip() for t in all_tables.split(",") if t.strip()]).value_counts()
        column_counts = pd.Series([c.strip() for c in all_columns.split(",") if c.strip()]).value_counts()
        st.write("**Tables:**")
        st.write(table_counts.head(10))
        st.write("**Columns:**")
        st.write(column_counts.head(10)) 