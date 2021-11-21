from graph import Connect
import textdistance
import pandas as pd
from operator import length_hint


class Question():
    def __init__(self, sent):
        self.sent = sent
        self.process_question()
        self.df = pd.read_csv("template.csv")
        self.connect = Connect()
        self.data = {"<Institution>": [], "<Service>": [], "<string>": []}
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
    
    def process_question(self):
        self.sent = self.sent.replace("that", "")
        words = self.sent.split(" ")
        if "which" in self.sent and words[0] != "which":
            self.sent = self.sent[0] + self.sent[1:].replace("which", "")
        if "who" in self.sent and words[0] != "who":
            self.sent = self.sent[0] + self.sent[1:].replace("who", "")
        
    @staticmethod
    def get_entityType(data, sent):
        entity = None
        entityType = None
        pattern = None
        recognized_entities = []
        recognized_type = None
        for k in data.keys():
            for c in data[k]:
                if c in sent:
                    recognized_entities.append(c)
                    recognized_type = k
                    pattern = sent
                    #pattern = sent.replace(c, k)
                    entity = c
                    entityType = k
                    break
        if len(recognized_entities) != 0:
            max_len = 0
            max_entity = ""
            for e in recognized_entities:
                length = len(e)
                if length >= max_len:
                    max_len = length
                    max_entity = e
        if entity != None:
            for k in data.keys():
                if k in sent:
                    pattern = sent.replace(k, "")
                    sent = sent.replace(k, "")
            pattern = pattern.replace(max_entity, recognized_type)
        else:
            for k in data.keys():
                if k in sent:
                    entity = k
                    entityType = k
                    pattern = sent
        
        #print([sent, entity, entityType, pattern])
        return [entity, entityType, sent, pattern]

    @staticmethod
    def find_all_entities(data, sent):
        entity_ls = []
        entityType_ls = []
        start_pos = []
        end_pos = []
        pattern = sent
        words = sent.split(" ")
        for k in data.keys():
            if k in sent:
                entity_ls.append(k)
                entityType_ls.append(k)
            for c in data[k]:
                if c in sent:
                    entity_ls.append(c)
                    entityType_ls.append(k)
                    pattern = sent.replace(c, k)
        while len(start_pos) < len(entity_ls):
            for i in range(len(words)):
                for j in range(i + 1, len(words) + 1):
                    blank = " "
                    sub = blank.join(words[i:j])
                    if sub in entity_ls:
                        start_pos.append(i)
                        end_pos.append(j)
        return [entity_ls, entityType_ls, pattern, start_pos, end_pos]

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
            #distance2 = textdistance.damerau_levenshtein(pattern, pattern_ls[j].replace("what ", ""))
            if distance < min_distance:
                min_distance = distance
                min_index = j
            #print(pattern_ls[j], distance)
        if min_distance == 1000 and min_index == -1:
            return [None, None]
        elif min_distance < 8:
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
        blank = " "
        for i in range(len(word_ls)):
            for j in range(i + 1, len(word_ls) + 1):
                sub = word_ls[i:j]
                subq = blank.join(sub)
                [entity, entityType, subq, pattern] = self.get_entityType(self.data, subq)
                if entity ==  None or entityType == None or pattern == None:
                    continue
                [query, answerType] = self.match_pattern(self.df, entity, entityType, pattern)
                if query == None or answerType == None:
                    continue
                newsent = sent.replace(subq, answerType)
                newsent_ls = newsent.split(" ")
                '''
                print(subq, "----", newsent)
                [entity, entityType, s, pattern] = self.get_entityType(self.data, newsent)
                #print(newsent, entity)
                #print(self.match_pattern(self.df, entity, entityType, pattern)[0])
                print("-"*40)
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
        result = self.connect.run()
        return result

    def clear_result(self, result):
        ls = []
        try:
            for r in result:
                ls.append(r['o']['name'])
        except KeyError:
            ls.append(result)
        return ls

    def run_simple(self):
        [self.entity, self.entityType, s, self.pattern] = self.get_entityType(self.data, self.sent)      
        [self.query, self.answerType] = self.match_pattern(self.df, self.entity, self.entityType, self.pattern)
        #print(self.pattern)
        self.result = self.run_query(self.query)
        if self.result == None:
            return "no result"
        else:
            return self.result
        
    def run_complex(self):
        self.decomposed_qs = []
        self.query_ls = []
        self.question_decomposition(self.sent, 0)
        print("D:", self.decomposed_qs)
        self.result = self.run_decomposed(self.query_ls, self.answerType_ls)
        return self.result

    def run_decomposed(self, query_ls, answerType_ls):
        result = []
        for i in range(len(query_ls) - 1, -1, -1):
            r = self.run_query(query_ls[i])
            r = self.clear_result(r)
            if r == None:
                return "no result"
            result.append(r)
            if i > 0:
                for j in r:
                    self.query_ls[i - 1] = query_ls[i - 1].replace(answerType_ls[i], j)
        if len(result) == 0:
            return "no result"
        else:
            return result[-1]





    def type_question_decomposition(self, sent, depth):
        if depth > 2:
            return [None, None]
        [entity_ls, entityType_ls, pattern, start_pos, end_pos] = self.find_all_entities(self.data, sent)
        words = sent.split(" ")
        blank = " "
        for i in range(end_pos[-1]):
            for index in range(len(entity_ls)):
                if start_pos[index] >= i:
                    break
            for k in range(end_pos[index], len(words)):
                sub = blank.join(words[i:k + 1])
                pattern = sub.replace(entity_ls[index], entityType_ls[index])
                [query, answerType] = self.match_pattern(self.df, entity_ls[index], entityType_ls[index], pattern)
                if [query, answerType] == [None,  None]:
                    continue
                newsent = sent.replace(sub, answerType)
                newsent_ls = newsent.split(" ")
                if len(newsent_ls) == 1 or self.type_question_decomposition(newsent, depth + 1) != [None, None]:
                    self.decomposed_qs.append(sub)
                    self.query_ls.append(query)
                    self.answerType_ls.append(answerType)
                    return [self.decomposed_qs, self.query_ls]
        return [None, None]

    def run_complex_type(self):
        self.decomposed_qs = []
        self.query_ls = []
        self.type_question_decomposition(self.sent, 0)
        result = []
        print("D:", self.decomposed_qs)
        for i in range(len(self.decomposed_qs) - 1, -1, -1):
            r = self.run_query(self.query_ls[i])
            if r == None:
                return "no result"
            result.append(r)
            if i > 0 :
                for j in r:
                    self.query_ls[i - 1] = self.query_ls[i - 1].replace(self.answerType_ls[i], j)
        if len(result) == 0:
            return "no result"
        else:
            return result[-1]
