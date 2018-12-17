# hangulizer
Phoneme to Grapheme converter (P2G) between roman and hangul script for LING83600.  Takes a text containing romanization of Korean lemms and produces list of likely equivalents in Hangul script. 

To use:
  python3 hangulizer.py [--Syllable] source [output (hangul.txt by default)]
  
  Note: --Syllable flag increases range of outputs and increases accuracy at possible cost to run-time performance.

Required: 
- pynini package and associated dependencies (please see requirements at http://www.openfst.org/twiki/bin/view/GRM/Pynini
- jamotools package: pip install jamotools

Common Issues:
- Software assumes that provided forms are romanizations of Hangul graphemes.  As such, assumes syllable composition to be VALID PHONETIC APPROXIMATIONS OF KOREAN WORDS.  Usage of English exclusive phonemes (/f/, /v/, /z/) will likely result in runtime error.  

Thanks to:
-Wiktionary for Korean Lemmas and associated romanizations.
-Universal Dependencies Treebank for Training Data.
-Ngram Fst
