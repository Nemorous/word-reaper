**Word Reaper** 🧙🔪

⚠️ **NOTICE: This project is in early development and not yet ready for production use. Features may change, break, or be incomplete. Use at your own risk.**

Extract & Forge Wordlists for Password Cracking.

Word Reaper is a flexible Python-based wordlist generation and manipulation utility. Designed with cybersecurity and red teaming in mind, it allows scraping, merging, mutation, and combining of words for password cracking tools.

**Features**

--method html/github/file :: Scrape HTML, GitHub repos, or local files

--ascii-art :: Displays a Reaper ASCII art banner

--mentalize :: Mutate wordlists like Mentalist tool

--merge :: Merge multiple wordlists into one

--combinator :: Hashcat-style combinator mode (word1 + word2)

**Installation**

git clone https://github.com/Nemorous/word-reaper.git
cd word-reaper
pip install -r requirements.txt

**Usage Examples**

🔗 Scraping:

# HTML scraping
python3 word_reaper.py --method html --url https://example.com --tag p --class content

# GitHub scraping
python3 word_reaper.py --method github --url https://github.com/user/repo

# Local file loading
python3 word_reaper.py --method file --input wordlist.txt

🔪 ASCII Art:

python3 word_reaper.py --ascii-art

🧠 Mentalist-style Wordlist Mutations:

python3 word_reaper.py --mentalize --input base.txt --output mutated.txt \
  --leet --toggle --underscores --spaces

✨ Merge Mode:

python3 word_reaper.py --merge rockyou.txt custom.txt leaked.txt --output merged.txt

🤾 Combinator Mode:

python3 word_reaper.py --combinator adjectives.txt nouns.txt --output combos.txt

Mutation Logic (Mentalist Mode)

Leetspeak: a → @, e → 3, i → 1, etc

Case Toggling: word → Word, wORd, etc

Underscores / Spaces: my_password, my password

Pattern Appending: ?a, ?s, ?d tokens left/right

**Requirements**

colorama
beautifulsoup4
requests

Install via pip install -r requirements.txt

Credits

**Created by d4rkfl4m3z**

Inspired by Mentalist, Hashcat, CeWL, and other tools

License

MIT

Happy Reaping ⚰️ 🪩
