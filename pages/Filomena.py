from functions.streamlitfunc import *
from functions.utils import *
import time
import os
import streamlit as st
from functions.chat_bot import *
from functions.utils import local_settings
from streamlit_extras.switch_page_button import switch_page 

#General configurations
st.set_page_config(page_title='Chat with Filomena', page_icon="ext_images\page_icon.png", layout="wide", initial_sidebar_state= "collapsed")
display_header()

filomena_pic =  "https://cdn.discordapp.com/attachments/1150843302644547768/1190661589347602492/1000_F_378272550_xN8H7ZVudgCYWzfuZxRxVS5uFKjzsoMg.jpg?ex=65a29d04&is=65902804&hm=4a84c24f579a1d8ac5493b28f47b50c1dc7aaabc2832cb090bd7e4e95b2ab786&"
user_pic =   "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*_ARzR7F_fff_KI14yMKBzw.png"                                 


#Intialize session states
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None

def initialize() -> None:
    """
    Initialize the ChatBot Filomena.
    Parameters:
        - None
    Returns:
        - None
    """
    files = []
    for file in os.listdir('text_data'):
        file = f'text_data/{file}'
        files.append(file)
    if "chatbot" not in st.session_state or st.session_state.chatbot is None:
        fil = Filomena()
        fil.initialize(files=files)    
        st.session_state.chatbot = fil
   


def display_history_messages():
    """
    Display chat messages from history on app rerun.
    Parameters:
        - None
    Returns:
        - None
    """

    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot.messages:
        if message["role"] == "user":
            avatar = user_pic
        else:
            avatar = avatar=filomena_pic
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            

def display_user_msg(message: str):
    """
    Display user message in chat message container.
    Parameters:
        - message (str): User message.
    Returns:
        - None
    """

    with st.chat_message("user", avatar=user_pic):
        st.markdown(message)

                                                           

def display_assistant_msg(message: str, animated=True):
    """
    Display assistant message.
    Parameters:
        - message (str): Assistant message.
        - animated (bool): If True, the message is displayed with a typing animation.
    Returns:
        - None
    """
    if animated:
        with st.chat_message("assistant",  avatar= filomena_pic):
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
        with st.chat_message("assistant",  avatar=filomena_pic):
            st.markdown(message)

def show_prompt_templates(show:str, prompt:str = None, num:int=1):
    """
    Display prompt templates in the sidebar.
    Parameters:
        - show (str): Button label.
        - prompt (str): Prompt to be sent to Filomena.
        - num (int): Number of the button.
    """
    #If the prompt is not defined, use the button label as the prompt.
    if prompt is None:
        prompt = show
    
    #Put the button and the prompt in the sidebar
    with st.sidebar:
        button =  st.button(show, key=f"button_{num}")
    
    #If the button is clicked, send the prompt to Filomena
    if button and prompt:
        display_chat(prompt=prompt)


def display_chat(prompt: str):
    """
    Generate and display chat messages.
    Parameters:
        - prompt (str): User message.
    Returns:
        - None
    """
    display_user_msg(message=prompt)
    assistant_response = st.session_state.chatbot.generate_response(query=prompt)
    display_assistant_msg(message=assistant_response)


if __name__ == "__main__":

    #If the user is correctly logged in
    if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
        pages_logged_in()

        #Aesthetic configurations
        cola, colb = st.columns([1, 3])
        with cola:
            st.image(filomena_pic, width=300)
        with colb:
            st.title("Talk with Filomena 🍲")
            st.write("Ask me anything about FlavourFlix, food personalities, or even restaurant recommendations and I'll do my best to answer you! 🇵🇹")
            st.caption("Note that the answers are not always 100% accurate, but I'm learning! Use the prompt templates in the sidebar to maximize my potential." )

        st.write('')

        #Initialize the chatbot and display the chat history
        initialize()
        display_history_messages()
        
        #Set the prompt templates in the sidebar
        st.sidebar.title("Prompt Templates")
        st.sidebar.write("Click on a prompt to send it to Filomena.")

        show_prompt_templates(show="👩‍🍳 What is FlavourFlix?", prompt="What is FlavourFlix?", num=1)
        show_prompt_templates(show="🍽️ Recommend me a Restaurant", prompt="Please recommend me a restaurant.", num=2)
        show_prompt_templates(show="🎉 Describe me portuguese culinary festivities", prompt="Describe me a portuguese culinary festivities", num=3)
 
        #If the user wants to talk freely with Filomena
        if prompt := st.chat_input("Talk with Filomena..."):
            display_chat(prompt=prompt)

    else:
        pages_logged_off()
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        st.write('You need to be logged in to access this feature.')
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
