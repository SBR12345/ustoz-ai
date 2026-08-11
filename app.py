"""Ustoz.AI — AI Teaching Assistant for Uzbekistan Schools."""

import base64
import os
import re
import streamlit as st
from i18n import ui, SUBJECTS
from prompts import (
    build_lesson_plan_prompt,
    build_exercises_prompt,
    build_test_prompt,
    build_quality_check_prompt,
)
from ai_client import generate_material, run_quality_check

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Ustoz.AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────

background_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "teacher-background.png",
)
with open(background_path, "rb") as background_file:
    background_data = base64.b64encode(background_file.read()).decode()

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --navy: #0C1222;
    --navy-light: #141D2F;
    --navy-mid: #1A2540;
    --cyan: #6FF0DD;
    --cyan-dim: rgba(111, 240, 221, 0.15);
    --gold: #D7B46A;
    --gold-dim: rgba(215, 180, 106, 0.15);
    --text-primary: #E8ECF4;
    --text-secondary: #8B95A8;
    --border: rgba(111, 240, 221, 0.12);
}

.stApp {
    background-color: var(--navy) !important;
    background-image:
        linear-gradient(rgba(12, 18, 34, 0.82), rgba(12, 18, 34, 0.88)),
        url("data:image/png;base64,__BACKGROUND_IMAGE__") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

section[data-testid="stSidebar"] {
    background-color: var(--navy-light) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: var(--text-secondary) !important;
}

h1, h2, h3, h4 {
    color: var(--text-primary) !important;
}

.main-title {
    background: linear-gradient(135deg, var(--cyan) 0%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0;
    line-height: 1.2;
}

.subtitle {
    color: var(--text-secondary);
    font-size: 1.05rem;
    margin-top: 0.25rem;
    margin-bottom: 1.5rem;
}

div[data-testid="stForm"] {
    background-color: var(--navy-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: var(--navy-mid) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px var(--cyan) !important;
}

.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.generate-btn button {
    background: linear-gradient(135deg, var(--cyan) 0%, #4DD4C0 100%) !important;
    color: var(--navy) !important;
    border: none !important;
    padding: 0.6rem 2rem !important;
    font-size: 1.05rem !important;
    width: 100% !important;
}

.generate-btn button:hover {
    box-shadow: 0 4px 20px rgba(111, 240, 221, 0.3) !important;
    transform: translateY(-1px) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background-color: var(--navy-light) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--navy-mid) !important;
    color: var(--cyan) !important;
    border-bottom: none !important;
}

.quality-card {
    background-color: var(--navy-light);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
}

.quality-card h4 {
    margin: 0 0 0.5rem 0;
    font-size: 0.95rem;
    color: var(--gold) !important;
}

.quality-badge-pass {
    display: inline-block;
    background-color: rgba(111, 240, 221, 0.15);
    color: #6FF0DD;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.quality-badge-warn {
    display: inline-block;
    background-color: rgba(215, 180, 106, 0.15);
    color: #D7B46A;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.quality-badge-fail {
    display: inline-block;
    background-color: rgba(255, 100, 100, 0.15);
    color: #FF6464;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.quality-comment {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-top: 0.4rem;
    line-height: 1.5;
}

div[data-testid="stExpander"] {
    background-color: var(--navy-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

.copy-area {
    position: relative;
}

.stMarkdown code {
    color: var(--cyan) !important;
}

.logo-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.stSpinner > div > div {
    border-top-color: var(--cyan) !important;
}
</style>
""".replace("__BACKGROUND_IMAGE__", background_data)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────

DEFAULTS = {
    "lang": "ru",
    "lesson_plan": "",
    "exercises": "",
    "test": "",
    "quality_results": {},
    "generated": False,
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    app_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(app_dir, "assets", "ustoz-logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(app_dir), "ustoz-logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)

    lang = st.selectbox(
        ui("language_label", st.session_state["lang"]),
        options=["ru", "uz", "en"],
        format_func=lambda x: {
            "ru": "Русский",
            "uz": "O'zbekcha",
            "en": "English",
        }[x],
        index={"ru": 0, "uz": 1, "en": 2}.get(st.session_state["lang"], 0),
        key="lang_select",
    )
    st.session_state["lang"] = lang
    L = lang

    st.divider()
    st.subheader(ui("sidebar_settings", L))

    api_key = st.text_input(
        ui("api_key_label", L),
        type="password",
        help=ui("api_key_help", L),
        value=os.environ.get("GROQ_API_KEY", ""),
    )

# ── Header ───────────────────────────────────────────────────────────────────

st.markdown(f'<p class="main-title">{ui("app_title", L)}</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="subtitle">{ui("app_subtitle", L)}</p>', unsafe_allow_html=True
)

# ── Input form ───────────────────────────────────────────────────────────────

with st.form("lesson_form"):
    col1, col2 = st.columns(2)

    with col1:
        subject = st.selectbox(
            ui("subject_label", L),
            options=SUBJECTS[L],
        )
        topic = st.text_input(
            ui("topic_label", L),
            placeholder=ui("topic_placeholder", L),
        )

    with col2:
        grade = st.selectbox(
            ui("grade_label", L),
            options=list(range(1, 12)),
            format_func=lambda x: f"{x}{ui('grade_suffix', L)}",
            index=3,
        )
        output_lang = st.selectbox(
            ui("output_language_label", L),
            options=["ru", "uz", "en"],
            format_func=lambda x: (
                ui(f"output_lang_{x}", L)
            ),
        )

    additional = st.text_area(
        ui("additional_instructions_label", L),
        placeholder=ui("additional_instructions_placeholder", L),
        height=68,
    )

    st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
    submitted = st.form_submit_button(
        ui("generate_button", L), use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Generation logic ────────────────────────────────────────────────────────

if submitted:
    if not topic.strip():
        st.error(ui("error_no_topic", L))
        st.stop()
    if not api_key:
        st.error(ui("error_no_api_key", L))
        st.stop()

    prompt_args = dict(
        subject=subject,
        grade=grade,
        topic=topic,
        output_lang=output_lang,
        additional=additional,
    )

    with st.spinner(ui("generating", L)):
        try:
            st.session_state["lesson_plan"] = generate_material(
                api_key, build_lesson_plan_prompt(**prompt_args), output_lang
            )
            st.session_state["exercises"] = generate_material(
                api_key, build_exercises_prompt(**prompt_args), output_lang
            )
            st.session_state["test"] = generate_material(
                api_key, build_test_prompt(**prompt_args), output_lang
            )
            st.session_state["generated"] = True
        except Exception as e:
            st.error(f"API Error: {e}")
            st.stop()

    # ── Quality Council ──────────────────────────────────────────────────
    with st.spinner(ui("checking_quality", L)):
        combined_material = (
            st.session_state["lesson_plan"][:1500]
            + "\n\n"
            + st.session_state["exercises"][:1000]
            + "\n\n"
            + st.session_state["test"][:500]
        )
        quality = {}
        for check_type, label_key in [
            ("curriculum", "quality_curriculum"),
            ("difficulty", "quality_difficulty"),
            ("clarity", "quality_clarity"),
        ]:
            try:
                result = run_quality_check(
                    api_key,
                    build_quality_check_prompt(
                        check_type=check_type,
                        subject=subject,
                        grade=grade,
                        topic=topic,
                        material=combined_material,
                        output_lang=output_lang,
                    ),
                    output_lang,
                )
                rating = "pass"
                if re.search(
                    r"Частично|Qisman|Partially meets|частично|qisman|partially meets",
                    result,
                ):
                    rating = "warn"
                elif re.search(
                    r"Требует доработки|Takomillashtirish|Needs improvement|требует|takomil|needs improvement",
                    result,
                    re.IGNORECASE,
                ):
                    rating = "fail"
                quality[check_type] = {
                    "label_key": label_key,
                    "rating": rating,
                    "text": result,
                }
            except Exception:
                quality[check_type] = {
                    "label_key": label_key,
                    "rating": "warn",
                    "text": "Could not complete this check.",
                }

        st.session_state["quality_results"] = quality

# ── Display results ──────────────────────────────────────────────────────────

if st.session_state["generated"]:
    # Quality Council panel
    quality = st.session_state.get("quality_results", {})
    if quality:
        st.markdown(f"### {ui('quality_title', L)}")
        qcols = st.columns(3)
        for idx, (check_type, data) in enumerate(quality.items()):
            with qcols[idx]:
                badge_class = f"quality-badge-{data['rating']}"
                rating_labels = {
                    "pass": ui("quality_pass", L),
                    "warn": ui("quality_warn", L),
                    "fail": ui("quality_fail", L),
                }
                comment_lines = data["text"].split("\n")
                comment_text = ""
                for line in comment_lines:
                    if (
                        line.strip().startswith("**Комментарий")
                        or line.strip().startswith("**Izoh")
                        or line.strip().startswith("**Comment")
                    ):
                        comment_text = line.split(":", 1)[-1].strip().strip("*").strip()
                        break
                if not comment_text:
                    for line in comment_lines:
                        stripped = line.strip()
                        if (
                            stripped
                            and not stripped.startswith("**Оценка")
                            and not stripped.startswith("**Baho")
                            and not stripped.startswith("**Rating")
                        ):
                            comment_text = stripped.strip("*").strip()
                            break

                st.markdown(
                    f"""<div class="quality-card">
<h4>{ui(data['label_key'], L)}</h4>
<span class="{badge_class}">{rating_labels[data['rating']]}</span>
<p class="quality-comment">{comment_text}</p>
</div>""",
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # Tabs with materials
    tab_plan, tab_ex, tab_test = st.tabs(
        [
            ui("lesson_plan_tab", L),
            ui("exercises_tab", L),
            ui("test_tab", L),
        ]
    )

    def render_tab(tab, content: str, tab_key: str):
        with tab:
            st.markdown(content)
            copy_col, _ = st.columns([1, 4])
            with copy_col:
                escaped = content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
                copy_js = f"""
<script>
function copyText_{tab_key}() {{
    const text = `{escaped}`;
    navigator.clipboard.writeText(text);
    document.getElementById('copy-status-{tab_key}').innerText = '{ui("copied", L)}';
    setTimeout(() => document.getElementById('copy-status-{tab_key}').innerText = '', 2000);
}}
</script>
<button onclick="copyText_{tab_key}()"
    style="background: var(--navy-mid); color: var(--cyan); border: 1px solid var(--border);
           border-radius: 6px; padding: 4px 14px; cursor: pointer; font-size: 0.85rem;">
    {ui("copy_button", L)}
</button>
<span id="copy-status-{tab_key}" style="color: var(--gold); margin-left: 8px; font-size: 0.85rem;"></span>
"""
                st.components.v1.html(copy_js, height=40)

    render_tab(tab_plan, st.session_state["lesson_plan"], "plan")
    render_tab(tab_ex, st.session_state["exercises"], "exercises")
    render_tab(tab_test, st.session_state["test"], "test")

    # Clear button
    st.markdown("")
    if st.button(ui("clear_button", L)):
        for key in ["lesson_plan", "exercises", "test", "quality_results", "generated"]:
            st.session_state[key] = DEFAULTS[key]
        st.rerun()
