#!/usr/bin/env python3
"""Word-count a draft and check it against a limit parsed from the prompt text.

Usage: check_draft.py DRAFT.txt [--prompt PROMPT.txt]
Exit 0 if within limit (or no limit found), 1 if outside, 2 on usage error.
Recognises "150-200 word", "150 to 200 words", "at least 300 words", "no more than 500 words".
"""
import re, sys

def count_words(text):
    return len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text))

def parse_limit(prompt):
    m = re.search(r"(\d+)\s*(?:-|–|to)\s*(\d+)\s*[- ]?words?", prompt, re.I)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(?:at least|minimum of|min\.?)\s*(\d+)\s*words?", prompt, re.I)
    if m:
        return int(m.group(1)), None
    m = re.search(r"(?:no more than|maximum of|max\.?|up to|under)\s*(\d+)\s*words?", prompt, re.I)
    if m:
        return None, int(m.group(1))
    return None, None

def check(text, prompt=""):
    n = count_words(text)
    lo, hi = parse_limit(prompt)
    ok = (lo is None or n >= lo) and (hi is None or n <= hi)
    return n, lo, hi, ok

def main(argv):
    if not argv:
        print(__doc__); return 2
    text = open(argv[0], encoding="utf-8").read()
    prompt = open(argv[argv.index("--prompt") + 1], encoding="utf-8").read() if "--prompt" in argv else ""
    n, lo, hi, ok = check(text, prompt)
    print(f"words={n} limit={lo}-{hi} {'OK' if ok else 'OUT OF RANGE'}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
