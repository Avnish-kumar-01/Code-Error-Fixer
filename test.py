import streamlit as st
from google import genai 
from google.genai import types


try:
    # ⚠️ IMPORTANT: Get the API key from Streamlit secrets
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("FATAL ERROR: 'GEMINI_API_KEY' not found in .streamlit/secrets.toml.")
    st.error("Please create the file .streamlit/secrets.toml and add your key.")
    st.stop()
    
client = genai.Client(api_key=api_key)

st.title("🧠  Code Error Fixer")

file = st.file_uploader("Upload your code file", type=["py", "txt", "java", "html", "js", "ts"])

if file:
    # Read and decode the file content
    content = file.read().decode("utf-8")
    
    st.subheader("Original Code")
    st.code(content, language=file.type.split('/')[-1] if file.type else 'python')

    
    system_instruction = "You are a coding assistant that expertly fixes errors and refactors code for best practices. Respond ONLY with the complete, fixed code block. Do not include any conversational text or explanation."
    
    user_prompt = f"{system_instruction}\n\nHere is the code to fix:\n{content}"
    
    
    messages = [
        types.Content(role="user", parts=[
            types.Part(text=user_prompt) 
        ])
    ]
    
   
   

    with st.spinner("Fixing errors and refactoring code..."):
        try:
           
            response = client.models.generate_content(
                model="gemini-2.5-flash",  
                contents=messages          
            )
            
            fixed_code = response.text
            
            st.subheader("Fixed Code")
            st.code(fixed_code, language=file.type.split('/')[-1] if file.type else 'python')
            
            
            download_file_name = f"fixed_{file.name}"
            st.download_button(
                "Download Fixed File", 
                fixed_code, 
                file_name=download_file_name
            )

        except Exception as e:
            st.error(f"An API or Runtime Error Occurred: {e}")
            st.info("Check your API key, ensure the model name is correct, and verify your account quota on the Google AI Studio platform.")
side = st.sidebar.write("HOME")
st.sidebar.write("LOGIN")
name=st.sidebar.text_input("Enter your name")
if name:
    st.success(f"welcome {name} in Code Error fixer")
st.sidebar.write("LOGOUT")
lname=st.sidebar.text_input("Enter your name for logout")
if lname:
    st.error(f"{lname} logout")
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color:white;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
    }
    </style>
    <div class="footer">
        © 2025 AVNISH KUMAR | All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)