import streamlit as st
import logging
from services.llm_service import llm_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Streamlit UI
st.set_page_config(page_title="Chatbot Roole X BOUGHRARA Souha", page_icon="🤖")
st.title("Chatbot Personnalisé : Restitution pour le poste Business Intelligence Analyst Junior chez Roole ")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Pose ta question...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            try:
                # Convert session messages to the format expected by LLM service
                messages_for_llm = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ]
                
                # Generate response
                answer = llm_service.generate(
                    messages=messages_for_llm,
                    use_system_prompt=True,
                    json_mode=False
                )
                
                st.write(answer)
                
            except Exception as e:
                logger.error(f"Error generating response: {e}", exc_info=True)
                answer = f" Erreur lors de l'appel au modèle : {e}"
                st.error(answer)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})