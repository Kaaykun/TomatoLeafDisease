import streamlit as st
import requests
import io
import PIL.Image

st.set_page_config(page_title='Tomato Leaf Disease Detection', page_icon='🍅🍃', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('Tomato Leaf Disease Detection 🍅🍃')
with st.sidebar:
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This web app is maintained by [Jaris fenner](https://linktr.ee/jaris_fenner). You can follow me on social media:
            [GitHub](https://github.com/Kaaykun) | [LinkedIn](https://www.linkedin.com/in/jaris-fenner).

        Source code: <https://github.com/Kaaykun/TomatoLeafDisease>

        To run the app, follow the instructions in the source code README file.
    """
    )

image = st.file_uploader('Upload your tomato leaf image:', type=['png', 'jpg', 'jpeg'])

if image is not None:
    img = PIL.Image.open(image)
    st.image(img, caption='Uploaded Image', use_column_width=False)

    button = st.button('Classify Condition')

    if button:
        img_as_byte = io.BytesIO()
        img.save(img_as_byte, format='PNG')
        img_byte_arr = img_as_byte.getvalue()

        response = requests.post('http://localhost:8000/identify', files={"file": img_byte_arr})
        response.raise_for_status()
        st.success("Identification successful!")

        result = response.json()
        st.markdown(f"**Prediction:** {result['prediction']}")
        st.markdown(f"**Confidence:** {round(result['confidence'], 2)}")
