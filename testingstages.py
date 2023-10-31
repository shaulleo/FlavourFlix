
import streamlit as st

# This doesn't work, because button "pressed" state doesn't survive rerun, and pressing
# any button triggers a rerun.

st.write("# This doesn't work:")

if st.button("begin_take1"):
    if st.button("login_take1"):
        if st.button("submitcode_take1"):
            st.write("submitcode")

# So, instead, we use session state to store the "pressed" state of each button, and
# make each button press toggle that entry in the session state.

st.write("# This works:")

if "begin" not in st.session_state:
    st.session_state["begin"] = False

if "login" not in st.session_state:
    st.session_state["login"] = False

if "submitcode" not in st.session_state:
    st.session_state["submitcode"] = False

if st.button("begin"):
    st.session_state["begin"] = not st.session_state["begin"]

if st.session_state["begin"]:
    if st.button("login"):
        st.session_state["login"] = not st.session_state["login"]

if st.session_state["begin"] and st.session_state["login"]:
    if st.button("submitcode"):
        # toggle submitcode session state
        st.session_state["submitcode"] = not st.session_state["submitcode"]

if st.session_state["submitcode"]:
    st.write("**submitcode!!!**")


# Print the session state to make it easier to see what's happening
st.write(
    f"""
    ## Session state:
    {st.session_state["begin"]=}

    {st.session_state["login"]=}

    {st.session_state["submitcode"]=}
    """
)