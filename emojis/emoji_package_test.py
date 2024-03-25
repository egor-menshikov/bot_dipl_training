import emoji

"""
Библиотека преобразует эмодзи из их текстового названия в иконки при помощи метода emojize(). Может находить их прямо в 
строке текста, остальной текст трогать не будет. Возвращает str.
"""
print(emoji.emojize(':penguin:'))
print(emoji.emojize('Это пингвинчик :penguin:') + '\n')

"""
Также можно сделать обратное - вывести текстовый код по эмодзи методом demojize().
"""
print(emoji.demojize('Это 🐈') + '\n')

"""
По умолчанию для кодов выбран английский язык, другой нам не понадобится. Есть также упрощенный 'язык', alias.
"""
print(emoji.emojize('Python is :thumbs_up:'))
print(emoji.emojize('Python is :thumbsup:', language='alias') + '\n')

text = emoji.emojize('This is a :cat:')
print(type(text))
print(text)
