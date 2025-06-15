import streamlit as st
import os
from yandex import YandexGPT

from dotenv import load_dotenv

load_dotenv()


def render_page(title, state_key, prompt_file=None):
    token = os.getenv('YANDEX_TOKEN')
    catalog = os.getenv('YANDEX_CATALOG')

    st.title(title)

    if state_key not in st.session_state:
        if prompt_file:
            with open(prompt_file, encoding='utf-8') as t:
                sys_prompt = t.read()
        else:
            sys_prompt = None                
        st.session_state[state_key] = YandexGPT(token, catalog, sys_prompt)

    message_key = f'message_{state_key}'
    if message_key not in st.session_state:
        st.session_state[message_key] = []

    for message in st.session_state[message_key]:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input("Say something")
    if prompt:
        st.chat_message('user').write(prompt)
        answer = st.session_state[state_key].get_answer(prompt)

        st.session_state[message_key].append({"role": "user", "content": prompt})
        st.session_state[message_key].append({"role": "yandex", "content": answer})

        st.rerun()


if __name__ == '__main__':
    render_page('Просто YandexGPT',  'base')
