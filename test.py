from translate import Translator

translator= Translator(from_lang='uz', to_lang='ar')

# a = translator.translate('1 декабря прошлого года адвокаты иностранные и грузинские')
a = translator.translate('O‘tgan yilning 1 dekabrida advokatlar chet ellik va gruziyalik')

print(a)
