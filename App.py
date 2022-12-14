# python.exe -m pip install --upgrade pip
#pip install streamlit --upgrad
import streamlit as st

st.set_page_config(
    page_title="Lyric Sketch",
    page_icon= "musical_score",
)

def main_page():
    st.title("Introduction")
    st.header("Lyric Sketch")
    # st.sidebar.title("Menu")
    st.write('The performance style of Tsai is usually combined with dancing, which is quite dissimilar to Chen’s. According to Spotify statistics, both artists belong to "taiwan pop," "mandopop," and "taiwan singer-songwriter" genres. Nevertheless, the two singers have different style tags. Tsai has other style labels such as “singaporean mandopop,” “mainland chinese pop,” and “taiwan idol pop,” which differ from Chen’s style labels (“chinese indie,” and “"taiwan indie”).*But, how are the linguistic features of their lyrics?* :sunglasses:')
    st.video('https://www.youtube.com/watch?v=0EN3MnGEBXk')
    st.video('https://www.youtube.com/watch?v=tXu-4BcZfE0')  
if __name__=="__main__":
    main_page()
# def Home():
#     st.markdown("# Home ❄️")
#     st.sidebar.markdown("# Home ❄️")

# def Data():
#     st.markdown("# Data 🎉")
#     st.sidebar.markdown("# Data 🎉")

# page_names_to_funcs = {
#     "Main Page": main_page,
#     "Home": Home,
#     "Data": Data,
# }

# selected_page = st.sidebar.selectbox("Menu", page_names_to_funcs.keys())
# page_names_to_funcs[selected_page]()


# st.sidebar.success("Menu")

# from multiapp import MultiApp
# from apps import home,data,model
# app = MultiApp()
# #add all aplication
# app.add_app("Home",home.app)
# app.add_app("Data", data.app)
# app.add_app("Model", model.app)
# # The main app
# app.run()
# #streamlit run app.py