
This python program takes in a file containing stirngs from 3 languages: Tamil, Malaysian and Indonesian. It then builds a language model for each language based on 4-grams.
We use NLTK to build the 4-grams.

To build and test the language models:
``` {.}
$ python3 build_test_LM.py -b input.train.txt -t input.test.txt -o input.predict.txt
```
Then, to verify the accuracy of the predictions:
``` {.}
$ python3 eval.py input.predict.txt input.correct.txt
```
_This program was completed in the context of CS3245 - Information Retrieval_
