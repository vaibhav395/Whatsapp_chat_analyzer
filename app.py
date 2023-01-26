import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer : Made by Vaibhav Thareja")

#This is a function from streamlit documentation
uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    #The uploaded file is currently a stream of byte data
    #we have to convert this stream into a string

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    #fetching unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        #All the stats
        num_messages, number_of_words, number_of_media, number_of_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(number_of_words)
        with col3:
            st.header("Media Shared")
            st.title(number_of_media)
        with col4:
            st.header("Links Shared")
            st.title(number_of_links)

        #Finding the most active users in the group (group level)
        if selected_user == 'Overall':
            st.title('Most Active users in chat')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #Creaing wordcloud
        st.title("WordCloud of the Chats")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)