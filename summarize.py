# coding=utf-8
import json 
import heapq
from langdetect import detect

class Summarize:
    def __init__(self):
        f = open("stopwords-all.json", "r",encoding='utf-8')
        self.stop_words = json.loads(f.read())
        f.close()

    def get_summary(self, text):
        source_language = detect(text).lower()
        word_frequency = self.__get_max_frequencies(text, source_language)
        terminating_char = self.__get_terminating_character(source_language)
        sentence_scores = self.__get_sentence_score(word_frequency, text, terminating_char)

        summary = self.__get_top_sentences(sentence_scores, terminating_char)
        result = {"text": summary}
        
        return json.dumps(result,ensure_ascii=False, separators=(',', ': ')) 

    def __get_max_frequencies(self, text, source_language):
        if source_language in self.stop_words:
            stopwords = self.stop_words[source_language]
            word_frequencies = {}
            for word in text.split():
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
        else:
            word_frequencies = {}
            for word in text.split():
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            
        return word_frequencies

    def __get_sentence_score(self, word_frequencies, text, terminating_char):
        sentence_scores = {}
        sentence_list = text.split(terminating_char)
    
        for sent in sentence_list:
            for word in text.split():
                if word in word_frequencies:
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores:
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        return sentence_scores
    
    def __get_top_sentences(self, sentence_scores, terminating_char):
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
        summary = terminating_char.join(summary_sentences)
        return summary
    
    def __get_terminating_character(self, source_language):
        if source_language == "hi":
            return "।"
        if source_language in ["ja","zh-cn" ]:
            return "。"
        return "."


if __name__ == "__main__":
    #print(detect("我是阿什溫。你是做什麼的"))
    summary = Summarize()
    
    text = """सामान्य रूप से देखें, तो मानव या तो नकल करता है या नकारता है। कभी-कभी नगण्य को ही नहीं, बल्कि बहुत से अदृश्य खजाने को भी। हमारे पास बहुत कम लेखक हैं, जिन्हें मुश्किल से फंटास्टिक लुगदी लेखन में सिद्धहस्त कहा जा सकता है। शायद एक भी नहीं, क्योंकि कुछ अन्य कारणों के साथ ही आर्थिक रूप से कमजोर प्रगतिशील देश इसे उरभने की इजाजत नहीं देते। प्रगतिशील देश केवल महान साहित्य के काम को ही इजाजत देते हैं। छोटे काम इस एकरस और प्रलयकारी दृश्य में एक फालतू किस्म का ऐश्वर्य हैं। और यह इस बात की ओर बिल्कुल इंगित नहीं करता कि हमारा साहित्य महान कामों से भरा पड़ा है, बल्कि इसके बरअक्स लेखक इन अपेक्षाओं से मुलाकात करना चाहता है, फिर यथार्थ वही सत्य जो इसे खड़ा करता है और अंततः वही इसका अंतिम प्रारूप बनाने में समर्थ होता है। जहां तक मेरे लेखन का प्रश्न है, मुझे नहीं पता मुझे क्या कहना चाहिए, मैं सोचता हूं कि यह यथार्थवादी है। मैं फंटास्टिक लेखक कहा जाना पसंद करूंगा। देखा जाए, तो प्रश्न यथार्थवादी और फंटास्टिक लुगदी के बीच का भी नहीं है, यह भाषा और उसकी संरचना का है। मैं जोखिम उठाता हूं बहुत ही बारीक से बारीक विवरण को अतिवादी दृष्टिकोण से रचकर (जो मुझे लगता है कि मेरे कहन में निहित होता है)। जब मैं लिखता हूं, तब जो चीज मुझमें दिलचस्पी जगाती है, वह लेखन ही होता है— उसकी शैली, लय और कथ्य। सभी तरह का साहित्य एक खास दृष्टिकोण से राजनीति ही है, मेरा मतलब है कि प्रथम दृष्टि में इसकी प्रतिच्छाया राजनीति पर दिखाई देती है, और दूसरी बात यह एक राजनीतिक कार्यक्रम भी होता है। लेखन एक ऐसी क्रिया है, जो मेरे खुशनुमा पलों को साझा करती है, लेकिन मैं और चीजों के बारे में भी जानता हूं, जो इससे भी ज्यादा आनंद देने वाली हैं।"""
    #print(text)
    print("-----------------------------------------------------------------------------------------------------------")
    print(summary.get_summary(text))