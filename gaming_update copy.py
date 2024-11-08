import streamlit as st
import os
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model with the generation configuration
generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 1500,  # Increased to allow longer responses
    "response_mime_type": "text/plain",
}

def get_game_content(category, game_name, detail_level):
    prompt = f"""
    Provide a {detail_level.lower()} {category.lower()} guide for the game {game_name}. 
    Include sections like Introduction, Step-by-step Instructions, Tips & Tricks, and FAQs.
    """
    
    if detail_level == "Detailed":
        prompt += " Add advanced strategies, pro tips, and avoid common mistakes."

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        
        content = response.text if response else 'No content available'
        return content
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Guild Game AI Bot", page_icon="🎮")
    st.title("Guild Game AI Bot")
    st.write("Get detailed information about your favorite games!")

    categories = ["Installation", "Guideline", "Review", "Speedrun", "News"]
    selected_category = st.selectbox("Select a category:", categories)

    if selected_category:
        detail_level = st.selectbox("Select the level of detail:", ["Basic", "Intermediate", "Detailed"])
        game_name = st.text_input(f"Enter the name of the game for {selected_category.lower()}:")

        if game_name:
            st.subheader(f"{selected_category} for {game_name} ({detail_level} Level)")
            content = get_game_content(selected_category, game_name, detail_level)
            if content:
                st.write(content)

if __name__ == "__main__":
    main()
