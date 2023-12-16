from functions.streamlitfunc import *

# a pagina personality só aparece se utilizador estiver logged in
st.set_page_config( page_icon="ext_images\page_icon.png", layout="wide")

def personality_inputs():
    st.subheader('You need to fill in the personality questionnaire')
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("- ##### I enjoy trying new and exotic cuisines when dining out.")
    Q1 = st.select_slider(
    'Select a range of color wavelength',
    options=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree", "I love exploring diverse cuisines."], value='Neutral')
    # Q1 = st.selectbox( '######  ',
        
    #      ["Choose an option", "Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree", "I love exploring diverse cuisines."])
    
    if Q1 is not "Choose an option": 
        st.write('**You selected:**', Q1)
    else:
        st.write('**Please select an option**')

    # aqui adicionar algo do genero
    # if Q1 == "Choose an option": data[Q1] = Nan 
    # if Q1 == "Strongly Disagree": data[Q1] = 0 (...)
    # if Q1 == "Disagree": data[Q1] = 1 (...) etc
    
    st.divider()


    st.markdown("- ##### I prefer restaurants that offer a variety of menu options.")
    Q2 = st.selectbox(
        "######  ",
        ["Choose an option", "Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree", "I appreciate a diverse menu."])
    
    if Q2 is not "Choose an option": 
        st.write('**You selected:**', Q2)
    else:
        st.write('**Please select an option**')

    
    # se houver algum nan não dá para descobrir a personalidade

    # se não houver null values guardar na dataframe dos clients

 
    
# se nan na dataframe dos clients
# mostrar a página dos inputs

personality_inputs()

# else
# mostrar a pagina da personalidade
def personality_presentation():
    
    st.subheader("Discover your personality")
    st.write(f"You are a blabla")


# if user logged in and não houver nans nas perguntas:
# personality_presentation()

# if user logged in and houver nans nas perguntas
# redirecionar para perfil para responder ao questionário

