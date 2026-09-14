import streamlit as st
import preprocessor, helper, sentiment, sentiment_plot
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — Dark Premium Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #080b12 !important;
    color: #dce6f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0c111c !important;
    border-right: 1px solid #162033;
    padding: 0;
}
section[data-testid="stSidebar"] > div { padding: 1.2rem 1rem; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span { color: #94a8bf !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 { color: #e0ecf8 !important; }

/* ── Sidebar brand ── */
.sb-brand {
    background: linear-gradient(135deg, #1a7a45 0%, #0e5c36 100%);
    border-radius: 14px;
    padding: 18px 16px 16px;
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #25D36630;
    box-shadow: 0 4px 24px rgba(37,211,102,0.12);
}
.sb-brand .sb-icon { font-size: 2.2rem; line-height: 1; margin-bottom: 6px; }
.sb-brand h2 { color: #fff !important; font-size: 1.05rem; font-weight: 800; margin: 0; letter-spacing: -0.3px; }
.sb-brand small { color: rgba(255,255,255,0.65) !important; font-size: 0.72rem; }

/* ── Sidebar step labels ── */
.sb-step {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0 10px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #25D366 !important;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}
.sb-step .num {
    background: #25D36620;
    border: 1px solid #25D36640;
    color: #25D366;
    border-radius: 50%;
    width: 20px; height: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 700; flex-shrink: 0;
}

/* ── Streamlit widgets dark overrides ── */
.stSelectbox > div > div,
.stFileUploader > div {
    background: #111827 !important;
    border: 1px solid #1e3050 !important;
    border-radius: 10px !important;
    color: #dce6f0 !important;
}
.stSelectbox label, .stFileUploader label {
    color: #94a8bf !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Analyse button ── */
.stButton > button {
    background: linear-gradient(135deg, #25D366 0%, #0e9e50 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 11px 0 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    width: 100% !important;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 18px rgba(37,211,102,0.25) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37,211,102,0.4) !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0b1829 0%, #091f16 55%, #0b1829 100%);
    border: 1px solid #25D36622;
    border-radius: 20px;
    padding: 40px 48px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, #25D36618 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 2px;
    color: #25D366; text-transform: uppercase; margin-bottom: 10px;
}
.hero h1 {
    font-size: 2.6rem; font-weight: 900; line-height: 1.1;
    background: linear-gradient(90deg, #25D366 0%, #82e0aa 50%, #dce6f0 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 10px; letter-spacing: -1.5px;
}
.hero p {
    font-size: 0.95rem; color: #607d96; margin: 0; max-width: 560px; line-height: 1.6;
}
.hero-chips {
    display: flex; gap: 8px; margin-top: 20px; flex-wrap: wrap;
}
.chip {
    background: #ffffff0a; border: 1px solid #ffffff12;
    border-radius: 50px; padding: 4px 12px;
    font-size: 0.72rem; font-weight: 500; color: #7a9ab5;
}

/* ── Metric cards ── */
.cards-row { display: flex; gap: 16px; margin-bottom: 28px; }
.mcard {
    flex: 1;
    background: #0e1520;
    border: 1px solid #182538;
    border-radius: 16px;
    padding: 22px 20px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    cursor: default;
}
.mcard:hover {
    border-color: #25D36650;
    box-shadow: 0 0 28px rgba(37,211,102,0.10);
    transform: translateY(-3px);
}
.mcard::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #25D366, #128C7E);
    opacity: 0;
    transition: opacity 0.2s;
}
.mcard:hover::before { opacity: 1; }
.mcard-icon { font-size: 1.6rem; margin-bottom: 12px; opacity: 0.9; }
.mcard-val { font-size: 2.1rem; font-weight: 800; color: #25D366; line-height: 1; letter-spacing: -1px; }
.mcard-lbl { font-size: 0.73rem; color: #4d6477; font-weight: 600; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; }

/* ── Section heading ── */
.sec-head {
    display: flex; align-items: center; gap: 10px;
    margin: 24px 0 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid #162033;
}
.sec-head h3 { font-size: 1.1rem; font-weight: 700; color: #c8d8e8; margin: 0; }
.sec-badge {
    background: #25D36615; color: #25D366;
    border: 1px solid #25D36630;
    border-radius: 20px; padding: 2px 9px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0e1520;
    border: 1px solid #182538;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    padding: 9px 22px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #4d6477 !important;
    transition: all 0.15s !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #94a8bf !important; background: #ffffff08 !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a7a45, #0e5c36) !important;
    color: #fff !important;
    box-shadow: 0 2px 12px rgba(37,211,102,0.2) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 8px !important; }

/* ── Sentiment pill ── */
.sent-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 7px 18px; border-radius: 50px;
    font-size: 0.9rem; font-weight: 700; margin: 10px 0 18px;
}
.sent-pos { background: #0a2e1a; color: #25D366; border: 1px solid #25D36640; }
.sent-neg { background: #2e0a0a; color: #f87171; border: 1px solid #f8717140; }
.sent-neu { background: #131c2e; color: #7ea8c4; border: 1px solid #7ea8c440; }

/* ── Info/empty state ── */
.empty-state {
    text-align: center;
    padding: 64px 32px;
    background: #0e1520;
    border: 1px dashed #182538;
    border-radius: 18px;
    margin-top: 12px;
}
.empty-state .es-icon { font-size: 3rem; margin-bottom: 14px; }
.empty-state h3 { font-size: 1.2rem; font-weight: 700; color: #c8d8e8; margin: 0 0 8px; }
.empty-state p { font-size: 0.88rem; color: #4d6477; margin: 0; line-height: 1.6; }

/* ── DataFrame ── */
.stDataFrame { background: #0e1520 !important; border-radius: 12px !important; }
.stDataFrame th { background: #111827 !important; color: #7ea8c4 !important; font-size: 0.75rem !important; }

/* ── Divider & footer ── */
hr { border-color: #162033 !important; margin: 20px 0; }
.footer {
    text-align: center; padding: 32px 0 12px;
    font-size: 0.82rem; color: #283d50;
}
.footer strong { color: #25D366; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080b12; }
::-webkit-scrollbar-thumb { background: #1e3a2e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #25D36650; }

/* ── Plotly chart container ── */
.stPlotlyChart {
    background: #0e1520;
    border: 1px solid #162033;
    border-radius: 14px;
    overflow: hidden;
    padding: 4px;
}

/* ── Streamlit info / warning ── */
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY HELPERS
# ─────────────────────────────────────────────
_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a8bf", size=12),
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a8bf"), borderwidth=0),
    hoverlabel=dict(bgcolor="#111827", font_color="#dce6f0", bordercolor="#1e3050"),
    xaxis=dict(
        gridcolor="#162033", linecolor="#162033", zerolinecolor="#162033",
        tickfont=dict(size=11, color="#607d96"),
    ),
    yaxis=dict(
        gridcolor="#162033", linecolor="#162033", zerolinecolor="#162033",
        tickfont=dict(size=11, color="#607d96"),
    ),
)

def _layout(**overrides):
    """Merge base layout with per-chart overrides, handling nested dicts like xaxis/yaxis."""
    result = dict(_BASE_LAYOUT)
    for k, v in overrides.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = {**result[k], **v}
        else:
            result[k] = v
    return result

WA_GREEN  = "#25D366"
WA_TEAL   = "#0e9e50"
WA_BLUE   = "#34B7F1"
WA_PURPLE = "#a29bfe"
WA_PINK   = "#fd79a8"
WA_YELLOW = "#ffd166"
COLOR_SEQ = [WA_GREEN, WA_BLUE, WA_PURPLE, WA_PINK, WA_YELLOW, "#e17055"]
GREEN_SCALE = [[0, "#071a10"], [0.4, "#0e5c36"], [1, WA_GREEN]]

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-icon">💬</div>
        <h2>WA Analyzer</h2>
        <small>WhatsApp Chat Intelligence</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-step"><div class="num">1</div>Upload Chat File</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["txt"], label_visibility="collapsed")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        with st.spinner("Parsing chat…"):
            df = preprocessor.preprocess(data)

        user_list = df['user'].unique().tolist()
        try:
            user_list.remove('group_notification')
        except ValueError:
            pass
        user_list.sort()
        user_list.insert(0, "OverAll")

        st.markdown('<div class="sb-step"><div class="num">2</div>Choose User</div>', unsafe_allow_html=True)
        selected_user = st.selectbox("", user_list, label_visibility="collapsed")

        with st.spinner("Computing sentiments…"):
            df = sentiment.fetch_sentiment(df)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sb-step"><div class="num">3</div>Run Analysis</div>', unsafe_allow_html=True)
        analyze_btn = st.button("🔍  Show Analysis")
    else:
        selected_user = None
        analyze_btn = False

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem;color:#283d50;text-align:center;line-height:1.8">
        📖 Export: WhatsApp → Chat<br>→ More → Export Chat<br>→ Without Media
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">💬 Powered by NLP & Data Viz</div>
    <h1>WhatsApp Chat Analyzer</h1>
    <p>Upload your exported chat to uncover hidden patterns, message trends, sentiment scores, and conversation insights — all beautifully visualized.</p>
    <div class="hero-chips">
        <span class="chip">📈 Timeline</span>
        <span class="chip">😊 Sentiment</span>
        <span class="chip">☁️ Word Cloud</span>
        <span class="chip">🗓️ Heatmap</span>
        <span class="chip">👥 User Stats</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("""
    <div class="empty-state">
        <div class="es-icon">👈</div>
        <h3>No chat file uploaded yet</h3>
        <p>Upload a WhatsApp chat export (.txt) from the sidebar to get started.<br>
        Your data stays local — nothing is sent to any server.</p>
    </div>
    """, unsafe_allow_html=True)

elif analyze_btn:
    num_message, words, num_media, num_links = helper.fetch_stats(selected_user, df)

    # ── METRIC CARDS ────────────────────────────
    st.markdown("""
    <div class="sec-head" style="margin-top:0">
        <h3>📊 Overview</h3><span class="sec-badge">Stats</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cards-row">
        <div class="mcard">
            <div class="mcard-icon">💬</div>
            <div class="mcard-val">{num_message:,}</div>
            <div class="mcard-lbl">Total Messages</div>
        </div>
        <div class="mcard">
            <div class="mcard-icon">📝</div>
            <div class="mcard-val">{words:,}</div>
            <div class="mcard-lbl">Total Words</div>
        </div>
        <div class="mcard">
            <div class="mcard-icon">🖼️</div>
            <div class="mcard-val">{num_media:,}</div>
            <div class="mcard-lbl">Media Shared</div>
        </div>
        <div class="mcard">
            <div class="mcard-icon">🔗</div>
            <div class="mcard-val">{num_links:,}</div>
            <div class="mcard-lbl">Links Shared</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈  Timeline",
        "🗓️  Activity",
        "😊  Sentiment",
        "💬  Words & Emojis",
        "👥  Users",
    ])

    # ══════════════════════════════════════════
    #  TAB 1 — TIMELINE
    # ══════════════════════════════════════════
    with tab1:
        # Monthly timeline
        st.markdown("""<div class="sec-head"><h3>Monthly Timeline</h3><span class="sec-badge">Trend</span></div>""", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timeline['time'], y=timeline['message'],
            mode='lines+markers',
            line=dict(color=WA_GREEN, width=3, shape='spline'),
            marker=dict(size=8, color=WA_GREEN, line=dict(color="#0e1520", width=2)),
            fill='tozeroy',
            fillcolor='rgba(37,211,102,0.07)',
            name="Messages",
            hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
        ))
        fig.update_layout(**_layout(
            title=dict(text="Messages per Month", font=dict(size=14, color="#c8d8e8"), x=0.02),
            height=380,
            xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Daily timeline (per-user only)
        if selected_user != 'OverAll':
            st.markdown("""<div class="sec-head"><h3>Daily Timeline</h3><span class="sec-badge">Daily</span></div>""", unsafe_allow_html=True)
            daily = helper.daily_timeline(selected_user, df)
            fig2 = px.area(
                daily, x='only_date', y='message',
                color_discrete_sequence=[WA_BLUE],
                labels={'only_date': 'Date', 'message': 'Messages'},
            )
            fig2.update_traces(
                fillcolor='rgba(52,183,241,0.08)',
                line=dict(color=WA_BLUE, width=2),
                hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
            )
            fig2.update_layout(**_layout(
                title=dict(text="Daily Message Activity", font=dict(size=14, color="#c8d8e8"), x=0.02),
                height=340,
            ))
            st.plotly_chart(fig2, use_container_width=True)

    # ══════════════════════════════════════════
    #  TAB 2 — ACTIVITY
    # ══════════════════════════════════════════
    with tab2:
        if selected_user != 'OverAll':
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("""<div class="sec-head"><h3>Most Active Day</h3><span class="sec-badge">Weekly</span></div>""", unsafe_allow_html=True)
                busy_day = helper.week_activity_map(selected_user, df)
                fig3 = px.bar(
                    x=busy_day.index, y=busy_day.values,
                    color=busy_day.values,
                    color_continuous_scale=GREEN_SCALE,
                    text=busy_day.values,
                    labels={'x': 'Day', 'y': 'Messages', 'color': ''},
                )
                fig3.update_traces(
                    texttemplate='%{text}',
                    textposition='outside',
                    textfont=dict(size=11, color="#94a8bf"),
                    marker_line_width=0,
                    hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
                )
                fig3.update_layout(**_layout(
                    title=dict(text="Activity by Day of Week", font=dict(size=14, color="#c8d8e8"), x=0.02),
                    height=380, coloraxis_showscale=False,
                ))
                st.plotly_chart(fig3, use_container_width=True)

            with col_b:
                st.markdown("""<div class="sec-head"><h3>Weekly Activity Heatmap</h3><span class="sec-badge">Heatmap</span></div>""", unsafe_allow_html=True)
                user_heatmap = helper.activity_heatmap(selected_user, df)
                if user_heatmap is not None and not user_heatmap.empty:
                    fig4 = px.imshow(
                        user_heatmap,
                        color_continuous_scale=[[0, "#080b12"], [0.4, "#0e5c36"], [1, WA_GREEN]],
                        aspect="auto",
                        labels=dict(x="Hour Period", y="Day", color="Messages"),
                    )
                    fig4.update_traces(
                        hovertemplate="Day: <b>%{y}</b><br>Hour: %{x}<br>Messages: %{z}<extra></extra>",
                    )
                    fig4.update_layout(**_layout(
                        title=dict(text="Message Activity Heatmap", font=dict(size=14, color="#c8d8e8"), x=0.02),
                        height=380,
                    ))
                    st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.warning("Not enough data to generate heatmap for this user.")
        else:
            st.markdown("""
            <div class="empty-state" style="padding:40px 24px">
                <div class="es-icon">🗓️</div>
                <h3>Select a specific user</h3>
                <p>Activity maps and heatmaps are available when you select an individual user from the sidebar.</p>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════
    #  TAB 3 — SENTIMENT
    # ══════════════════════════════════════════
    with tab3:
        sentiment_value, dict1 = sentiment.sentiment_value(df)
        pill_cls   = {"positive": "sent-pos", "negative": "sent-neg"}.get(sentiment_value, "sent-neu")
        pill_emoji = {"positive": "😊", "negative": "😞"}.get(sentiment_value, "😐")

        st.markdown(f"""
        <div class="sec-head" style="margin-top:4px">
            <h3>Overall Sentiment</h3><span class="sec-badge">NLP · VADER</span>
        </div>
        <p style="color:#4d6477;font-size:0.85rem;margin-bottom:10px">
            Chat tone computed via VADER sentiment analysis across all messages.
        </p>
        <span class="sent-pill {pill_cls}">{pill_emoji} &nbsp;{sentiment_value.upper()}</span>
        """, unsafe_allow_html=True)

        col_s1, col_s2 = st.columns(2)

        with col_s1:
            st.markdown("""<div class="sec-head"><h3>Sentiment Breakdown</h3><span class="sec-badge">VADER</span></div>""", unsafe_allow_html=True)
            sentiment_colors = {"positive": WA_GREEN, "negative": "#f87171", "neutral": "#7ea8c4"}
            sent_keys = list(dict1.keys())
            sent_vals = [round(v, 2) for v in dict1.values()]

            fig5 = go.Figure(go.Bar(
                x=sent_keys,
                y=sent_vals,
                text=[f"{v:.1f}" for v in sent_vals],
                textposition='outside',
                textfont=dict(size=13, color="#94a8bf"),
                marker_color=[sentiment_colors[k] for k in sent_keys],
                marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>Score: %{y:.2f}<extra></extra>",
            ))
            fig5.update_layout(**_layout(
                title=dict(text="Positive / Negative / Neutral Scores", font=dict(size=14, color="#c8d8e8"), x=0.02),
                height=380, showlegend=False,
            ))
            st.plotly_chart(fig5, use_container_width=True)

        with col_s2:
            st.markdown("""<div class="sec-head"><h3>Emotion Distribution</h3><span class="sec-badge">NLP</span></div>""", unsafe_allow_html=True)
            w = sentiment_plot.sentiment_plot()
            if w:
                em_df = (pd.DataFrame(w.items(), columns=['Emotion', 'Count'])
                           .sort_values('Count', ascending=False)
                           .head(10))
                em_df['Emotion'] = em_df['Emotion'].str.strip().str.title()
                fig6 = px.bar(
                    em_df, x='Emotion', y='Count',
                    color='Count',
                    color_continuous_scale=GREEN_SCALE,
                    text='Count',
                    labels={'Count': 'Frequency'},
                )
                fig6.update_traces(
                    texttemplate='%{text}', textposition='outside',
                    textfont=dict(size=11, color="#94a8bf"), marker_line_width=0,
                    hovertemplate="<b>%{x}</b><br>Frequency: %{y}<extra></extra>",
                )
                fig6.update_layout(**_layout(
                    title=dict(text="Detected Emotions in Chat", font=dict(size=14, color="#c8d8e8"), x=0.02),
                    height=380, coloraxis_showscale=False,
                ))
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.info("No strong emotions detected in this chat.")

    # ══════════════════════════════════════════
    #  TAB 4 — WORDS & EMOJIS
    # ══════════════════════════════════════════
    with tab4:
        col_w1, col_w2 = st.columns([3, 2])

        with col_w1:
            st.markdown("""<div class="sec-head"><h3>Word Cloud</h3><span class="sec-badge">Visual</span></div>""", unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_user, df)
            fig_wc, ax_wc = plt.subplots(figsize=(9, 4.5), facecolor='none')
            ax_wc.imshow(df_wc)
            ax_wc.axis('off')
            fig_wc.patch.set_alpha(0.0)
            st.pyplot(fig_wc, use_container_width=True)

        with col_w2:
            st.markdown("""<div class="sec-head"><h3>Most Used Emojis</h3><span class="sec-badge">Top 7</span></div>""", unsafe_allow_html=True)
            emoji_df = helper.emoji_help(selected_user, df)
            if not emoji_df.empty:
                st.dataframe(
                    emoji_df,
                    column_config={
                        "emoji": st.column_config.TextColumn("Emoji", width="small"),
                        "count": st.column_config.ProgressColumn(
                            "Count", format="%d",
                            min_value=0, max_value=int(emoji_df['count'].max()),
                        ),
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=300,
                )
            else:
                st.markdown("""
                <div style="text-align:center;padding:40px 16px;color:#4d6477;font-size:0.85rem">
                    😶 No emojis found in this chat
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""<div class="sec-head"><h3>Most Common Words</h3><span class="sec-badge">Top 20</span></div>""", unsafe_allow_html=True)
        most_common_word = helper.most_common_words(selected_user, df)

        fig7 = px.bar(
            most_common_word, x=1, y=0,
            orientation='h',
            color=1,
            color_continuous_scale=GREEN_SCALE,
            text=1,
            labels={0: 'Word', 1: 'Frequency'},
        )
        fig7.update_traces(
            texttemplate='%{text}', textposition='outside',
            textfont=dict(size=11, color="#94a8bf"), marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        )
        # Fix: override yaxis separately via update_yaxes to avoid conflict with _layout's yaxis key
        fig7.update_layout(**_layout(
            title=dict(text="Top 20 Most Frequently Used Words", font=dict(size=14, color="#c8d8e8"), x=0.02),
            height=540,
            coloraxis_showscale=False,
        ))
        fig7.update_yaxes(autorange="reversed", tickfont=dict(size=12, color="#94a8bf"))
        st.plotly_chart(fig7, use_container_width=True)

    # ══════════════════════════════════════════
    #  TAB 5 — USERS
    # ══════════════════════════════════════════
    with tab5:
        x, new_df = helper.most_busy_user(df)
        col_u1, col_u2 = st.columns(2)

        with col_u1:
            st.markdown("""<div class="sec-head"><h3>Most Active Users</h3><span class="sec-badge">Top 5</span></div>""", unsafe_allow_html=True)
            fig8 = px.bar(
                x=x.index, y=x.values,
                color=x.values,
                color_continuous_scale=GREEN_SCALE,
                text=x.values,
                labels={'x': 'User', 'y': 'Messages', 'color': ''},
            )
            fig8.update_traces(
                texttemplate='%{text}', textposition='outside',
                textfont=dict(size=12, color="#94a8bf"), marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
            )
            fig8.update_layout(**_layout(
                title=dict(text="Message Count per User", font=dict(size=14, color="#c8d8e8"), x=0.02),
                height=400, coloraxis_showscale=False,
            ))
            st.plotly_chart(fig8, use_container_width=True)

        with col_u2:
            st.markdown("""<div class="sec-head"><h3>Conversation Share</h3><span class="sec-badge">%</span></div>""", unsafe_allow_html=True)
            pie_df = new_df.copy()
            name_col  = pie_df.columns[0]
            value_col = pie_df.columns[1]
            fig9 = px.pie(
                pie_df, names=name_col, values=value_col,
                hole=0.58,
                color_discrete_sequence=COLOR_SEQ,
            )
            fig9.update_traces(
                textinfo='label+percent',
                pull=[0.025] * len(pie_df),
                textfont=dict(size=11, color="#dce6f0"),
                marker=dict(line=dict(color="#080b12", width=2)),
                hovertemplate="<b>%{label}</b><br>Share: %{percent}<br>Messages: %{value}<extra></extra>",
            )
            fig9.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a8bf"),
                margin=dict(l=16, r=16, t=48, b=16),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a8bf"), orientation="h", y=-0.1),
                title=dict(text="Conversation Share by User", font=dict(size=14, color="#c8d8e8"), x=0.02),
                height=400,
            )
            st.plotly_chart(fig9, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Made with ❤️ by <strong>Soumya Samanta</strong> &nbsp;·&nbsp; WhatsApp Chat Analyzer
</div>
""", unsafe_allow_html=True)
