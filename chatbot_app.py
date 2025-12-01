import streamlit as st
import logging
from services.llm_service import LLMService
from config.llm.settings import llm_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Streamlit UI
st.set_page_config(page_title="Chatbot Roole X BOUGHRARA Souha", page_icon="🤖")
st.title("Chatbot Personnalisé : Restitution pour le poste Business Intelligence Analyst Junior chez Roole ")

# Sidebar for HuggingFace token configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for token in various sources
    try:
        token_from_secrets = st.secrets.get("HUGGINGFACEHUB_API_TOKEN", "")
    except:
        token_from_secrets = ""
    
    token_from_env = llm_settings.hf_token or ""
    
    # Initialize session state for token
    if "hf_token" not in st.session_state:
        st.session_state.hf_token = token_from_secrets or token_from_env
    
    # Show token input field
    st.markdown("### 🔑 HuggingFace Token")
    
    if st.session_state.hf_token and st.session_state.hf_token.strip():
        st.success("✅ Token configuré")
        if st.button("🔄 Changer le token"):
            st.session_state.hf_token = ""
            st.rerun()
    else:
        st.warning("⚠️ Token requis pour utiliser le chatbot")
        token_input = st.text_input(
            "Entrez votre token HuggingFace:",
            type="password",
            help="Obtenez votre token sur https://huggingface.co/settings/tokens"
        )
        
        if st.button("💾 Sauvegarder le token"):
            if token_input and token_input.strip():
                st.session_state.hf_token = token_input.strip()
                st.success("Token sauvegardé ! L'application va redémarrer.")
                st.rerun()
            else:
                st.error("Veuillez entrer un token valide")
    
    st.markdown("---")
    st.markdown(f"""
    **Modèle:** {llm_settings.llm_model_id}  
    **Max tokens:** {llm_settings.max_new_tokens}  
    **Temperature:** {llm_settings.temperature}
    """)

# Check if token is available before showing chat
if not st.session_state.hf_token or not st.session_state.hf_token.strip():
    st.info("👈 Veuillez configurer votre token HuggingFace dans la barre latérale pour commencer.")
    st.stop()

# Initialize LLM service with the token
try:
    llm_service = LLMService(hf_token=st.session_state.hf_token)
except Exception as e:
    st.error(f"❌ Erreur lors de l'initialisation du service LLM: {e}")
    st.stop()

# Initialize session state for messages
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