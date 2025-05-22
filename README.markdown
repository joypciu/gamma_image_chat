# Image Summary Generator

![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1+-FF4B4B)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB)
![Google Generative AI](https://img.shields.io/badge/Google_GenAI-1.16.1+-4285F4)

A Streamlit web application that generates concise summaries of uploaded images using the Google Generative AI API (Gemma model). Users can upload images (JPG, JPEG, PNG) and ask follow-up questions about the image content in a chat-like interface. The app features a dark theme for a modern user experience.

## Features

- **Image Summarization**: Upload an image to generate a 2-4 line summary using the Gemma-3-27b-it model.
- **Interactive Chat**: Ask follow-up questions about the image, with responses based on the image content or summary.
- **Dark Theme**: Sleek UI with a dark background, white text, and cyan buttons.
- **Error Handling**: Robust logging and user feedback for invalid inputs or API errors.
- **Secure API Key Management**: Uses a `.env` file to securely store the Google Generative AI API key.

## Demo

The app is deployed on Streamlit Community Cloud: [View Live Demo](https://your-app-name.streamlit.app) *(Replace with your actual Streamlit URL after deployment)*.

## Prerequisites

- Python 3.8 or higher
- A Google Generative AI API key (sign up at [Google AI Studio](https://aistudio.google.com/))
- Git installed for cloning the repository
- A Streamlit Community Cloud account for deployment (optional)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/image-summary-app.git
   cd image-summary-app
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` includes:
   - `google-genai>=1.16.1`
   - `streamlit>=1.45.1`
   - `pillow>=11.2.1`

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root:
     ```bash
     touch .env  # On Windows: echo. > .env
     ```
   - Add your Google Generative AI API key:
     ```env
     GEMINI_API_KEY=your-api-key-here
     ```
   - The `.env` file is ignored by `.gitignore` to prevent accidental uploads.

5. **Run the App Locally**:
   ```bash
   streamlit run main.py
   ```
   - Open your browser to `http://localhost:8501` to view the app.

## Usage

1. **Upload an Image**:
   - On the home page, upload a JPG, JPEG, or PNG image using the file uploader.
   - The app processes the image and displays a concise summary (2-4 lines).

2. **View Summary**:
   - The uploaded image and its summary are shown below the uploader.
   - The summary is generated using the Gemma-3-27b-it model.

3. **Ask Follow-Up Questions**:
   - Use the chat input box to ask questions about the image (e.g., "What’s in the background?").
   - Responses are based on the image content or summary, with a maximum of 150 tokens.

4. **Reset or Clear**:
   - Click **Reset App** to clear everything and start over.
   - Click **Clear Chat** to reset the chat history while keeping the image and summary.

## Deployment on Streamlit Community Cloud

To deploy the app as a webpage:

1. **Push to GitHub**:
   - Ensure `main.py`, `requirements.txt`, and `.gitignore` are in your GitHub repository.
   - Do **not** include `.env` or `app.log`.
   - Example commands:
     ```bash
     git add main.py requirements.txt .gitignore
     git commit -m "Initial commit"
     git push origin main
     ```

2. **Deploy on Streamlit Cloud**:
   - Sign in to [Streamlit Community Cloud](https://streamlit.io/cloud) with GitHub.
   - Create a new app, selecting your repository and `main.py` as the main file.
   - In **Advanced settings**, add your `GEMINI_API_KEY` as an environment variable.
   - Deploy the app and access it via the provided URL.

## Project Structure

```
image-summary-app/
├── main.py              # Main Streamlit app code
├── requirements.txt     # Python dependencies
├── .gitignore           # Ignored files (.env, app.log)
└── .env                 # Local file for API key (not in Git)
```

## Troubleshooting

- **API Key Errors**:
  - Ensure `GEMINI_API_KEY` is set in `.env` locally or in Streamlit Cloud’s **Advanced settings**.
  - Verify the key is valid via [Google AI Studio](https://aistudio.google.com/).

- **Dependency Issues**:
  - Update dependencies:
    ```bash
    pip install --upgrade google-genai streamlit pillow
    pip freeze > requirements.txt
    ```
  - Check Streamlit Cloud logs for installation errors.

- **Model Errors**:
  - The app uses `gemma-3-27b-it`. If unavailable, update `main.py` to use `gemini-1.5-flash` or another supported model:
    ```python
    st.session_state.chat_session = client.chats.create(model="gemini-1.5-flash")
    ```

- **UI Issues**:
  - If the dark theme doesn’t apply, verify the CSS in `main.py` under `st.markdown(css, unsafe_allow_html=True)`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. *(Add a LICENSE file if you choose to include one)*

## Author

- ORCID: [0009-0003-9498-3828](https://orcid.org/0009-0003-9498-3828)

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web app framework.
- [Google Generative AI](https://aistudio.google.com/) for the Gemma model.
- [Pillow](https://python-pillow.org/) for image processing.