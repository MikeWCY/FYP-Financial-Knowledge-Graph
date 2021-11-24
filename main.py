from question import Question
import streamlit as st
import codecs
import json


class Page():
    def __init__(self):
        func_list = ["Conditional Questioning", "Complex Question"]
        function = st.sidebar.selectbox("", func_list)
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
        st.header("Conditional Questioning")
        st.markdown("##### This part supports the user to ask a simple question or a combinaiton of simple questions")
        num = st.number_input("Select the number of conditions for your question", value=1, step=1, format="%d")
        sq_ls = [""]*num
        for i in range(num):
            sq_ls[i] = st.text_input("Condition " + str(i + 1), key=i)
        choose_ls = ['name', 'type', 'CEO']
        selection = st.selectbox("Select the answer type you want", choose_ls)
        if st.button("Confirm all the conditions"):
            self.qa.sent = sq_ls[0]
            run_ls = self.qa.run_simple()
            entity = self.qa.entity
            for i in range(1, num):
                self.qa.sent = sq_ls[i]
                result = self.qa.run_simple()
                new = []
                for j in result:
                    if j in run_ls:
                        new.append(j)
                run_ls = new
            if selection == 'name':
                result_ls = run_ls
            elif selection == 'type':
                result_ls = []
                self.qa.sent = "what is the type of " + run_ls[0]
                result_ls.append(self.qa.run_simple()[0])
                for r in run_ls[1:]:
                    q = sq_ls[-1] + r
                    self.qa.sent = q
                    result = self.qa.run_simple()[0]
                    if result not in result_ls:
                        result_ls.append(result)
            elif selection == "CEO":
                result_ls = []
                self.qa.sent = "what is the CEO of " + run_ls[0]
                result_ls.append(self.qa.run_simple())
                for r in run_ls[1:]:
                    q = sq_ls[-1] + r
                    self.qa.sent = q
                    result = self.qa.run_simple()
                    if result not in result_ls:
                        result_ls.append(result)
            st.write(result_ls)
            st.components.v1.html(self.print_html(entity, result_ls), height = 2000, width=2500)

    def complex_page(self):
        st.header("Complex Question")
        st.markdown("##### This part supports the user to ask a complex question")
        cq = st.text_area("Please input your complex question")


if __name__ == "__main__":
    Page()
