"""Keep dashboard inputs in the same Streamlit session across page switches."""

import streamlit as st

_UPLOADS = "_healthbrief_retained_uploads"


def file_uploader(label, *, key, on_change, **kwargs):
    # File upload widgets cannot be persisted or prefilled through Streamlit's
    # public API. Keep their in-memory UploadedFile separately from widget state.
    retained = st.session_state.setdefault(_UPLOADS, {})

    def changed():
        retained[key] = st.session_state.get(key)
        on_change()

    uploaded = st.file_uploader(label, key=key, on_change=changed, **kwargs)
    if uploaded is not None:
        retained[key] = uploaded
        return uploaded

    uploaded = retained.get(key)
    if uploaded is not None:
        st.caption(f"Retained file: {uploaded.name}")

        def remove_retained():
            retained.pop(key, None)
            # The native uploader is empty here, so the original callback sees
            # the same empty widget value as a normal file removal.
            on_change()

        st.button(
            "Remove retained file",
            key=f"{key}_remove_retained",
            on_click=remove_retained,
        )
    return uploaded


def previous_source_changed(reset_callback):
    # A source change deliberately discards the previous PDF; a page change
    # does not. Keep the stable dashboard's existing reset callback intact.
    st.session_state.get(_UPLOADS, {}).pop("previous_report_uploader", None)
    reset_callback()
