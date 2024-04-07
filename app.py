import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# File upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read and preprocess the data
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    data = preprocessor.preprocess(data)
    # st.dataframe(data)

    # Fetch unique users for dropdown
    users_list = data['user'].unique().tolist()
    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0, "Overall")

    # Analysis section
    selected_user = st.sidebar.selectbox("Show analysis with respect to", users_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_msg, num_links = helper.fetch_stats(selected_user, data)
        st.title("Top Statistics")

        # Display analysis metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_msg)
        with col4:
            st.header("Links shared")
            st.title(num_links)

            # Monthly Timeline 
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, data)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, data)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'],daily_timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Activity map
        st.title('Activity Map')
        col1 , col2 = st.columns(2)
         
        with col1:
            st.header('Most busy days')
            busy_day = helper.weekly_activity_map(selected_user,data)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy months')
            busy_month = helper.month_activity_map(selected_user,data)
            fig , ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,data)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

        



        # Plot busiest users (if 'Overall' is selected)
        if selected_user == 'Overall':
            st.title("Busiest Users")
            x, new_data = helper.most_busy_users(data)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                ax.set_xticks(x.index)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_data)

        # WordCloud
        st.title("WordCloud")
        data_wc = helper.create_wordcloud(selected_user, data)
        fig , ax = plt.subplots()
        ax.imshow(data_wc)
        st.pyplot(fig)

        # Most Common words
        most_common_data = helper.most_common_words(selected_user,data)
        fig, ax = plt.subplots()
        ax.barh(most_common_data['Word'], most_common_data['Frequency'])
        plt.xticks(rotation = 'vertical')
        st.title("Most common words")
        st.pyplot(fig)
        st.dataframe(most_common_data)

        # Emoji Analysis
        emoji_data = helper.emoji_helper(selected_user, data)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
          st.dataframe(emoji_data)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_data['Count'], labels=emoji_data['Emoji'], autopct='%1.1f%%')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)