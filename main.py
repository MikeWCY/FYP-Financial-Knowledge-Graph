import streamlit as st
from py2neo import Graph


st.write("# Welcome to FiGo!")
graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
if graph:
    st.write("Connected")
else:
    st.write("Connection error")

class Question():
    def __init__(self):
        st.sidebar.markdown("# Question type")
        self.option = st.sidebar.selectbox("",["Prepared", "Natural Language"])

        c_sp = graph.run("MATCH (p: Person) RETURN p")
        l_sp = []
        while c_sp.forward():
            if c_sp.current[0]:
                l_sp.append(c_sp.current[0]["name"])
        self.l_sp = l_sp

        if self.option == "Prepared":
            self.queryPrepared()
        elif self.option == "Natural Language":
            self.queryNL()

    def collectQuestion(self):
        q = st.text_input("Please input your question here")
        if st.button("Confirm"):
            self.q = q
            self.runQuery()

    def queryPrepared(self):
        sp = st.selectbox("Person", self.l_sp)
        st.write("ACTED_IN")
        s = st.selectbox("", ["Movie"])
        if st.button("Confirm"):
            if sp != None:
                self.query = "MATCH (p: Person {name:'" + sp + "'})-[rel: ACTED_IN]-(m: Movie) RETURN m;"
                self.runMovieQuery()

    def queryNL(self):
        nl = st.text_input("")
        if st.button("Confirm"):
            if nl in self.l_sp:
                self.query = "MATCH (p: Person {name:'" + nl + "'})-[rel: ACTED_IN]-(m: Movie) RETURN m;"
                st.markdown("### " + nl + " acted in ")
                self.runMovieQuery()


    def runMovieQuery(self):
        c_result = graph.run(self.query)
        l_result = []
        while c_result.forward():
            if c_result.current[0]:
                l_result.append(c_result.current[0]["title"])
                st.markdown(c_result.current[0]["title"])
        if len(l_result) == 0:
            st.write("No result")



if __name__ == "__main__":
    Demo = Question()
