#importing the required packages 
import streamlit as st
import pandas as pd
import psycopg2
import os 
import json
import plotly.express as px
from streamlit_option_menu import option_menu
from git.repo.base import Repo
from PIL import Image



#setting the page  configuration
st.set_page_config(page_title="Phonepe Pulse Visualization",
                   layout='wide',
                   
                   )

#configuring postgresSQL required for the calculations
mydb= psycopg2.connect(host="localhost",
            user="postgres",
            password="Preethi@1804",
            database= "phonepe",
            port = "5432"
            )
mycursor = mydb.cursor()

#creating a title for the page
st.title('_Phonepe Pulse Visualizations_')

#creating a topbar menu 
topbar=option_menu(
    menu_title=None,
    options=['Top Charts','Data Exploration'],
    icons=['file-bar-graph','search'],
    orientation='horizontal',
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f0f0"},
        "icon": {"color": "orange", "font-size": "16.5px"}, 
        "nav-link": {"font-size": "16.5px", "text-align": "left", "margin":"0px", "--hover-color": " #6739b7"},
        "nav-link-selected": {"background-color": " #6739b7"},
    }
    )



        

#creating top10 visualizations for Transactions and users 
if topbar == "Top Charts":
    

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        Type = st.selectbox("**Type**", ("Transactions", "Users"))

    with col2:
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            Years = st.slider("**Years**", min_value=2018, max_value=2022)
        with col2_2:
            Quarter = st.radio("Quarter", [1, 2, 3, 4], index=0, horizontal=True)

    
    if Type == "Transactions":
    
        
        col1, col2, = st.columns([1, 1], gap="small")

        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f'''
                SELECT "states", 
                    SUM("transaction_count") as Total_Transactions_Count, 
                    SUM("transaction_amount") as Total 
                FROM aggt 
                WHERE "years" = \'{(Years)}\' AND "quarter" = {int(Quarter)}  
                GROUP BY "states" 
                ORDER BY Total DESC 
                LIMIT 10
            ''')
            df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'transactions_count', 'total_amount'])
            fig = px.pie(df, values='total_amount',
                        names='state',
                        title='Top 10',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['transactions_count'],
                        labels={'transactions_count': 'transactions_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f'''
                    SELECT "districts",
                        SUM("transaction_count") as Total_Count,
                        SUM("transaction_amount") as Total
                    FROM mapt
                    WHERE "years" = \'{Years}\' AND "quarter" = {Quarter}
                    GROUP BY "districts"
                    ORDER BY Total DESC
                    LIMIT 10
                        ''')
                df = pd.DataFrame(mycursor.fetchall(), columns=['districts', 'transactions_count','total_amount'])

                fig = px.pie(df, values='total_amount',
                                names='districts',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['transactions_count'],
                                labels={'transactions_count':'transactions_count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
                #insights about the pie chart
        with st.container():
                    st.markdown(
                '''
                <div style="background-color: #000000; padding: 15px; border-radius: 10px;">
                    <p style="font-size: 18px;">The pie-charts provide valuable insights on the Transaction data</p>
                    <p style="font-size: 18px;">The state pie-chart gives insights on top 10 states that have done transactions using PhonePe</p>
                    <p style="font-size: 18px;">The District pie-chart provides info on the top 10 districts based on the number of transactions</p>
                    <p style="font-size: 18px;">The required parameters can be set using the slider and radio at the top</p>
                </div>
                ''',
                unsafe_allow_html=True
            )
        
                
               
                

    if Type == "Users":
                    
            col1,col2 = st.columns([1,1],gap="small")
                
            with col1:
                          
                          st.markdown("### :violet[Brands]")
                          if Years == 2022 and Quarter in [2,3,4]:
                            st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")

                          else:
                                 mycursor.execute(f'''
                                                SELECT "brands",
                                                    SUM("transaction_count") as Total_Count,
                                                    AVG("percentage") * 100 as Avg_Percentage
                                                FROM aggu
                                                WHERE "years" = \'{Years}\'AND "quarter" = {Quarter}
                                                GROUP BY "brands"
                                                ORDER BY Total_Count DESC
                                                LIMIT 10
                                                ''')
                                 
                                 df = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'TotalUsers','Avg_Percentage'])
                                 fig = px.bar(df,
                                            title='Top 10',
                                            x="TotalUsers",
                                            y="Brands",
                                            orientation='h',
                                            color='Avg_Percentage',
                                            color_continuous_scale=px.colors.sequential.Agsunset)
                                 st.plotly_chart(fig,use_container_width=True)   
            with col2:
                        st.markdown("### :violet[Districts]")
                        mycursor.execute( f'''
                                            SELECT "districts",
                                                SUM("RegisteredUser") as Total_Users,
                                                SUM("AppOpens") as Total_Appopens
                                            FROM mapu
                                            WHERE "years" =\'{Years}\' AND "quarter" = {Quarter}
                                            GROUP BY "districts"
                                            ORDER BY total_Users DESC
                                            LIMIT 10
                                        ''')

                        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                        df.Total_Users = df.Total_Users.astype(float)
                        fig = px.bar(df,
                                    title='Top 10',
                                    x="Total_Users",
                                    y="District",
                                    orientation='h',
                                    color='Total_Users',
                                    color_continuous_scale=px.colors.sequential.Agsunset)
                        st.plotly_chart(fig,use_container_width=True)
            
            #insights about the pie chart
            with st.container():
                    st.markdown(
                '''
                <div style="background-color: #000000; padding: 15px; border-radius: 10px;">
                    <p style="font-size: 18px;">The bar charts provide valuable insights on the user data</p>
                    <p style="font-size: 18px;">The brand  bar chart gives insights on most used mobile brands on which the phonepe app is used</p>
                    <p style="font-size: 18px;">The District bar chart provides info on the top 10 districts based on the number of users in the district</p>
                    <p style="font-size: 18px;">The required parameters can be set using the slider and radio at the top</p>
                </div>
                ''',
                unsafe_allow_html=True
            )


#creating geo visualization for data exploration for transaction and users 

if topbar == 'Data Exploration':
        col1, col2 = st.columns([1, 1], gap="small")

        with col1:
            Type = st.selectbox("**Type**", ("Transactions", "Users"))

        with col2:
            col2_1, col2_2 = st.columns(2)

            with col2_1:
                Years = st.slider("**Years**", min_value=2018, max_value=2022)

            with col2_2:
                Quarter = st.radio("Quarter", [1, 2, 3, 4], index=0, horizontal=True)

        if Type == "Transactions":
        
                st.markdown("## :violet[Overall State Data - Transactions Amount]")
                mycursor.execute(f'''
                            SELECT "states",
                                SUM("transaction_count") as Total_Transactions,
                                SUM("transaction_amount") as Total_amount
                            FROM mapt
                            WHERE "years" = \'{Years}\' AND "quarter" = {Quarter}
                            GROUP BY "states"
                            ORDER BY "states"
                        ''')
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['states', 'total_transactions', 'total_amount'])
                df2 = df1['states']
                df2=df2.drop_duplicates()

                fig = px.choropleth(df1,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='states',
                        color='total_amount',
                        labels={'states'},
                        hover_data=['total_amount', 'total_transactions', 'states'],
                        color_continuous_scale='sunset'
                    )

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(geo=dict(
                                center=dict(lon=78, lat=23),
                                projection_scale=5
                            ))
                fig.update_geos(showsubunits=True, subunitcolor="Black")
                fig.update_layout(width=600, height=700)
               

                st.plotly_chart(fig,use_container_width=True)
            

        if Type=='Users':
                st.markdown("## :violet[Overall State Data - User App opening frequency]")
                mycursor.execute(f'''
                    SELECT "states",
                        SUM("RegisteredUser") as Total_Users,
                        SUM("AppOpens") as Total_Appopens
                    FROM mapu
                    WHERE "years" = \'{Years}\' AND "quarter" = {Quarter}
                    GROUP BY "states"
                    ORDER BY "states"
                ''')
                df1 = pd.DataFrame(mycursor.fetchall(), columns=['states', 'RegisteredUser','AppOpens'])
                df2 = df1['states']
                df1['AppOpens'] = df1['AppOpens'].astype(float)
                    
        
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                        featureidkey='properties.ST_NM',
                                        locations='states',
                                        labels={'states'},
                                        hover_data=['states'],
                                        color='AppOpens',
                                        color_continuous_scale='sunset'
                                        )
                                

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(geo=dict(
                                center=dict(lon=78, lat=23),
                                projection_scale=5
                            ))
                fig.update_geos(showsubunits=True, subunitcolor="Blue")
                fig.update_layout(width=600, height=700)

                st.plotly_chart(fig,use_container_width=True)
        
        #insights about the geo viz
        with st.container():
                            st.markdown(
                        '''
                        <div style="background-color: #000000; padding: 15px; border-radius: 10px;">
                            <p style="font-size: 18px;">The geo viz makes it easy to understand the data of the respective states</p>
                            <p style="font-size: 18px;">Selecting thr 'transaction' option from the dropdown gives insigth on the statewise transactions</p>
                            <p style="font-size: 18px;">Selecting the 'users' option from the dropdown provides insights on the statewise user data </p>
                            <p style="font-size: 18px;">The required parameters can be set using the slider and radio at the top</p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )


            