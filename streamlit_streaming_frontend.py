import streamlit as st 
from langgraph_backend import chatbot
from langchain.messages import HumanMessage

CONFIG = {"configurable": {'thread_id': 'thread-1'}}

# session_state is just a simple dictionary but this way streamlit stores teh previous data
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    # first add the message to the message history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

# we use streamlit stream prop to implement it

    with st.chat_message('assistant'):
        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content='what is the recipe to make pasta?')]},
                config = {"configurable": {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )
        st.session_state['message_history'].append({'role':'assistant', 'content':ai_response})

