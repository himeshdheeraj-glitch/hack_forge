import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np

def render_dashboard(stats):
    """
    Renders professional analytics dashboard using Plotly.
    """
    st.markdown("## 📊 System Intelligence & Analytics")
    
    # Calculate Dynamic Satisfaction
    total_feedback = stats['feedback']['helpful'] + stats['feedback']['not_helpful']
    satisfaction = 0
    if total_feedback > 0:
        satisfaction = round((stats['feedback']['helpful'] / total_feedback) * 100, 1)
    else:
        satisfaction = 100.0 # Default starting point

    # --- Top Level Metrics ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Queries", stats.get('total_questions', 0))
    m2.metric("Success Rate", f"{stats.get('query_success_rate', 0)}%", delta="Live Tracking")
    avg_latency = np.mean(stats.get('response_times', [0])) if stats.get('response_times') else 0.0
    m3.metric("Avg Response Time", f"{avg_latency:.2f}s")
    m4.metric("User Satisfaction", f"{satisfaction}%", delta="Based on Feedback")

    st.markdown("---")

    # --- Query & Performance Analytics ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Language Distribution")
        lang_map = {'en': 'English', 'hi': 'Hindi', 'te': 'Telugu'}
        lang_data = pd.DataFrame({
            'Language': [lang_map[l] for l in stats['language_dist'].keys()],
            'Count': list(stats['language_dist'].values())
        })
        if lang_data['Count'].sum() == 0:
            st.info("No queries tracked yet in this session.")
        else:
            fig_lang = px.pie(lang_data, values='Count', names='Language', 
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             hole=0.4)
            fig_lang.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_lang, use_container_width=True)

    with col2:
        st.subheader("⏱️ Intelligence & Performance Index")
        performance_hist = stats.get('intelligence_scores', [85.0])
        if not performance_hist:
            st.info("Waiting for system activity to track intelligence...")
        else:
            fig_perf = px.line(y=performance_hist, labels={'y': 'Intelligence Score (%)', 'x': 'Interaction History'},
                                 title="Real-time System Trust & Intelligence Trend")
            fig_perf.update_traces(line_color='#00d11f', line_width=4)
            fig_perf.update_layout(yaxis_range=[0, 105])
            st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("---")

    # --- Document & Content Analytics ---
    c1, c2 = st.columns([1, 1.5])
    
    with c1:
        st.subheader("📄 Document Metrics")
        st.write(f"📁 **Total Uploads:** {stats.get('total_policies', 0)}")
        st.write(f"📖 **Pages Processed:** {stats.get('total_pages', 0)}")
        st.write(f"🧩 **Vector Chunks:** {stats.get('total_chunks', 0)}")
        
        # Retrieval Accuracy Gauge (Linked to success rate)
        current_acc = stats.get('query_success_rate', 0)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_acc,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Retrieval Accuracy", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#004080"},
                'steps': [
                    {'range': [0, 70], 'color': "#ffcccc"},
                    {'range': [70, 90], 'color': "#ffffcc"},
                    {'range': [90, 100], 'color': "#ccffcc"}]
            }
        ))
        fig_gauge.update_layout(height=180, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with c2:
        st.subheader("🔥 Popular Schemes")
        recs = stats.get('searched_schemes', {})
        if not recs or sum(recs.values()) == 0:
            st.info("No scheme engagement recorded yet.")
        else:
            pop_data = pd.DataFrame({
                'Scheme': list(recs.keys()),
                'Interactions': list(recs.values())
            }).sort_values('Interactions', ascending=True)
            
            fig_pop = px.bar(pop_data, y='Scheme', x='Interactions', orientation='h',
                            color='Interactions', color_continuous_scale='Blues')
            st.plotly_chart(fig_pop, use_container_width=True)

    # --- Feedback Section ---
    st.markdown("---")
    f1, f2 = st.columns(2)
    with f1:
        st.subheader("💬 User Feedback (REAL-TIME)")
        feedback = stats.get('feedback', {'helpful': 0, 'not_helpful': 0})
        
        fig_feedback = px.bar(
            x=['Helpful (👍)', 'Not Helpful (👎)'],
            y=[feedback['helpful'], feedback['not_helpful']],
            color=['Helpful', 'Not Helpful'],
            color_discrete_map={'Helpful': '#28a745', 'Not Helpful': '#dc3545'}
        )
        fig_feedback.update_layout(showlegend=False, xaxis_title="", yaxis_title="Votes")
        st.plotly_chart(fig_feedback, use_container_width=True)
    
    with f2:
        if satisfaction >= 80:
            st.success(f"✅ **High Satisfaction:** Users are finding the chatbot very helpful ({satisfaction}%).")
        elif satisfaction >= 50:
            st.warning(f"⚠️ **Moderate Satisfaction:** System is performing at {satisfaction}%. Consider checking retrieval context.")
        else:
            st.error(f"🚨 **Low Satisfaction:** System accuracy is low ({satisfaction}%). User feedback is predominantly negative.")
        
        st.info(f"💡 **AI Insight:** Lang: {max(stats['language_dist'], key=stats['language_dist'].get) if any(stats['language_dist'].values()) else 'None'} is currently the most active.")
