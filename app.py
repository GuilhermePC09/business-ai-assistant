import streamlit as st
import uuid
from nodes import llm
from nodes.llm import ChatOllama

def init_state() -> None:
    if "chats" not in st.session_state:
        chat_id = str(uuid.uuid4())
        st.session_state.chats = {chat_id: []}
        st.session_state.active_chat = chat_id

def get_current_messages() -> list[dict]:
    return st.session_state.chats[st.session_state.active_chat]

def generate_reply(user_text: str) -> str:
    answer = ChatOllama().generate_response(user_text, st.session_state.active_chat)    
    return answer


def render_header() -> None:
    st.set_page_config(page_title="Assistant", page_icon=":speech_balloon:", layout="centered")
    st.title("Bussines Assistant chat")
    st.caption(
    "Your AI copilot for business consulting: metrics, market insights, currency conversion, and report generation."
    )


def render_history() -> None:
    messages = get_current_messages()
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_input() -> None:
    user_text = st.chat_input("Ask me anything")
    if not user_text:
        return

    st.session_state.chats[st.session_state.active_chat].append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    reply = generate_reply(user_text)
    st.session_state.chats[st.session_state.active_chat].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)


def render_sidebar():
    with st.sidebar:
        st.header("Chats")

        for chat_id in st.session_state.chats.keys():
            is_active = chat_id == st.session_state.active_chat
            label = f"👉 Chat {chat_id[:4]}" if is_active else f"Chat {chat_id[:4]}"
            if st.button(label, key=chat_id):
                st.session_state.active_chat = chat_id
                st.rerun()

        st.divider()

        if st.button("+ New chat"):
            new_id = str(uuid.uuid4())
            st.session_state.chats[new_id] = []
            st.session_state.active_chat = new_id
            st.rerun()

        if st.button("Delete current chat"):
            if len(st.session_state.chats) > 1:
                del st.session_state.chats[st.session_state.active_chat]
                st.session_state.active_chat = next(iter(st.session_state.chats))
                st.rerun()
            else:
                st.warning("Cannot delete the only chat.")

        if st.button("Clear current chat"):
            st.session_state.chats[st.session_state.active_chat] = []
            st.rerun()

def main() -> None:
    init_state()
    render_header()
    render_sidebar()
    render_history()
    handle_input()


if __name__ == "__main__":
    main()

