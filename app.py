"""Improved version of the uploaded washing-machine Streamlit exercise.

Run: streamlit run app.py
The same HTML/JS runs in the component and standalone preview.
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"


def build_html() -> str:
    """Inline local assets so Streamlit needs no static-file server or CDN."""
    template = (ASSETS / "exercise.html").read_text(encoding="utf-8")
    replacements = {
        "/*__STYLES__*/": "style.css",
        "/*__MODEL__*/": "controller.js",
        "/*__APP__*/": "exercise.js",
    }
    for marker, filename in replacements.items():
        template = template.replace(marker, (ASSETS / filename).read_text(encoding="utf-8"))
    return template


def source_archive() -> bytes:
    """Create the actual source download, without caches or local session data."""
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for name in ["app.py", "requirements.txt", "README.md", "CHANGELOG.md"]:
            path = ROOT / name
            if path.exists():
                archive.write(path, f"washing_machine_connected/{name}")
        for folder in ["assets", "tests", ".streamlit"]:
            for path in sorted((ROOT / folder).rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    archive.write(path, f"washing_machine_connected/{path.relative_to(ROOT)}")
    return buffer.getvalue()


def render_washing_machine() -> None:
    """Call this from an existing workshop page to embed the exercise."""
    html = build_html()
    if hasattr(st, "iframe"):
        st.iframe(html, height="content", alt="Interactive washing-machine state-machine exercise")
    else:
        components.html(html, height=1100, scrolling=True)


def main() -> None:
    st.set_page_config(
        page_title="Washing Machine | State Machine Workshop",
        page_icon="🧺",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """<style>
        .block-container {padding: 0 0 .5rem; max-width: 620px;}
        [data-testid="stAppViewContainer"] {background:#ffffff;}
        iframe {border:0; border-radius:14px; width:100%;}
        [data-testid="stHeader"] {display:none;}
        [data-testid="stDownloadButton"] button {font-size:12px;}
        </style>""",
        unsafe_allow_html=True,
    )
    render_washing_machine()


if __name__ == "__main__":
    main()
