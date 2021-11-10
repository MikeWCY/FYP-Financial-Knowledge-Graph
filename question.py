from graph import Connect
import textdistance
import pandas as pd


class Question():
    def __init__(self, sent):
        self.sent = sent
        self.df = pd.read_csv("template.csv")
        self.connect = Connect()
        self.data = {"<Institution>": [], "<Service>": []}
        self.data["<Institution>"] = self.connect.get_company_list()
        self.data["<Service>"] = self.connect.get_service_list()
        self.pattern = sent
        self.entity = ""
        self.entityType = ""
        self.candidate_entityType = []
        self.query = ""
        self.result = ""

        self.decomposed_qs = []
        self.query_ls = []
        self.answerType_ls = []
        
    @staticmethod
    def get_entityType(data, sent):
        entity = None
        entityType = None
        pattern = None
        for k in data.keys():
            if k in sent:
                entity = k
                entityType = k
                pattern = sent
                continue
            for c in data[k]:
                if c in sent:
                    pattern = sent.replace(c, k)
                    entity = c
                    entityType = k
                    break
                
        #print([sent, entity, entityType, pattern])
        return [entity, entityType, pattern]

    @staticmethod
    def match_pattern(df, entity, entityType, pattern):
        pattern_ls = []
        lquery_ls = []
        rquery_ls = []
        answerType_ls = []
        for i in range(len(df)):
            if df["entityType"][i] == entityType:
                pattern_ls.append(df["pattern"][i])
                lquery_ls.append(df["lquery"][i])
                rquery_ls.append(df["rquery"][i])
                answerType_ls.append(df["answerType"][i])
        min_distance = 1000
        min_index = -1
        for j in range(len(pattern_ls)):
            distance = textdistance.damerau_levenshtein(pattern, pattern_ls[j])
            if distance < min_distance:
                min_distance = distance
                min_index = j
            #print(pattern_ls[j], distance)
        if min_distance == 1000 and min_index == -1:
            return [None, None]
        elif min_distance < 10:
            matched_pattern = pattern_ls[min_index]
            query = lquery_ls[min_index] + entity + rquery_ls[min_index]
            answerType = answerType_ls[min_index]
            return [query, answerType]
        else:
            return [None, None]

    def question_decomposition(self, sent, depth):
        if depth > 2:
            return [None, None, None]
        word_ls = sent.split(" ")
        for i in range(len(word_ls)):
            for j in range(i + 1, len(word_ls) + 1):
                sub = word_ls[i:j]
                subq = word_ls[i]
                for k in range(1, j - i):
                    subq = subq + " " + sub[k]
                print(subq)
                [entity, entityType, pattern] = self.get_entityType(self.data, subq)
                if entity ==  None or entityType == None or pattern == None:
                    continue
                [query, answerType] = self.match_pattern(self.df, entity, entityType, pattern)
                if query == None or answerType == None:
                    continue
                newsent = sent.replace(subq, answerType)
                newsent_ls = newsent.split(" ")
                '''
                if "Bank of China (Hong Kong)" or "<Institution>" in subq:
                    print(newsent)
                    print(self.get_entityType(self.data, newsent))
                    print(self.match_pattern(self.df, "<Institution>", "<Institution>", newsent))
                    print(len(newsent_ls))
                    print("-" * 60)
                '''
                if len(newsent_ls) == 1 or self.question_decomposition(newsent, depth + 1) != [None, None, None]:
                    self.decomposed_qs.append(subq)
                    self.query_ls.append(query)
                    self.answerType_ls.append(answerType)
                    return [self.decomposed_qs, self.query_ls, self.answerType_ls]
        return [None, None, None]

    def run_query(self, query):
        # print(query)
        self.connect.query = query
        result = self.connect.run_query()
        return result

    def run_simple(self):
        [self.entity, self.entityType, self.pattern] = self.get_entityType(self.data, self.sent)      
        [self.query, answerType] = self.match_pattern(self.df, self.entity, self.entityType, self.pattern)
        self.result = self.run_query(self.query)
        return self.result

    def run_complex(self):
        self.question_decomposition(self.sent, 0)
        print("Decomposed:", self.decomposed_qs)
        print("query", self.query_ls)
        result = []
        for i in range(len(self.decomposed_qs) - 1, -1, -1):
            print(i, self.query_ls[i])
            r = self.run_query(self.query_ls[i])
            print(r)
            print("-"*40)
            result.append(r)
            if i > 0 :
                for j in r:
                    self.query_ls[i - 1] = self.query_ls[i - 1].replace(self.answerType_ls[i], j)
        if len(result) == 0:
            return "no result"
        else:
            return result[-1]
