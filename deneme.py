import streamlit as st
import time
import random
import plotly.express as px
import pandas as pd
import numpy as np
import psycopg2

st.set_page_config(layout="wide")
placeholder = st.empty()
start_button = st.empty()


def radar_chart():
  df = pd.DataFrame(dict(
    r=[random.randint(0, 22),
       random.randint(0, 22),
       random.randint(0, 22),
       random.randint(0, 22),
       random.randint(0, 22)],
    theta=['processing cost', 'mechanical properties', 'chemical stability',
           'thermal stability', 'device integration']))
  fig = px.line_polar(df, r='r', theta='theta', line_close=True)
  placeholder.write(fig)
def formCreate(count):
    inner_cols = st.columns([1,1,1])
    with st.form(key=str(count)):
        text = st.text_area("Elif",value = "Bu bir Text Alanıdır...")
        colOne, colTwo, colThree = st.columns(3)
        with inner_cols[0]:
            choice = colOne.selectbox(
                "Etiketi Seçiniz",
                ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri", "Müşteri Temsilcisi", "Diğer"), key=str(count)
            )
        with inner_cols[1]:
            deleteButon = colTwo.form_submit_button("Sil")
        with inner_cols[2]:
            approveButon = colThree.form_submit_button("Onayla")

def repeat(count):
    start_button.empty()
    if start_button.button('Start',key=str(count)):
        start_button.empty()
        # while True:
            # formCreate(count)
        inner_cols = st.columns([1, 1, 1])
        with st.form(key=str(count)+"formUnique"):
            text = st.text_area("Elif", value="Bu bir Text Alanıdır...")
            colOne, colTwo, colThree = st.columns(3)
            with inner_cols[1]:
                deleteButon = colTwo.form_submit_button("Sil")
            with inner_cols[2]:
                approveButon = colThree.form_submit_button("Onayla")
            with inner_cols[0]:
                choice = colOne.selectbox(
                        "Etiketi Seçiniz",
                        ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri", "Müşteri Temsilcisi", "Diğer"),
                        key=str(count)+"target"
                )

def buttonComplaints():
    for i in range(10):
        start_button = st.empty()
        if start_button.button(f'Complaint {i+1}',key=str(i)):
            start_button.empty()
            inner_cols = st.columns([1, 1, 1])
            with st.form(key=str(i)):
                text = st.text_area("Elif", value="Bu bir Text Alanıdır...")
                colOne, colTwo, colThree = st.columns(3)
                with inner_cols[1]:
                    deleteButon = colTwo.form_submit_button("Sil")
                with inner_cols[2]:
                    approveButon = colThree.form_submit_button("Onayla")
                with inner_cols[0]:
                    choice = colOne.selectbox("Etiketi Seçiniz",
                            ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri", "Müşteri Temsilcisi", "Diğer"),
                            key=str(i)+"choice")
# buttonComplaints()
def formComplaints():
    for i in range(10):
        start_button = st.form(key=str(i))
        if start_button.button(f'Complaint {i+1}',key=str(i)):
            start_button.empty()
            inner_cols = st.columns([1, 1, 1])
            with st.form(key=str(i)):
                text = st.text_area("Elif", value="Bu bir Text Alanıdır...")
                colOne, colTwo, colThree = st.columns(3)
                with inner_cols[1]:
                    deleteButon = colTwo.form_submit_button("Sil")
                with inner_cols[2]:
                    approveButon = colThree.form_submit_button("Onayla")
                with inner_cols[0]:
                    choice = colOne.selectbox("Etiketi Seçiniz",
                            ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri", "Müşteri Temsilcisi", "Diğer"),
                            key=str(i)+"choice")

def deneme():
    for i in range(10):
        st.write(i)
        placeholder = st.empty()
        with placeholder.form(key = str(i)):
            inner_cols = st.columns([1, 1, 1])
            text = st.text_area("Elif", value="Bu bir Text Alanıdır...")
            colOne, colTwo, colThree = st.columns(3)
            choice = colOne.selectbox("Etiketi Seçiniz",
                                           ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri",
                                            "Müşteri Temsilcisi", "Diğer"),
                                            key=str(i) + "choice")
        deleteButon = colTwo.form_submit_button("Sil")
        if deleteButon:
            if i == 0:
                st.write(f"{i} id'li kisi silindi.")
                placeholder.empty()
        approveButon = colThree.form_submit_button("Onayla")
        if approveButon:
            if choice == "Kredi İşlemleri":
                st.write(choice)
                placeholder.empty()

# deneme()
def placeholderFunction():
    placeholder = st.empty()
    with placeholder.form("my_form"):
        st.write("Inside the form")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
           st.write("slider", slider_val, "checkbox", checkbox_val)
           placeholder.empty()

    st.write("Outside the form")
# placeholderFunction()
def login():
    # Create an empty container
    placeholder = st.empty()

    actual_email = "email"
    actual_password = "password"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and email == actual_email and password == actual_password:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.success("Login successful")
    elif submit and email != actual_email and password != actual_password:
        st.error("Login failed")
    else:
        pass

def multiPage():
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # st.set_page_config(layout="wide")

    df = pd.DataFrame(px.data.gapminder())

    st.header("National Statistics")

    page = st.sidebar.selectbox('Select page', ['Country data', 'Continent data'])

    if page == 'Country data':

        ## Countries
        clist = df['country'].unique()

        country = st.selectbox("Select a country:", clist)

        col1, col2 = st.columns(2)

        fig = px.line(df[df['country'] == country],
                      x="year", y="gdpPercap", title="GDP per Capita")
        col1.plotly_chart(fig, use_container_width=True)

        fig = px.line(df[df['country'] == country],
                      x="year", y="pop", title="Population Growth")
        col2.plotly_chart(fig, use_container_width=True)

    else:
        ## Continents

        contlist = df['continent'].unique()

        continent = st.selectbox("Select a continent:", contlist)

        col1, col2 = st.columns(2)
        fig = px.line(df[df['continent'] == continent],
                      x="year", y="gdpPercap",
                      title="GDP per Capita", color='country')
        col1.plotly_chart(fig)

        fig = px.line(df[df['continent'] == continent],
                      x="year", y="pop",
                      title="Population", color='country')
        col2.plotly_chart(fig)

# outer_cols = st.columns([1,1,1])
# with outer_cols[0]:
#     placeholder = st.empty()
#     with placeholder.form(key="form"):
#
#         inner_cols = st.columns([1,1,1])
#         col1,col2,col3 = st.columns(3)
#         with inner_cols[0]:
#             col1.button("Buton")
#         with inner_cols[1]:
#             col2.checkbox("Checkbox")
df = pd.read_csv("../databaseConnect/database.csv")
hostname = "localhost"
port_id = 5432
database = "nlpDatabase"
username = "postgres"
password = "Eliftosun123"

def sqlExecute(raw_code):
    with psycopg2.connect(host=hostname,port=port_id,dbname=database,user=username,password=password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(*raw_code)
            conn.commit() # save
def sqlData(raw_code):
    with psycopg2.connect(host=hostname,port=port_id,dbname=database,user=username,password=password) as conn:
        with conn.cursor() as curs:
            curs.execute(raw_code)
            conn.commit()
            data = curs.fetchall()
            return data
def sidebarPanel():
    with st.sidebar:
        def user():
            user = st.text_input("👤 Kullanıcı adınızı giriniz", key="user")
            userButton = st.button("📁 Kaydet")
            userIdTotalQuery = "select id from users"
            userIdQuery = f"select id from users where username = '{user}'"
            userId = sqlData(userIdQuery)
            userIdTotalQuery = sqlData(userIdTotalQuery)
            usersDf = pd.DataFrame(userIdTotalQuery, columns=["users"])
            usersIdList = []
            for i in range(len(usersDf)):
                usersIdList.append(usersDf.iloc[i,0])
            if userButton:
                if userId in usersIdList:
                    with st.spinner('Giriş yapılıyor...'):
                        time.sleep(0.5)
                    st.warning(f"Hoşgeldin {user} :smile:")
                    userIdDf = pd.DataFrame(userId)
                    return userIdDf.iloc[0,0]
                else:
                    insertQuery = f"insert into users (id,username) values ({len(usersDf)},'{user}')"
                    insertQuery = sqlExecute(insertQuery)
                    if insertQuery == None:
                        with st.spinner('Kaydınız yapılıyor...'):
                            time.sleep(0.5)
                        st.success(f"Hoşgeldin {user} :smile:")
                    userIdQuery = sqlData(f"select id from users where id = {len(usersDf)}")
                    userIdDf = pd.DataFrame(userIdQuery)
                    return userIdDf.iloc[0,0]
        def file():
            cho = st.selectbox("Dataset indirme biçimini seçiniz",("csv","excel","json"))
            if cho == "csv":
                st.download_button(
                    label="📥 Download data as CSV",
                    data=df.to_csv().encode("utf-8"),
                    file_name='bank_deneme.csv',
                    mime='text/csv',
                )
            elif cho == "excel":
                file_path = "../databaseConnect/database.csv"
                with open(file_path, 'rb') as my_file:
                    st.download_button(label='📥 Download data as Excel', data=my_file, file_name='bank_deneme.xlsx',
                                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            elif cho == "json":
                st.download_button(
                    label="📥 Download data as Json",
                    data=df.to_json(),
                    file_name="bank_deneme.json",
                    mime="text/json"
                )
        userId = user()
        file()
    return userId

import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)


userId = sidebarPanel()
st.write(userId)
insertQuery = """insert into targets (id,target,targetuser) values (%s,%s,%s)""",(193,'Müşteri Temsilcisi',userId)
insertQuery = sqlExecute(insertQuery)
if insertQuery == None:
    # placeholder.empty()
    st.success(f"{193} id'li şikayet veritabanına aktarıldı.")
else:
    # placeholder.empty()
    st.info(f"{193} id'li şikayet targets tablosunda bulunuyor...")
# data = pd.read_csv("../databaseConnect/database.csv")
#
# data_list = [list(row) for row in data.itertuples(index=False)]
# print(data_list)
# deneme()
# for i in range(10):
#     placeholder = st.empty()
#     column1 = placeholder.form(key=str(i)+"form")
#     # inner_cols = st.columns([1, 1, 1])
#     text = column1.text_area(f"Text Area {i+1}", value=f"Bu bir {i+1}. Text Alanıdır...")
#     col1,col2,col3 = column1.columns(3)
#     choice = col1.selectbox("Etiketi Seçiniz",("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri",
#                                 "Müşteri Temsilcisi", "Diğer"),key=str(i)+"select")
#     submit = col2.form_submit_button("Onayla")
#     if submit:
#         placeholder.empty()
#     # if submit:
#     #     if choice == "Kredi İşlemleri":
#     #         placeholder.empty()
#     #     if choice == "Bankacılık İşlemleri":
#     #         placeholder.empty()
#     #     if choice == "Kart İşlemleri":
#     #         placeholder.empty()
#     delete = col3.form_submit_button("Sil")
#     if delete:
#         placeholder.empty()
#     st.write(i)

# with inner_cols[1]:
#     choice = column1.selectbox("Etiketi Seçiniz",
#                                            ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri",
#                                             "Müşteri Temsilcisi", "Diğer"),
#                                                 key="deneme" + "choice")
# elif column2.button("Click me2"):
#     placeholder.empty()
# elif column3.button("Click me3"):
#     placeholder.empty()



# placeholder = st.empty()
# with placeholder.container():
#   st.number_input("One", value=1)
#   st.number_input("Two", value=2)
#
#   if st.button('Clear & Add'):
#     placeholder.empty()
#     with placeholder.container():
#       st.number_input("One - Second", value=3)
#       st.number_input("Two - Second", value=4)
#       st.number_input("Three", value=5)


# if session_state.password != 'pwd123':
#    title = st.empty()
#    title.title("Welcome to this page")
#    subtitle = st.empty()
#    subtitle.header("Please enter your login details to proceed")
#    login = st.empty()
#    login.subheader("LOGIN")
#    login_id = st.empty()
#    log_name = login_id.text_input("Ad")
#    print(login_id)
#    pwd_placeholder = st.empty()
#    pwd = pwd_placeholder.text_input("Password:", value="", type="password")
#    session_state.password = pwd
#    if session_state.password == 'pwd123':
#        pwd_placeholder.empty()
#        title.empty()
#        subtitle.empty()
#        login.empty()
#        login_id.empty()
#        main()
#    elif session_state.password != '':
#        st.error("the password you entered is incorrect")
# else:
#    main()