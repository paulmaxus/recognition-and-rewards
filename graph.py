import pandas as pd

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config


def run():

    # load data
    df = pd.read_csv("recognition.csv")

    # create an empty graph
    c = Config(height=700, width=700, 
               directed=False, physics=True, hierarchical=False)

    nodes = []
    edges = []

    # create nodes from column Output with Domain as color, contains duplicates
    df_output = df[["Output","Domain"]].drop_duplicates()
    for i, row in df_output.iterrows():
        nodes.append(
            Node(
                id=row["Output"]+row["Domain"],
                label=row["Output"],
                size=20,
                color=row["Domain"],
            )
        )
    # create nodes from column Indicator, with color grey, contains duplicates
    indicators = df["Indicator"].drop_duplicates()
    # inside labels determine node size so pad to the largest 
    max_len = indicators.apply(len).max()
    max_loc = indicators.apply(len).idxmax()
    for i, indicator in enumerate(indicators):
        nodes.append(
            Node(
                id=indicator,
                label=f"{indicator:^{max_len+2 if i!=max_loc else max_len}}",
                #size=30,
                color="lightgrey",
                shape='circle',  # circle has inside label: 
                #font={"color": "white"},
            )
        )
    # create nodes from column Source, with color grey, contains duplicates
    #df_source = df[["Source"]].drop_duplicates().dropna()
    #for i, row in df_source.iterrows():
    #    nodes.append(
    #        Node(
    #            id=row["Source"],
    #            label=row["Source"],
    #            size=20,
    #            color="red",
    #        )
    #    )
    # create edges between Indicator and Output where column Metric is the edge label, edge width is column Impact
    # create edges between Output and Source
    for i, row in df.iterrows():
        edges.append(
            Edge(   
                source=row["Indicator"],
                target=row["Output"]+row["Domain"],
                label=row["Metric"],
                width=row["Impact"],
                font={"size": 13},
                
            )
        )
        #edges.append(
        #    Edge(
        #        source=row["Output"]+row["Domain"],
        #        target=row["Source"],
        #    )
        #)
    # show graph
    agraph(nodes=nodes, edges=edges, config=c)
    

st.set_page_config(page_title="R&R", page_icon="📈")

if __name__ == "__main__":
    run()
