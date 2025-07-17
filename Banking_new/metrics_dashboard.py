import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from nodes.sql_generator import generate_sql
from state import AgentState
from nodes.intent_classifier import detect_intent
from nodes.sql_validator import validate_sql
from nodes.sql_executor import execute_sql_query
from nodes.formatter import format_dataframe_safely

# Page configuration
st.set_page_config(
    page_title="Text2SQL Pipeline Metrics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }
    .success-high {
        color: #27ae60;
        font-weight: 600;
    }
    .success-medium {
        color: #f39c12;
        font-weight: 600;
    }
    .success-low {
        color: #e74c3c;
        font-weight: 600;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4 0%, #2980b9 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Text2SQL Pipeline Metrics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("Enter your questions below and run the pipeline to analyze performance across all nodes.")
    
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Paste 10+ questions (one per line)
    2. Click 'Run Pipeline' 
    3. View metrics and detailed results
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="section-header">📝 Input Questions</h2>', unsafe_allow_html=True)
    questions_input = st.text_area(
        'Enter your questions here:',
        height=300,
        placeholder="Example:\nShow me all customers\nWhat are the account balances?\nFind transactions above $1000"
    )

with col2:
    st.markdown('<h2 class="section-header">🚀 Pipeline Status</h2>', unsafe_allow_html=True)
    run_button = st.button('▶️ Run Pipeline', use_container_width=True)
    
    if not questions_input.strip():
        st.info("Please enter some questions to begin analysis.")
        st.stop()

if run_button and questions_input.strip():
    with st.spinner('🔄 Running pipeline analysis...'):
        questions = [q.strip() for q in questions_input.split('\n') if q.strip()]
        
        if len(questions) < 10:
            st.warning(f"⚠️ Only {len(questions)} questions provided. For better analysis, consider using 10+ questions.")
        
        results = []
        progress_bar = st.progress(0)
        
        for i, q in enumerate(questions):
            # Intent detection
            intent_pred = detect_intent(q)
            intent_success = bool(intent_pred and intent_pred != "fallback")
            
            # Table/column selection and SQL generation
            state = AgentState(user_input=q)
            state = generate_sql(state)
            tables_pred = state.relevant_tables or []
            columns_pred = state.relevant_columns or []
            value_mapping_pred = getattr(state, 'value_mapping', {}) or {}
            sql_pred = state.generated_sql or ''
            table_success = bool(tables_pred)
            column_success = bool(columns_pred)
            sql_gen_success = bool(sql_pred)
            
            # SQL validation
            sql_valid_pred, _ = validate_sql(sql_pred, q)
            
            # SQL execution
            state = execute_sql_query(state)
            execution_success = state.error is None
            execution_error = state.error if state.error else ''
            
            # Final output formatting
            if hasattr(state, 'query_result') and isinstance(state.query_result, pd.DataFrame):
                formatted_output = format_dataframe_safely(state.query_result)
                formatting_success = bool(formatted_output and not formatted_output.isspace())
            else:
                formatted_output = ''
                formatting_success = False
            
            results.append({
                'question': q,
                'intent_pred': intent_pred,
                'tables_pred': tables_pred,
                'columns_pred': columns_pred,
                'value_mapping_pred': value_mapping_pred,
                'sql_pred': sql_pred,
                'sql_valid_pred': sql_valid_pred,
                'execution_success': execution_success,
                'execution_error': execution_error,
                'formatted_output': formatted_output,
                'intent_success': intent_success,
                'table_success': table_success,
                'column_success': column_success,
                'sql_gen_success': sql_gen_success,
                'sql_valid_success': sql_valid_pred,
                'execution_success_metric': execution_success,
                'formatting_success': formatting_success
            })
            
            progress_bar.progress((i + 1) / len(questions))
        
        progress_bar.empty()
    
    # Calculate metrics
    total = len(results)
    intent_acc = sum(r['intent_success'] for r in results) / total if total else 0
    table_acc = sum(r['table_success'] for r in results) / total if total else 0
    column_acc = sum(r['column_success'] for r in results) / total if total else 0
    sql_gen_acc = sum(r['sql_gen_success'] for r in results) / total if total else 0
    sql_valid_acc = sum(r['sql_valid_success'] for r in results) / total if total else 0
    execution_acc = sum(r['execution_success_metric'] for r in results) / total if total else 0
    formatting_acc = sum(r['formatting_success'] for r in results) / total if total else 0
    
    # Calculate average node success rate
    node_accuracies = [intent_acc, table_acc, column_acc, sql_gen_acc, sql_valid_acc, execution_acc, formatting_acc]
    average_node_acc = sum(node_accuracies) / len(node_accuracies) if node_accuracies else 0
    
    # Display metrics in a clean layout
    st.markdown('<h2 class="section-header">📈 Performance Metrics</h2>', unsafe_allow_html=True)
    
    # Create metric cards with better styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Intent Detection</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if intent_acc >= 0.8 else 'success-medium' if intent_acc >= 0.6 else 'success-low'}">
                    {intent_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['intent_success'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>📋 Table Selection</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if table_acc >= 0.8 else 'success-medium' if table_acc >= 0.6 else 'success-low'}">
                    {table_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['table_success'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Column Selection</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if column_acc >= 0.8 else 'success-medium' if column_acc >= 0.6 else 'success-low'}">
                    {column_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['column_success'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔧 SQL Generation</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if sql_gen_acc >= 0.8 else 'success-medium' if sql_gen_acc >= 0.6 else 'success-low'}">
                    {sql_gen_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['sql_gen_success'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ SQL Validation</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if sql_valid_acc >= 0.8 else 'success-medium' if sql_valid_acc >= 0.6 else 'success-low'}">
                    {sql_valid_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['sql_valid_success'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ SQL Execution</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if execution_acc >= 0.8 else 'success-medium' if execution_acc >= 0.6 else 'success-low'}">
                    {execution_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['execution_success_metric'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📄 Formatting</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if formatting_acc >= 0.8 else 'success-medium' if formatting_acc >= 0.6 else 'success-low'}">
                    {formatting_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                {sum(r['formatting_success'] for r in results)}/{total} successful
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Average Success</h3>
            <p style="font-size: 2rem; font-weight: bold; margin: 0;">
                <span class="{'success-high' if average_node_acc >= 0.8 else 'success-medium' if average_node_acc >= 0.6 else 'success-low'}">
                    {average_node_acc*100:.1f}%
                </span>
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
                Overall pipeline performance
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Per-Question Performance Analysis
    st.markdown('<h2 class="section-header">🔍 Per-Question Performance Analysis</h2>', unsafe_allow_html=True)
    
    # Create a detailed per-question performance table
    per_question_data = []
    for i, result in enumerate(results):
        # Calculate individual node success for this question
        success_count = sum([
            result['intent_success'], result['table_success'], result['column_success'],
            result['sql_gen_success'], result['sql_valid_success'], 
            result['execution_success_metric'], result['formatting_success']
        ])
        success_rate = f"{success_count / 7 * 100:.1f}%"
        question_success = {
            'Question #': i + 1,
            'Question': result['question'][:50] + '...' if len(result['question']) > 50 else result['question'],
            'Intent': '✅' if result['intent_success'] else '❌',
            'Tables': '✅' if result['table_success'] else '❌',
            'Columns': '✅' if result['column_success'] else '❌',
            'SQL Gen': '✅' if result['sql_gen_success'] else '❌',
            'SQL Valid': '✅' if result['sql_valid_success'] else '❌',
            'Execution': '✅' if result['execution_success_metric'] else '❌',
            'Formatting': '✅' if result['formatting_success'] else '❌',
            'Success Count': success_count,
            'Success Rate': success_rate
        }
        per_question_data.append(question_success)
    
    per_question_df = pd.DataFrame(per_question_data)
    
    # Display the per-question performance table
    st.dataframe(
        per_question_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Add expandable sections for detailed question analysis
    st.markdown('<h3 style="margin-top: 2rem;">📋 Detailed Question Analysis</h3>', unsafe_allow_html=True)
    
    for i, result in enumerate(results):
        with st.expander(f"Question {i+1}: {result['question'][:100]}{'...' if len(result['question']) > 100 else ''}"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Node Performance:**")
                st.markdown(f"- 🎯 **Intent Detection**: {'✅ Success' if result['intent_success'] else '❌ Failed'}")
                st.markdown(f"- 📋 **Table Selection**: {'✅ Success' if result['table_success'] else '❌ Failed'}")
                st.markdown(f"- 📊 **Column Selection**: {'✅ Success' if result['column_success'] else '❌ Failed'}")
                st.markdown(f"- 🔧 **SQL Generation**: {'✅ Success' if result['sql_gen_success'] else '❌ Failed'}")
                st.markdown(f"- ✅ **SQL Validation**: {'✅ Success' if result['sql_valid_success'] else '❌ Failed'}")
                st.markdown(f"- ⚡ **SQL Execution**: {'✅ Success' if result['execution_success_metric'] else '❌ Failed'}")
                st.markdown(f"- 📄 **Formatting**: {'✅ Success' if result['formatting_success'] else '❌ Failed'}")
                
                # Calculate success rate for this question
                question_success_rate = sum([
                    result['intent_success'], result['table_success'], result['column_success'],
                    result['sql_gen_success'], result['sql_valid_success'], 
                    result['execution_success_metric'], result['formatting_success']
                ]) / 7 * 100
                
                st.markdown(f"**Overall Success Rate for this question: {question_success_rate:.1f}%**")
            
            with col2:
                st.markdown("**Generated Outputs:**")
                st.markdown(f"**Intent:** {result['intent_pred']}")
                st.markdown(f"**Tables:** {result['tables_pred']}")
                st.markdown(f"**Columns:** {result['columns_pred']}")
                st.markdown(f"**SQL:** ```sql\n{result['sql_pred']}\n```")
                if result['execution_error']:
                    st.markdown(f"**Error:** {result['execution_error']}")
                if result['formatted_output']:
                    st.markdown(f"**Formatted Output:** {result['formatted_output'][:200]}{'...' if len(result['formatted_output']) > 200 else ''}")
    
    # Visualization
    st.markdown('<h2 class="section-header">📊 Performance Visualization</h2>', unsafe_allow_html=True)
    
    # Create a more professional chart
    node_names = ['Intent Detection', 'Table Selection', 'Column Selection', 'SQL Generation', 'SQL Validation', 'SQL Execution', 'Formatting']
    node_accs = [intent_acc, table_acc, column_acc, sql_gen_acc, sql_valid_acc, execution_acc, formatting_acc]
    
    # Create color mapping based on performance
    colors = ['#27ae60' if acc >= 0.8 else '#f39c12' if acc >= 0.6 else '#e74c3c' for acc in node_accs]
    
    fig = go.Figure(data=[
        go.Bar(
            x=node_names,
            y=[acc * 100 for acc in node_accs],
            marker_color=colors,
            text=[f'{acc*100:.1f}%' for acc in node_accs],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Success Rate: %{y:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Node Success Rates',
        xaxis_title='Pipeline Nodes',
        yaxis_title='Success Rate (%)',
        yaxis=dict(range=[0, 100]),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.markdown('<h2 class="section-header">📋 Summary Statistics</h2>', unsafe_allow_html=True)
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Total Questions", len(questions))
        st.metric("Best Performing Node", 
                 node_names[node_accs.index(max(node_accs))] if node_accs else "N/A",
                 f"{max(node_accs)*100:.1f}%" if node_accs else "N/A")
    
    with summary_col2:
        st.metric("Average Success Rate", f"{average_node_acc*100:.1f}%")
        st.metric("Worst Performing Node", 
                 node_names[node_accs.index(min(node_accs))] if node_accs else "N/A",
                 f"{min(node_accs)*100:.1f}%" if node_accs else "N/A")
    
    with summary_col3:
        high_performing = sum(1 for acc in node_accs if acc >= 0.8)
        st.metric("High Performing Nodes (≥80%)", f"{high_performing}/{len(node_accs)}")
        low_performing = sum(1 for acc in node_accs if acc < 0.6)
        st.metric("Low Performing Nodes (<60%)", f"{low_performing}/{len(node_accs)}")
    
    # Detailed results
    st.markdown('<h2 class="section-header">🔍 Detailed Results</h2>', unsafe_allow_html=True)
    
    # Create a cleaner results dataframe
    results_df = pd.DataFrame(results)
    
    # Select only the most important columns for display
    display_columns = ['question', 'intent_pred', 'sql_pred', 'execution_success', 'execution_error']
    results_display = results_df[display_columns].copy()
    results_display.columns = ['Question', 'Intent', 'Generated SQL', 'Execution Success', 'Error']
    
    # Add success indicators
    results_display['Success'] = results_df.apply(
        lambda row: '✅' if all([
            row['intent_success'], row['table_success'], row['column_success'],
            row['sql_gen_success'], row['sql_valid_success'], 
            row['execution_success_metric'], row['formatting_success']
        ]) else '❌', axis=1
    )
    
    st.dataframe(
        results_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Download option
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Full Results (CSV)",
        data=csv,
        file_name=f"text2sql_pipeline_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    ) 