import model
import CSVExecutor
import WordExecutor
import weka.core.jvm as jvm

keywords = CSVExecutor.read_csv('output/keyword.csv')

library = CSVExecutor.read_csv('./Dataset/ktest.csv')
freq = []
for li in library:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], keywords[0], 1)
    freq.append(li[0])

jvm.start()
# train_data = model.load_dataset("./output/output_5EMO_2.csv")
# clsf = model.naivebay_classifier(train_data)
# model.save_model(clsf, 'output/out.model')
clsf = model.read_model('output/out.model')
result = model.predict_for_result(clsf, freq[0])
print(str(result))
jvm.stop()
