import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


## create requirements.txt
create=True
if create:
    text_file = open("requirements.txt", "w")
    text_file.write('\n'.join(f'{m.__name__} {m.__version__}' for m in globals().values() if getattr(m, '__version__', None)))
    text_file.close()


sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .4, label, fontweight="bold", color='black',
            ha="left", va="center", transform=ax.transAxes)

df = pd.read_csv('data/nsi.csv')
df=df.set_index("date")
vars = ["st", "wl", "ml", "gm"]
labels = ["Stress", "Workload", "Motivation", "Mood"]


mainvar = "Stress"
v = vars[labels.index(mainvar)]

tdf = df.filter(regex=v+'_\d') # I love regex
tdf["date"] = tdf.index
tdf = pd.wide_to_long(tdf, stubnames=v+"_", i="date", j="score").reset_index().rename(columns={v+"_": v}).dropna()
tdf = tdf.loc[tdf.index.repeat(tdf[v])].reset_index()
tdf["date"] = pd.to_datetime(tdf["date"], format='%d/%m/%Y')
tdf["date"] = tdf["date"].dt.strftime('%Y-%m-%d')
tdf = tdf.sort_values(by='date',ascending=False)


# Initialize the FacetGrid object
pal = sns.cubehelix_palette(6, rot=-.25, light=.7)
g = sns.FacetGrid(tdf, row="date", hue="date", aspect=4, height=1.8, palette=pal)
g.map(sns.kdeplot, "score",
  bw_adjust=.5, clip_on=False,
  fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "score", clip_on=False, color="k", lw=2, bw_adjust=.5)
g.map(plt.axhline, y=0, lw=2, clip_on=False)
g.map(label, "score")
g.fig.subplots_adjust(hspace=-.35)
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)


st.sidebar.markdown('## Side menu')
mainvar = st.sidebar.selectbox(
    'Which variable would you like to see',
    ('Stress', 'Workload', 'Motivation', 'Mood')
)

st.title("Neurocode mental health index: "+mainvar)
st.pyplot(g)
