
Create a Neat Trading Log Web App with Python and Streamlit — part [1]
Mohamed Fouad
Mohamed Fouad

·
Follow

8 min read
·
Aug 10, 2023

Listen


Share

Part 1 — Create The Visual Elements Using Streamlit Framework
In this tutorial, we will focus on setting up the elements and preparing the groundwork for the actual coding process. While some may prefer to dive headfirst into the coding aspect, taking the time to properly set up the necessary elements can save you time and effort in the long run. By laying a solid foundation, the coding process can be more streamlined and efficient, leading to a better end product. However, to avoid overwhelming readers with a lengthy tutorial, we will only cover the UI setup process in this part. The actual backend coding process will be covered in Part 2 of this tutorial, where we will delve deeper and write the necessary code to bring the project to life. So, let’s take it step by step and ensure that we have a solid foundation before moving on to the more complex aspects of the project.

We’re gonna code a Trades log web app using Python and Streamlit framework to look like this:


What is Streamlit Framework?
Streamlit is a powerful and easy-to-use open-source app framework in Python that allows for the creation of beautiful web apps for data science and machine learning. It is designed to streamline the process of building interactive and data-driven apps, enabling users to focus on creating content rather than worrying about the underlying infrastructure.

One of the key benefits of Streamlit is its compatibility with major Python libraries such as scikit-learn, Keras, PyTorch, LaTeX, NumPy, Pandas, and Matplotlib, among others. This means that users can easily integrate their favorite libraries into their Streamlit apps, allowing them to leverage the full power of these tools to create robust and informative data visualizations.

Another advantage of Streamlit is its ability to facilitate collaboration and sharing among data scientists and developers. The framework provides a simple and intuitive interface for creating and sharing apps, making it easy for users to collaborate on projects and share their work with others.

Overall, Streamlit is an excellent tool for anyone looking to build interactive and data-driven web apps in Python. With its user-friendly interface, powerful library integration, and collaboration features, it is a must-have for data scientists and developers alike.

You Can Know More About Streamlit from here and Dive in their API from here

Let’s Start Creating The UI of Our Trading Webapp
First, you have to install streamlit to your system if it’s not already install. Just use the following command:

% pip install streamlit
Second, Create a new python file and import streamlit inside it, and add a write() element to it — actually it can almost write anything to screen:

import streamlit as st

st.write('Hello world')
Now just start the streamlit server by typing following command in terminal — app.py is our python file name:

% streamlit run app.py
Try to change the write() function to title() and save the file and see what happens:

import streamlit as st

st.title('Hello world')
The app will sense the change in the code and ask you to rerun the script from browser. You should get your app running in the browser and look like this:


Now Let’s Get Serious
We want our app to have 3 tabs. One for new entry, one for showing the database and one for filter section. So, we will add the following to get our tabs:

import streamlit as st

st.title('Trading Book')

tab1,tab2,tab3 = st.tabs(['New Entry','Trade Log','Filter'])

Easy, Right!

Let’s add some elements inside our first tab:

with tab1:
    st.subheader(':green[New Entry]')
    col1,col2,col3 = st.columns(3)
    with col2:
        date = st.date_input('Date')
        time = st.time_input('Time')
    with col1:
        symb = st.text_input('Symbol',).upper()
        order = st.selectbox('Order',options=['BUY','SELL'])
    with col3:
        position = st.number_input('Position')
        price = st.number_input('Price')
        #save button
    st.button('Add Trade') 

New Entry Tab
Now to The Trade Log tab, we need some data to fill the log. So I have used data from csv file to load inside our dataframe

Here, I have imported the file using pandas, created an option to upload another file if the first one is not found, and wrapped everything inside a spinner element. It will give a notification if the file is loaded successfully.

st.data_editor() loads the data inside an editable dataframe viewer

import pandas as pd
with st.spinner('Loading Tradeing Logs'):
    logb = pd.DataFrame()
    try:
        logb = pd.read_csv('base/TradeBookw.csv')
        st.toast('Data Successfully Loaded ',icon='✅')
    except:
        file = st.file_uploader(label='Upload Trade Book')
        st.toast('Data Successfully Loaded ',icon='✅')

with tab2:
        st.subheader(':green[Trade Book]')
        if len(logb)>0:
            logb = logb = st.data_editor(logb)
        elif file is not None:
             file = pd.read_csv(file)
             logb = st.data_editor(file)
    

Trading log Tab
Let’s Clean Our Dataframe Element
But, First I had to create a function to convert string date and time inside the csv file to datetime type. Then I passed my dataframe to it

def fix_df(df):
    """ Fix database date and time column"""
    df.order_date = pd.to_datetime(df.order_date)
    df.order_time = pd.to_datetime(df.order_time)
    return df

file =  fix_df(file)
Crucial thing to REMEMBER is “Streamlit renders the python file sequentially, so you have to identify variables and functions before where they called, otherwise you will get errors”.

In the following code, we modified the data_editor element for better shape. I passed the column_config={} parameter and declared the shape and types of dataframe columns:

with tab2:
        st.subheader(':green[Trade Book]')
        if len(logb)>0:
            logb = st.data_editor(logb.sort_values('order_date',ascending=False),
                              hide_index=True,
                              column_config={
                                'trade_id': st.column_config.NumberColumn(
                                    'ID',
                                    format="%d",
                                    width='small'
                                ),
                                'symb':st.column_config.TextColumn(
                                    'Ticker',
                                    width='small',

                                ),
                                'value-usd': st.column_config.NumberColumn(
                                    format="$%.2f"
                                ),
                                'order': st.column_config.SelectboxColumn(
                                    options=['BUY','SELL'],
                                    width='small',
                                ),
                                
                                'order_date':st.column_config.DateColumn(
                                    'Date',
                                    width='small',
                                    format='DD-MM-yyyy'
                                ),
                                'order_time':st.column_config.TimeColumn(
                                    'Time',
                                    width='small',
                                    format='HH:MM',

                                ),
                                'state': st.column_config.SelectboxColumn(
                                    options=['open','closed'],
                                    width='small'
                                ),

                            },use_container_width=True)

Customized data_editor( )
Notice the editable fields and drop menus.

!! Still Our Code Doesn’t Save Modifications Yet. We will change that in Part 2 of this tutorial. Wait for it :)

Nice! now to the Filter Tab:
Yes, this is the final part in this tutorial. It should be like this:


But Actually I will setup the elements only in this tutorial and do the hard coding in the next Part 2 of this tutorial, because it become too long

You should be able to filter your trade book by tickers, order type, date, and id. In order to do that we have to create some functions to do that work, but we starts only with the visual elements

Filter_UI( ) — Function to Return the User Choice
You should be able to understand the code yourself. columns here is used to arrange the view of elements and then we call it.

def filter_ui():
        """
        Draw Filter user elements

        Returns:
            choice [str]: stores the user choice of filter type 
            filter [str]: stores choice parameter
        
        """  
        filter = ''
        
        with st.container():
            # st.subheader(':green[Filter Trades]')
            col1,col2= st.columns(2)
            with col1:
                choice= st.selectbox('Filter Trades By',options=[
                    'Ticker','Trade id','Order Type','Date','Order State'
                ])
            with col2:
                if choice == 'Ticker':
                    # Enter Ticker
                    filter = st.text_input('Ticker',max_chars=4,placeholder='Symbol')
                elif choice == 'Trade id':
                    filter = str(st.number_input('Trade ID',min_value=0,key='filter id')
                elif choice == 'Date':
                    filter = str(st.date_input('Date',key='filter date'))
                elif choice == 'Order Type':
                    filter = st.selectbox('Select state',options=['All','Buy','Sell'])
                elif choice == 'Order State':
                    filter = st.selectbox('Select state',options=['All','Open','Closed'])
            
            return choice, filter


choice,filter = filter_ui()
Final Code
import streamlit as st
import pandas as pd

def fix_df(df):
    """ Fix database date and time column"""
    df.order_date = pd.to_datetime(df.order_date)
    df.order_time = pd.to_datetime(df.order_time)
    return df

st.title('Trading Book')

tab1,tab2,tab3 = st.tabs(['New Entry','Trade Log','Filter'])

with tab1:
        st.subheader(':green[New Entry]')
        col1,col2,col3 = st.columns(3)
        with col2:
            date = st.date_input('Date')
            time = st.time_input('Time')
        with col1:
            symb = st.text_input('Symbol',).upper()
            order = st.selectbox('Order',options=['BUY','SELL'])
        with col3:
            position = st.number_input('Position')
            price = st.number_input('Price')
            #save button
        st.button('Add Trade') 

with st.spinner('Loading Tradeing Logs'):
    logb = pd.DataFrame()
    try:
        logb = pd.read_csv('base/TradeBook.csv')
        logb= fix_df(logb)
        st.toast('Data Successfully Loaded ',icon='✅')
        
    except:
        file = st.file_uploader(label='Upload Trade Book')
        st.toast('Data Successfully Loaded ',icon='✅')

with tab2:
        st.subheader(':green[Trade Book]')
        if len(logb)>0:
            logb = st.data_editor(logb.sort_values('order_date',ascending=False),
                              hide_index=True,
                              column_config={
                                'trade_id': st.column_config.NumberColumn(
                                    'ID',
                                    format="%d",
                                    width='small'
                                ),
                                'symb':st.column_config.TextColumn(
                                    'Ticker',
                                    width='small',

                                ),
                                'value-usd': st.column_config.NumberColumn(
                                    format="$%.2f"
                                ),
                                'order': st.column_config.SelectboxColumn(
                                    options=['BUY','SELL'],
                                    width='small',
                                ),
                                
                                'order_date':st.column_config.DateColumn(
                                    'Date',
                                    width='small',
                                    format='DD-MM-yyyy'
                                ),
                                'order_time':st.column_config.TimeColumn(
                                    'Time',
                                    width='small',
                                    format='HH:MM',

                                ),
                                'state': st.column_config.SelectboxColumn(
                                    options=['open','closed'],
                                    width='small'
                                ),

                            },use_container_width=True)
        elif file is not None:
             file = pd.read_csv(file)
             file = fix_df(file)
             logb = st.data_editor(file.sort_values('order_date',ascending=False),
                              hide_index=True,
                              column_config={
                                'trade_id': st.column_config.NumberColumn(
                                    'ID',
                                    format="%d",
                                    width='small'
                                ),
                                'symb':st.column_config.TextColumn(
                                    'Ticker',
                                    width='small',

                                ),
                                'value-usd': st.column_config.NumberColumn(
                                    format="$%.2f"
                                ),
                                'order': st.column_config.SelectboxColumn(
                                    options=['BUY','SELL'],
                                    width='small',
                                ),
                                
                                'order_date':st.column_config.DateColumn(
                                    'Date',
                                    width='small',
                                    format='DD-MM-yyyy'
                                ),
                                'order_time':st.column_config.TimeColumn(
                                    'Time',
                                    width='small',
                                    format='HH:MM',

                                ),
                                'state': st.column_config.SelectboxColumn(
                                    options=['open','closed'],
                                    width='small'
                                ),
                            },use_container_width=True)
             
#FILTER
with tab3:
    def filter_ui():
        """
        Draw Filter user elements in the side bar

        Returns":
            choice [str]: stores the user choice of filter type 
            filter [str]: stores choice parameter
        
        """  
        filter = ''
        
        with st.container():
            # st.subheader(':green[Filter Trades]')
            col1,col2= st.columns(2)
            with col1:
                choice= st.selectbox('Filter Trades By',options=[
                    'Ticker','Trade id','Order Type','Date','Order State'
                ])
            with col2:
                if choice == 'Ticker':
                    # Enter Ticker
                    filter = st.text_input('Ticker',max_chars=4,placeholder='Symbol')
                elif choice == 'Trade id':
                    filter = str(st.number_input('Trade ID',min_value=0,key='filter id'))
                    
                elif choice == 'Date':
                    filter = str(st.date_input('Date',key='filter date'))
                elif choice == 'Order Type':
                    filter = st.selectbox('Select state',options=['All','Buy','Sell'])
                elif choice == 'Order State':
                    filter = st.selectbox('Select state',options=['All','Open','Closed'])
            
            return choice, filter
    
    choice,filter = filter_ui()
    #merge df
    st.button('Show Results')
    st.divider()
    st.subheader(':green[Filter Results]')
