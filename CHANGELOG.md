# Changelog

## [1.0.1] - 2025-04-10
### Fixed
- Added support for Gist raw URLs (`gist.githubusercontent.com`) in GitHub scraper.
- Minor improvements to `scrape()` error messaging.
- Changed the example usage in the help menu to be more accurate
- Added missing dependencies (requests, beautifulsoup4) to install_requires in setup.py
- Restructured GitHub repo to enable full functionality as an installable Python package
- Added setup.py and __init__.py files to appropriate directories to support packaging and module imports
- Added installation instructions to README.md for local and PyPI usage
- Updated usage examples in README.md to reflect correct CLI syntax
- Provided new banner image in README.md with updated usage examples
- Changed version number to 1.0.1 where appropriate

## [1.0.0] - 2025-04-10
### Added
- Initial release of Word Reaper with HTML, GitHub, and Local file scraping
- Wordlist mutation features (leetspeak, case toggles, underscores, spaces, hyphens)
- HTML tag-based scraping with class and ID filtering
- GitHub raw wordlist pulling
- Hashcat-style permutation features (?a ?d ?s ?l ?u)
- Merge unlimited wordlists & sort/clean them on the fly
- Hashcat-style combinator mode to combine words
- Synchronize mode (prepend and append permutation chars at the same time)
- Hashcat-style increment mode
- ASCII art mode

