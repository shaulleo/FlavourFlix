from functions.streamlitfunc import *
from functions.utils import *
import time
import streamlit as st
from functions.chat_bot import *
from functions.utils import local_settings
from streamlit_extras.switch_page_button import switch_page 

st.set_page_config(page_title='Chat with Filomena', page_icon="ext_images\page_icon.png", layout="wide", initial_sidebar_state= "auto")

display_header()
                                                                                


def initialize() -> None:
    """
    Initialize the app
    """
  
    st.title("Ask Filomena 🍲")
    st.write("Ask me anything about portuguese food and restaurants and I'll do my best to answer you! 🇵🇹")
    st.write("Note that the answers are not always 100% accurate, but I'm learning!")

    files = ['data\CP-23Group4 Project Proposal.pdf', 'data\Food Personalities.pdf']
    if "chatbot" not in st.session_state or st.session_state.chatbot is None:
        fil = Filomena()
        fil.load_documents(files, 'pdf')
        fil.generate_response("[Instruction: Identification] Hello", identified=True)
        st.session_state.chatbot = fil


    




def display_history_messages():
    """
    Display chat messages from history on app rerun.
    """
    # Display chat messages from history on app rerun
    if st.session_state.chatbot.messages != []:
        for message in st.session_state.chatbot.messages:
            if message["role"] == "user":
                avatar = 'https://miro.medium.com/v2/resize:fit:1100/format:webp/1*_ARzR7F_fff_KI14yMKBzw.png'
            else:
                avatar = avatar="https://cdn.discordapp.com/attachments/1150843302644547768/1190661589347602492/1000_F_378272550_xN8H7ZVudgCYWzfuZxRxVS5uFKjzsoMg.jpg?ex=65a29d04&is=65902804&hm=4a84c24f579a1d8ac5493b28f47b50c1dc7aaabc2832cb090bd7e4e95b2ab786&"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
            

def display_user_msg(message: str):
    """
    Display user message in chat message container.
    """

    with st.chat_message("user", avatar="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*_ARzR7F_fff_KI14yMKBzw.png"):
        st.markdown(message)

                                                           

def display_assistant_msg(message: str, animated=True):
    """
    Display assistant message
    """

    if animated:
        with st.chat_message("assistant",  avatar="https://cdn.discordapp.com/attachments/1150843302644547768/1190661589347602492/1000_F_378272550_xN8H7ZVudgCYWzfuZxRxVS5uFKjzsoMg.jpg?ex=65a29d04&is=65902804&hm=4a84c24f579a1d8ac5493b28f47b50c1dc7aaabc2832cb090bd7e4e95b2ab786&"):
            message_placeholder = st.empty()

            # Simulate stream of response with milliseconds delay
            full_response = ""
            for chunk in message.split():
                full_response += chunk + " "
                time.sleep(0.05)

                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
    else:
        with st.chat_message("assistant",  avatar="https://cdn.discordapp.com/attachments/1150843302644547768/1190661589347602492/1000_F_378272550_xN8H7ZVudgCYWzfuZxRxVS5uFKjzsoMg.jpg?ex=65a29d04&is=65902804&hm=4a84c24f579a1d8ac5493b28f47b50c1dc7aaabc2832cb090bd7e4e95b2ab786&"):
            st.markdown(message)



if __name__ == "__main__":

    if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
        pages_logged_in()
        initialize()

        # [i] Display History #
        display_history_messages()

        if prompt := st.chat_input("Talk with Filomena..."):

            # [*] Request & Response #
            display_user_msg(message=prompt)
            assistant_response = st.session_state.chatbot.generate_response(query=prompt)
            display_assistant_msg(message=assistant_response)

    else:
        pages_logged_off()
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        st.write('You need to be logged in to access this feature.')
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
