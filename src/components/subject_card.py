from html import escape

import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Bordered card with subject details and an optional footer widget.

    stats: list of (label, value) or (icon, label, value) tuples.
    footer_callback: function that renders widgets (e.g. a button) inside the card.
    """
    parts = [
        f'<div class="at-subject-name">{escape(str(name))}</div>',
        '<div class="at-subject-meta">',
        f'<span class="at-code">{escape(str(code))}</span>',
    ]
    if section:
        parts.append(f'<span>Section {escape(str(section))}</span>')
    parts.append('</div>')

    if stats:
        parts.append('<div class="at-stats">')
        for stat in stats:
            label, value = stat[-2], stat[-1]
            icon = f"{stat[0]} " if len(stat) == 3 and stat[0] else ""
            parts.append(
                f'<div class="at-stat"><b>{escape(str(value))}</b>'
                f'<span>{icon}{escape(str(label))}</span></div>'
            )
        parts.append('</div>')

    # One compact string (no indentation or blank lines) so Markdown never
    # mistakes part of it for a code block.
    with st.container(border=True):
        st.markdown("".join(parts), unsafe_allow_html=True)
        if footer_callback:
            footer_callback()
