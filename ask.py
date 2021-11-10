from question import Question

s1 = "what does Bank of China (Hong Kong) provide"
s2 = "what institution provides credit cards"
s3 = "what services does the parent company of Bank of China (Hong Kong) provide"
s4 = "what is the type of Bank of China (Hong Kong)"
s5 = "what is the type of the parent company of Bank of China (Hong Kong)"
q = Question(s3)
# run_simple() is used to process questions with one triple and run_complex() used to process questions with more than one triples
# the limit of run_complex() is 3
print(q.run_complex())
