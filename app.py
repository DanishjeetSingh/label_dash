import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="LabelDash - A Quick Text Labeling Tool")
st.title("🎮 LabelDash - A Quick Text Labeling Tool")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
if not uploaded_file:
    st.sidebar.info("Please upload a CSV to get started.")
    st.stop()

df = pd.read_csv(uploaded_file)
input_name = uploaded_file.name

col_name_input = st.sidebar.text_input(
    "Label column name:", value="label", key="col_name_input"
)
label_input = st.sidebar.text_input(
    "Enter labels (comma-separated)", value="Positive,Negative,Neutral", key="label_input"
)
base_labels = [l.strip() for l in label_input.split(",") if l.strip()]
cols_to_show = st.sidebar.multiselect(
    "Columns to display", options=df.columns.tolist(),
    default=df.columns.tolist()[:1], key="cols_to_show"
)
start_row = st.sidebar.number_input(
    "Start at record # (1-based)", min_value=1,
    max_value=len(df), value=1, step=1, key="start_row"
)
start_btn = st.sidebar.button("▶️ Start Annotation", key="start_btn")

if 'filename' not in st.session_state or st.session_state.filename != input_name:
    st.session_state.filename = input_name
    st.session_state.started = False
    st.session_state.labels = {}
    st.session_state.idx = 0
    st.session_state.download_mode = False

if start_btn:
    st.session_state.col_name = col_name_input
    st.session_state.base_labels = base_labels
    st.session_state.label_options = ["Select…"] + base_labels
    st.session_state.cols = cols_to_show
    st.session_state.idx = start_row - 1
    if col_name_input in df.columns:
        for idx, val in df[col_name_input].dropna().items():
            if val in base_labels:
                st.session_state.labels[int(idx)] = val
    st.session_state.started = True

if not st.session_state.get('started', False):
    st.header("🔧 Configuration Preview")
    st.markdown(f"**Label column name:** {col_name_input}")
    st.markdown(f"**Labels:** {', '.join(base_labels)}")
    st.markdown(f"**Columns to display:** {', '.join(cols_to_show)}")
    st.markdown(f"**Start at record:** {start_row}")
    st.stop()

col_name = st.session_state.col_name
base_labels = st.session_state.base_labels
label_options = st.session_state.label_options
cols = st.session_state.cols

filled = len(st.session_state.labels)
total = len(df)
st.sidebar.markdown(f"**Progress:** {filled} / {total} labeled")
st.sidebar.progress(filled / total)

st.markdown("---")
st.subheader(f"Record {st.session_state.idx+1} of {total}")

prev_pressed = st.button("◀️ Prev", key="nav_prev")
next_pressed = st.button("Next ▶️", key="nav_next")

if next_pressed and st.session_state.idx < len(df) - 1:
    st.session_state.idx += 1
    st.rerun()
elif prev_pressed and st.session_state.idx > 0:
    st.session_state.idx -= 1
    st.rerun()

existing = None
if col_name in df.columns:
    val = df[col_name].iloc[st.session_state.idx]
    if pd.notna(val) and val in base_labels:
        existing = val
current_label = st.session_state.labels.get(st.session_state.idx, existing)
default_i = (base_labels.index(current_label) + 1) if current_label in base_labels else 0

radio_col, msg_col = st.columns([3, 2])

with radio_col:
    default_key = f"radio_{st.session_state.idx}"
    choice = st.radio(
        "Assign a label:", options=label_options,
        index=default_i, key=default_key
    )

with msg_col:
    if choice != "Select…":
        prev = st.session_state.labels.get(st.session_state.idx)
        st.session_state.labels[st.session_state.idx] = choice
        if choice != prev:
            st.success(f"Saved: '{choice}'")
    else:
        if st.session_state.idx in st.session_state.labels:
            del st.session_state.labels[st.session_state.idx]
            st.info("Label cleared")

row = df.iloc[st.session_state.idx]
st.markdown("### Content:")
for c in cols:
    st.markdown(f"**{c}**: {row[c]}")

if choice != "Select…":
    prev = st.session_state.labels.get(st.session_state.idx)
    st.session_state.labels[st.session_state.idx] = choice
else:
    if st.session_state.idx in st.session_state.labels:
        del st.session_state.labels[st.session_state.idx]

if st.sidebar.button("📥 Prepare Download", key="prep_download"):
    st.session_state.download_mode = True

if st.session_state.get("download_mode"):
    out_fname = st.sidebar.text_input(
        "Output file name:", value=input_name, key="out_fname"
    )

    out = df.copy()
    out[col_name] = ""
    for idx, lbl in st.session_state.labels.items():
        out.at[idx, col_name] = lbl
    csv = out.to_csv(index=False).encode("utf-8")

    dl_clicked = st.sidebar.download_button(
        label="Click to download labeled CSV",
        data=csv,
        file_name=out_fname,
        mime="text/csv",
        key="dl"
    )

    if dl_clicked:
        st.session_state.clear()
        st.rerun()