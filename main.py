import streamlit as st
from google import genai
from google.genai import types
import os
import tempfile
from PIL import Image
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Workaround for Streamlit file watcher
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'poll'

# Initialize session state
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'last_uploaded_image' not in st.session_state:
    st.session_state.last_uploaded_image = None
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'image_file' not in st.session_state:
    st.session_state.image_file = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Configure Gemini API
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY not found in .env file.")
        logger.error("GEMINI_API_KEY not found.")
        st.stop()
    client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("Gemini API client initialized.")
except Exception as e:
    logger.error(f"Error initializing Gemini API: {str(e)}")
    st.error(f"Error initializing Gemini API: {str(e)}")
    st.stop()

def process_image(uploaded_image):
    """Process uploaded image and generate a summary."""
    logger.info("Processing image...")
    if not uploaded_image:
        logger.warning("No image uploaded.")
        st.error("No image uploaded.")
        return None
    
    try:
        image = Image.open(uploaded_image)
    except Exception as e:
        logger.error(f"Invalid image file: {str(e)}")
        st.error("Please upload a valid image file (JPG, JPEG, PNG).")
        return None
    
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, "uploaded_image.jpg")
    
    try:
        image = image.resize((512, 512))
        image.save(temp_file_path, format="JPEG")
        logger.info(f"Image saved to {temp_file_path}")
        
        my_file = client.files.upload(file=temp_file_path)
        logger.info(f"Image uploaded to Gemma: {my_file.uri}")
        
        st.session_state.chat_session = client.chats.create(model="gemma-3-27b-it")
        
        config = types.GenerateContentConfig(
            max_output_tokens=150,
            temperature=0.5
        )
        prompt = (
            "You are a helpful assistant specializing in image analysis and concise summarization. "
            "Generate a concise summary (2-4 lines) of the content in this image."
        )
        response = client.models.generate_content_stream(
            model="gemma-3-27b-it",
            contents=[my_file, prompt],
            config=config
        )
        summary = "".join(chunk.text for chunk in response if chunk.text)
        logger.info(f"Summary generated: {summary}")
        
        os.unlink(temp_file_path)
        logger.info(f"Temporary file {temp_file_path} deleted.")
        
        if not summary:
            logger.warning("No summary generated.")
            st.warning("No summary generated.")
            return None
        
        return summary
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        st.error(f"Error processing image: {str(e)}")
        return None

def ask_follow_up_question(question, summary):
    """Handle follow-up questions about the image."""
    logger.info(f"Processing question: {question}")
    if not st.session_state.chat_session:
        logger.error("No chat session available.")
        st.error("Please process an image first.")
        return None
    
    try:
        config = types.GenerateContentConfig(
            max_output_tokens=150,
            temperature=0.7
        )
        prompt = (
            "You are a helpful assistant specializing in image analysis. "
            "For questions directly related to the image, provide detailed answers based on its content. "
            "If the question is broadly related to the image's subject but not specific, "
            "give a brief, interesting fact and encourage the user to ask about the image itself. "
            "If the question is unrelated, respond with: 'Please ask a question related to the image.'\n"
            f"Image summary: {summary}\n"
            f"Question: {question}"
        )
        response = st.session_state.chat_session.send_message_stream(
            message=prompt,
            config=config
        )
        answer = "".join(chunk.text for chunk in response if chunk.text)
        logger.info(f"Answer generated: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        st.error(f"Error processing question: {str(e)}")
        return None

# Streamlit UI setup
st.set_page_config(page_title="Image Summary Generator", layout="wide", initial_sidebar_state="collapsed")

# Apply dark theme CSS
css = """
<style>
.stApp {
    background: #1a1a1a !important;  /* Dark background */
    color: #FFFFFF !important;
}
.stApp * {
    color: #FFFFFF !important;  /* White text for all elements */
}
.summary-card {
    background-color: rgba(255, 255, 255, 0.1) !important;  /* Semi-transparent for summary card */
    border: 1px solid #00c4cc;
    border-radius: 10px;
    padding: 15px;
    margin-top: 10px;
    color: #FFFFFF !important;  /* White text in summary card */
}
.stButton>button {
    background-color: #00c4cc !important;  /* Cyan background for buttons */
    color: #FFFFFF !important;  /* White text for buttons */
    border-radius: 5px;
    border: none;
    padding: 8px 16px;
}
.stButton>button:hover {
    background-color: #ff6f61 !important;  /* Coral hover effect */
    color: #FFFFFF !important;
}
.stChatMessage, .stChatMessage * {
    color: #FFFFFF !important;  /* White text for chat messages */
}
.stSpinner > div > div {
    color: #FFFFFF !important;  /* White spinner text */
}
.stTextInput > div > div > input {
    color: #FFFFFF !important;  /* White text for input fields */
    background-color: #2a2a2a !important;  /* Darker background for inputs */
}
.stSelectbox > div > div > select {
    color: #FFFFFF !important;  /* White text for selectbox */
    background-color: #2a2a2a !important;  /* Darker background for selectbox */
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Navigation
page = st.sidebar.selectbox("Select Page", ["Home", "About"])

if page == "Home":
    st.title("Image Summary Generator")
    st.markdown("Upload an image to generate a concise summary, then ask follow-up questions in a chat-like interface.")

    # Reset app button
    if st.button("Reset App", help="Clear everything and start over"):
        st.session_state.processing_complete = False
        st.session_state.last_uploaded_image = None
        st.session_state.chat_session = None
        st.session_state.summary = None
        st.session_state.image_file = None
        st.session_state.chat_history = []
        st.rerun()

    # Image uploader
    with st.container():
        uploaded_image = st.file_uploader("Upload an Image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"], key="image_uploader")

    # Process new image
    if uploaded_image and uploaded_image != st.session_state.last_uploaded_image:
        with st.spinner("Analyzing image..."):
            summary = process_image(uploaded_image)
            if summary:
                st.session_state.summary = summary
                st.session_state.processing_complete = True
                st.session_state.last_uploaded_image = uploaded_image
                st.session_state.image_file = uploaded_image
                st.session_state.chat_history = []
                st.success("Image processed successfully!")
            else:
                st.session_state.processing_complete = False
                st.session_state.chat_session = None
                st.session_state.summary = None
                st.session_state.image_file = None
                st.session_state.chat_history = []

    # Display image and summary
    if st.session_state.summary:
        with st.container():
            st.subheader("Uploaded Image")
            st.image(st.session_state.image_file, width=500)  # Fixed width for image
            st.subheader("Summary")
            st.markdown(f'<div class="summary-card">{st.session_state.summary}</div>', unsafe_allow_html=True)
            st.markdown("---")

    # Clear conversation button
    if st.session_state.chat_history:
        if st.button("Clear Chat", help="Clear conversation history"):
            st.session_state.chat_history = []
            st.rerun()

    # Chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['question'])
        with st.chat_message("assistant"):
            st.write(chat['answer'])

    # Chat input
    if st.session_state.summary:
        follow_up_question = st.chat_input(placeholder="Ask about the image (e.g., 'What’s in the background?')")
        if follow_up_question:
            with st.spinner("Generating response..."):
                answer = ask_follow_up_question(follow_up_question, st.session_state.summary)
                if answer:
                    st.session_state.chat_history.append({"question": follow_up_question, "answer": answer})
                    st.rerun()

    # Initial prompt
    if not st.session_state.summary and not uploaded_image:
        st.info("Please upload an image to begin.")

elif page == "About":
    st.title("About")
    st.write("""
    This app uses the Gemma-3-27b-it model to generate concise summaries of uploaded images.
    The pipeline involves:
    1. Uploading an image.
    2. Processing the image using Gemma to generate a summary.
    3. Allowing follow-up questions about the image.
    
    ORCID ID: [0009-0003-9498-3828](https://orcid.org/0009-0003-9498-3828)
    """)