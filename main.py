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
        st.sidebar.markdown("Question type")
        self.collectQuestion()

    def collectQuestion(self):
        q = st.text_input("Please input your question here")
        if st.button("Confirm"):
            self.q = q
            self.runQuery()

    def runQuery(self):
        st.write(graph.run(self.q))


if __name__ == "__main__":
    Demo = Question()
