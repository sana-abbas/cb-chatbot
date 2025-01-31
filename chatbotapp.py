import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from openai import OpenAI
import time

# OpenAI API key yahan daalein
# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable

client = OpenAI(api_key="OPENAI_API_KEY")


def get_chatbot_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": "Aap ek helpful multilingual assistant ho jo kisi bhi bhasha mein prompt expect karta hai aur JSON format mein jawab deta hai. JSON mein three fields hone chahiye: 'roman-urdu' Urdu mein response, 'translation' for English translation aur 'speaker_language' for the language in which the prompt was received. Agar aapko Hindi, English, Urdu, Swahili, Shona, French ya koi aur language mein prompt milta hai, to aapko Urdu mein jawab dena chahiye 'roman-urdu' field mein, English mein translation 'translation' field mein add karna chahiye aur us language ka naam 'speaker_language' field mein enter karna chahiye."},
               {"role": "user", "content": "Hello kya haal hain apkay?"}, # 1 shot prompting
                {"role": "assistant", "content": '{"roman-urdu": "Hello! Main theek hoon, aap batayen kya haal hai?", "translation": "Hello! I\'m fine, how are you?", "speaker_language": "Urdu"}'},
               {"role": "user", "content": "What is your name"}, # 2 shot prompting
                {"role": "assistant","content" : '{"roman-urdu": "Mera naam Assistant hai.", "translation": "My name is Assistant.", "speaker_language": "English"}'},
                {"role": "user", "content": "Mhoro, wakadii?"}, # 3 shot prompting
                {"role": "assistant","content" : '{"roman-urdu": "Main theek hoon, shukriya", "translation": "I am doing good. Thank you", "speaker_language": "Shona"}'},
                {"role": "user", "content": "Zvese zvinhu zvawakwanisa kuita zvakadii?"}, #4 shot prompting
                {"role": "assistant","content" : '{"roman-urdu": "Main aapki madad karne ke liye yahaan hoon!", "translation": "I am here to help you with anything!", "speaker_language": "Shona"}'},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Kuch galat hogya :(: {str(e)}"

# def main():
#     st.title("Chatbot with OpenAI and Streamlit")
    
#     # Input text box for user prompt
#     user_input = st.text_input("User:", "")
    
#     if st.button("Send"):
#         if user_input.strip() != "":
#             with st.spinner('Soch raha hun...'):
#                 response = get_chatbot_response(user_input)
#             st.write("Chatbot:", response)
#         else:
#             st.warning("Yahan likhen!")


def handle_send():
    if st.session_state.user_input.strip() != "":
        user_message = st.session_state.user_input
        st.session_state.chat_history.append({"message": user_message, "is_user": True})

        with st.spinner('Soch Raha hun....'):
            # Simulate chatbot processing time
            time.sleep(1)
            response = get_chatbot_response(user_message)

        st.session_state.chat_history.append({"message": response, "is_user": False})
        st.session_state.user_input = ""  # Clear the input
    else:
        st.warning("Please enter a message!")

def main():
    # Set page configuration
    st.set_page_config(page_title="Fancy Chatbot", page_icon="🤖", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f8ff;
    }
    .css-1d391kg {
        background-color: #e6f3ff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title with custom styling
    st.markdown("<h1 style='text-align: center; color: #1e90ff;'>🤖 Fancy Chatbot with OpenAI and Streamlit</h1>", unsafe_allow_html=True)

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for i, chat in enumerate(st.session_state.chat_history):
        message(chat["message"], is_user=chat["is_user"], key=str(i))

    # Input text box for user prompt
    st.text_input("You:", key="user_input")

    # Send button
    if st.button("Send"):
        handle_send()

    # Add a footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Made with ❤️ by Sana Fatima</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
# openai.api_key = api_key

# def chatbot(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7
#         )
#         message = response.choices[0].message.content.strip()
#         return message
#     except Exception as e:
#         return f"Kuch ghalat ho gaya: {str(e)}"

# def main():
#     st.title("Chatbot with OpenAI and Streamlit")
    
#     # Input text box for user prompt
#     user_input = st.text_input("User:", "")
    
#     if st.button("Send"):
#         if user_input.strip() != "":
#             with st.spinner('Sooch raha hai...'):
#                 response = chatbot(user_input)
#             st.write("Chatbot:", response)
#         else:
#             st.warning("Kuch type karein user input mein!")

# if __name__ == "__main__":
#     main()