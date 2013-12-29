yandex-translate
================

A thin Python wrapper around the Yandex Translation API.

## Requirements

* Python 2.6+ (for `multiprocessing` module)
* requests (can be found in the accompanying `requirements.text`)

## Usage
```python
import yandex
t = yandex.Translator(api_key='TEST', from_lang='en', to_lang='de')
t.strings.append('My name is Joe.')
t.translate()
print t.translated # Shows returned strings
translation_dict = t.make_dict() # For easier use later on
```