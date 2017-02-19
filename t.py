import CSVExecutor
import WordExecutor
import emoji

word = "ฉันอยากไปไปโรงเรียน😮,😲,😳,😵,🙀😮,😲,😳,😵,🙀"
keyword = WordExecutor.createNgram(word, 1) +  WordExecutor.createNgram(word, 2)
keyword = WordExecutor.add_emoji_keyword(keyword)
freq = WordExecutor.frequency_occur_in_keyword(word, sorted(keyword))
t = []
for i in sorted(freq.keys()):
    if freq.get(i) != 0:
        t.append({i: freq.get(i)})
print(t)
