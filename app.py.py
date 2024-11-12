import streamlit as st
import tensorflow as tf
import tensorflow_text as tf_text  # Required for the saved model to work

def load_translator_model():
    """Load the saved translator model."""
    try:
        model = tf.saved_model.load('translator')
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def translate_text(model, text):
    """Translate Bengali text to English using the loaded model."""
    try:
        result = model.translate(tf.constant([text]))
        return result[0].numpy().decode()
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None

def main():
    st.title("Bengali to English Translator")
    st.write("Enter Bengali text below to translate it to English")

    # Load the model
    @st.cache_resource
    def get_model():
        return load_translator_model()
    
    model = get_model()

    if model is None:
        st.error("Failed to load the translator model. Please check if the model files are present in the 'translator' directory.")
        return

    # Create the input text area
    input_text = st.text_area("Enter Bengali text:", height=100)

    if st.button("Translate"):
        if input_text:
            with st.spinner("Translating..."):
                translation = translate_text(model, input_text)
                if translation:
                    st.success("Translation:")
                    st.write(translation)
        else:
            st.warning("Please enter some text to translate.")

    # Add some usage examples
    with st.expander("See example translations"):
        st.write("Try these Bengali phrases:")
        examples = {
            "আপনি কেমন আছেন?": "How are you?",
            "আমি বাড়িতে যাচ্ছি।": "I am going home.",
            "টম মিথ্যা কথা বললো।": "Tom lied."
        }
        for ben, eng in examples.items():
            st.write(f"Bengali: {ben}")
            st.write(f"English: {eng}")
            st.write("---")

if __name__ == "__main__":
    main()
