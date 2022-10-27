import re
from collections import Counter
from pprint import pprint
import streamlit as st

#from functools import filter

def words(text): return re.findall(r'\w+', text.lower())
word_count = Counter(words(open('big.txt').read()))
N = sum(word_count.values())
def P(word): return word_count[word] / N # float

#Run the function:

print( list(map(lambda x: (x, P(x)), words('speling spelling speeling'))) )

letters    = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in word_count)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
 
print('speling -->', correction('speling'))
# speling spelling
    
# frame
st.title("Spellchecker Demo")
sentence1 = st.selectbox(
    'Choose a word or...',
    ("", "project", "ebook", "lamon", "blue", "pineapple", "fing")
)
sentence2 = st.text_input(
    'type your own!!!',
)
sidebar_checkbox = st.sidebar.checkbox(
    "Show original word"
)
if sidebar_checkbox: st.markdown("Original word:" + (sentence2 or sentence1))

spell_check_word = sentence2 or sentence1
if spell_check_word:
    if correction(spell_check_word) == spell_check_word:
        st.success(str(spell_check_word)+' is the correct spelling!')
    else:
        st.error('Correction: '+ str(correction(spell_check_word)))
    

