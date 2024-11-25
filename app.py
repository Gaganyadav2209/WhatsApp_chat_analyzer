import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from mplcursors import cursor

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_date = uploaded_file.getvalue()
    data = bytes_date.decode("utf-8")
    df = preprocess.preprocess(data)

    ##unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis with user",user_list)


    if st.sidebar.button("Show Analysis"):

        ##Stats

        number_of_messages,words,number_of_media_messages,number_of_links = helper.fetch_stats(selected_user,df)
        st.title('Chat Statistics')
        col1 , col2 , col3 , col4 = st.columns(4)

        with col1:
            st.header('Total messages')
            st.title(number_of_messages)

        with col2:
            st.header('Total words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(number_of_media_messages)
        with col4:
            st.header('Total Links Shared')
            st.title(number_of_links)

        # Monthly Timeline
        st.title('Monthly Timeline')
        custom_font = 'DIN Condensed'
        monthly_timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        cursor(hover=True)
        ax.plot(monthly_timeline['time'], monthly_timeline['message'],color='blueviolet',linewidth=2.5)
        plt.xticks(rotation='vertical',fontname=custom_font)
        plt.yticks(fontname=custom_font)
        plt.ylabel('Messages', fontname=custom_font, fontsize=18)

        st.pyplot(fig)

        # Daily Timeline
        st.title('Daily Timeline')
        custom_font = 'DIN Condensed'
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='blueviolet',linewidth=1.5)
        plt.xticks(rotation='vertical',fontname=custom_font)
        plt.yticks(fontname=custom_font)
        plt.ylabel('Messages',fontname=custom_font,fontsize=18)
        st.pyplot(fig)

        #Daily Activity
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            custom_font = 'DIN Condensed'
            busy_day = helper.day_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='blueviolet')
            plt.xticks(rotation='vertical',fontname=custom_font)
            plt.yticks(fontname=custom_font)
            plt.ylabel('Messages', fontname=custom_font, fontsize=18)
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            custom_font = 'DIN Condensed'
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='blueviolet')
            plt.xticks(rotation='vertical',fontname=custom_font)
            plt.yticks(fontname=custom_font)
            plt.ylabel('Messages', fontname=custom_font, fontsize=18)
            st.pyplot(fig)

        # User heatmap
        st.title('Weekly Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax  = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xticks(fontname=custom_font)
        plt.xlabel('Period',fontname=custom_font,fontsize=18)
        plt.ylabel('Day Name',fontname=custom_font,fontsize=18)
        plt.yticks(fontname=custom_font)
        st.pyplot(fig)


        # Busiest user in the group

        if selected_user == 'Overall':
            st.title('Most Active Users')
            custom_font = 'DIN Condensed'
            x,new_df = helper.most_active_users(df)
            fig,ax = plt.subplots()
            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='blueviolet')
                plt.xticks(rotation='vertical',fontname=custom_font,fontsize=16)
                plt.xlabel('User Name',fontname=custom_font,fontsize=18)
                plt.yticks(fontname=custom_font,fontsize=18)
                plt.ylabel('Messages',fontname=custom_font,fontsize=18)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        plt.xticks(fontname=custom_font)
        plt.yticks(fontname=custom_font)
        st.pyplot(fig)

        #Most Common words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='blueviolet')
        # plt.xticks(rotation='vertical')
        plt.xlabel('Count',fontname=custom_font,fontsize=18)
        plt.ylabel('Words',fontname=custom_font,fontsize=18)
        plt.xticks(fontname=custom_font)
        plt.yticks(fontname=custom_font)
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.emoji_count(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)

















