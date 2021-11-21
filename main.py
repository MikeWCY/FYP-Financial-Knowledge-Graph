from question import Question
import streamlit as st
import codecs
import json


class Page():
    def __init__(self):
        func_list = ["Simple Question", "Complex Question"]
        function = st.sidebar.selectbox("Ask a Question", func_list)
        self.qa = Question("")
        if function == func_list[0]:
            self.simple_page()
        else:
            self.complex_page()

    def clear_result(result):
        ls = []
        for r in result:
            ls.append(r['o']['name'])
        return ls

    def print_html(self, entity, result):
        f = codecs.open("demo.html", "r")
        html = f.read()
        en_ls = []
        en_ls.append(entity)
        html = html.replace("##node1##", json.dumps(en_ls)).replace("##node2##", json.dumps(result))
        return html

    def simple_page(self):
        st.header("This part supports the user to ask a simple question or a combinaiton of simple questions")
        num = st.number_input("Select the number of conditions for your question", value=1, step=1, format="%d")
        sq_ls = [""]*num
        for i in range(num):
            st.write("Question " + str(i + 1))
            sq_ls[i] = st.text_input("", key=i)
        if st.button("Confirm all the questions"):
            q_ls = []
            query_ls = []
            answerType_ls = []
            for i in range(num):
                self.qa.sent = sq_ls[i]
                self.qa.run_simple()
                q_ls.append(sq_ls[i])
                query_ls.append(self.qa.query)
                answerType_ls.append(self.qa.answerType)
            result = self.qa.run_decomposed(query_ls, answerType_ls)
            entity = self.qa.entity
            st.write(result)
            st.components.v1.html(self.print_html(entity, result), height = 2000, width=2500)

    def complex_page(self):
        st.header("This part supports the user to ask a complex question")
        cq = st.text_area("Please input your complex question")


if __name__ == "__main__":
    Page()
