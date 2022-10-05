import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import time


beging_prg_time = time.time()

# load the dataset one for each year to make work the cach
def load_data(x):
    if x==2020 :
        df = load_data_2020("sample_2020.csv")       
        df = cleanning_2020(df)
        return df
    if x==2019 :
        df = load_data_2019("sample_2019.csv")
        df = cleanning_2019(df)
        return df
    
@st.experimental_memo
def load_data_2019(path):
    df = pd.read_csv (path, sep=",", low_memory=False, nrows=300000)
    return df

@st.experimental_memo
def load_data_2020(path):
    df = pd.read_csv (path, sep=",", low_memory=False, nrows=300000)
    return df

@st.experimental_memo
def load_data_2020(path):
    df = pd.read_csv (path, sep=",", low_memory=False, nrows=100000)
    return df

# clean the dataset one for each year to make work the cach
@st.experimental_memo
def cleanning_2019(df):
    df.dropna(axis=1, how="all", inplace = True)
    df.dropna(subset=['longitude','latitude'], axis = 0, inplace = True)
    df["price/surface"]=df["valeur_fonciere"]/df["surface_reelle_bati"]
    df.drop_duplicates(subset='id_mutation', inplace = True, keep='last')
    df.drop(["numero_disposition","numero_volume","lot1_numero","lot1_surface_carrez","lot2_numero","lot2_surface_carrez","lot3_numero","lot3_surface_carrez","lot4_numero","lot4_surface_carrez","lot5_numero","lot5_surface_carrez","nombre_lots","code_nature_culture_speciale","nature_culture_speciale","code_nature_culture","nature_culture"], axis = 1, inplace = True)
    return df

@st.experimental_memo
def cleanning_2020(df):
    df.dropna(axis=1, how="all", inplace = True)
    df.dropna(subset=['longitude','latitude'], axis = 0, inplace = True)
    df["price/surface"]=df["valeur_fonciere"]/df["surface_reelle_bati"]
    df.drop_duplicates(subset='id_mutation', inplace = True, keep='last')
    df.drop(["numero_disposition","numero_volume","lot1_numero","lot1_surface_carrez","lot2_numero","lot2_surface_carrez","lot3_numero","lot3_surface_carrez","lot4_numero","lot4_surface_carrez","lot5_numero","lot5_surface_carrez","code_nature_culture_speciale","nombre_lots","nature_culture_speciale","code_nature_culture","nature_culture"], axis = 1, inplace = True)
    return df

# altair histogram
@st.experimental_memo
def histo_alt(df) : 
    x = alt.Chart(df).mark_bar().encode(
        alt.X("date_mutation", title="Date"),
        alt.Y("mean(price/surface)", title="surface"),
    ).properties(
    title="Surface by date current the year"
    )
    return x

# altair line chart
@st.experimental_memo
def line_alt(df) : 
    x = alt.Chart(df).mark_line().encode(
        alt.X("date_mutation", title="Date"),
        alt.Y("mean(price/surface)", title="surface"),
    ).properties(
    title="Surface by date current the year"
    )
    return x

# altair scatter chart
@st.experimental_memo
def scatter_alt(df) : 
    x = alt.Chart(df).mark_circle(size = 60).encode(
        alt.X("date_mutation", title="Date"),
        alt.Y("mean(price/surface)", title="surface"),
    ).properties(
    title="Surface by date current the year"
    )
    return x

@st.experimental_memo
def scatter_alt_room(df) : 
    x = alt.Chart(df).mark_circle(size = 60).encode(
        alt.X("valeur_fonciere", title="Price of logement"),
        alt.Y("nombre_pieces_principales", title="Nb romm"),
    ).properties(


    title="Price by number of room"
    )
    return x

# pyplot subplot
@st.experimental_memo
def plot_line_pyplo(df) : 
    df2 = df.groupby(["date_mutation"]).mean()
    fig, ax = plt.subplots(figsize=(50, 10))
    ax.plot(df2["price/surface"])
    ax.set_xlabel('price/surface')
    ax.margins(0, 0)    
    ax.set_title("The evolution of the surface price current the year")   
    ax.tick_params(axis ='x', rotation = 45)
    return fig

# streamlit line graph
@st.experimental_memo(suppress_st_warning=True)
def plot_line(df1, df2):
    chart_data = pd.DataFrame({'2019' : df1['valeur_fonciere'],
    '2020' : df2['valeur_fonciere']})
    return chart_data

# type local selection
@st.experimental_memo
def type_local_split(df,le_type_local) :
    if le_type_local=="all":
        return df
    else :
        return df[df["type_local"]==le_type_local]

# montant mask
@st.experimental_memo
def mask(df,montant) :
    if montant=="all":
        return df
    else :
        return df[df["valeur_fonciere"]<montant]

# code departement mask
@st.experimental_memo
def dep_selector(df,code_dep) :
    if code_dep=="all":
        return df
    else :
        return df[df["code_departement"]==code_dep]


st.title("Valeur fonciere dataset")

st.write("This dashboard have for objective to show the evolution of price by m² in France between 2019 and 2020.")
st.write("You can filter by departement and valeur fonciere to show more revelent data")

df_2019=load_data(2019)
df_2020=load_data(2020)

# apply the masks and filters
code_dep = ["all",'01', '02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','2A','2B','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','89','90','91','92','93','94','95','971','972','973','974','975','976']

choice_dep = st.selectbox("Departement", code_dep)

st.write("You selected {}".format(choice_dep))

df_2019_dep= dep_selector(df_2019,choice_dep)
df_2020_dep = dep_selector(df_2020,choice_dep)


choice_loc = st.select_slider(
     'Select a type of location',
     options=["all","Appartement","Maison"])

df_2019_dep_type_loc = type_local_split(df_2019_dep,choice_loc)
df_2020_dep_type_loc = type_local_split(df_2020_dep,choice_loc)


masklist = [100000,500000, 1000000, 2000000,"all"]

choice_mask = st.selectbox("Maske", masklist)

st.write("You selected {}".format(choice_mask))

df_2019_dep_type_loc_mak = mask(df_2019_dep_type_loc,choice_mask)
df_2020_dep_type_loc_mak = mask(df_2020_dep_type_loc,choice_mask)


# select the graph wanted
check_graph = ["Show valeur fonciere by id for 2019 and 2020", "Show evolution of price/surface over the year 2019 and 2020", "Valeur fonciere depending of room number" ]

choice_graphe = st.selectbox("Graph selected", check_graph)

st.write("You selected {}".format(choice_graphe))


if choice_graphe=="Show valeur fonciere by id for 2019 and 2020" :
    plt_are1 = plot_line(df_2019_dep_type_loc_mak, df_2020_dep_type_loc_mak)
    st.area_chart(plt_are1)


elif choice_graphe=="Valeur fonciere depending of room number" :
    st.altair_chart(scatter_alt_room(df_2019_dep_type_loc_mak))
    st.altair_chart(scatter_alt_room(df_2020_dep_type_loc_mak))
else :

    status = st.radio ("Show graphe with pyplot or altair histogramme or altair scatter or altair line show days with out sale ?", ("altair_histo","altair_line","altair_scatter","pyplot"))
    if status == 'altair_histo':
        st.altair_chart(histo_alt(df_2019_dep_type_loc_mak)) 
        st.altair_chart(histo_alt(df_2020_dep_type_loc_mak)) 

    if status == 'altair_line': 
        st.altair_chart(line_alt(df_2019_dep_type_loc_mak))
        st.altair_chart(line_alt(df_2020_dep_type_loc_mak))

    if status == 'altair_scatter':
        st.altair_chart(scatter_alt(df_2019_dep_type_loc_mak))
        st.altair_chart(scatter_alt(df_2020_dep_type_loc_mak))
 
    if  status =="pyplot" :
        st.pyplot(plot_line_pyplo(df_2019_dep_type_loc_mak))   
        st.pyplot(plot_line_pyplo(df_2020_dep_type_loc_mak))   


if st.checkbox ("Show/Hide map"):
    st.write("2019 and 2020 map for your selection")
    st.map(df_2019_dep_type_loc_mak)
    st.map(df_2020_dep_type_loc_mak)

# execution time
enfing_prg_time = time.time()

if not st.checkbox ("Hide/Show timestamp"):
	st.write("timestamp :", enfing_prg_time-beging_prg_time)


