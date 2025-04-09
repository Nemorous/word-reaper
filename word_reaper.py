import argparse
import sys
from scraper import html_scraper, github_scraper, file_loader
from utils import cleaner, formatter, permutator
import utils.ascii_art as ascii_art
from utils import ascii as banner


def main():
    # Pre-check for banner-only mode
    if '--ascii-art' in sys.argv:
        ascii_art.print_scythe()
        sys.exit()

    banner.print_banner()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Word Reaper - Extract & Forge Wordlists for Password Cracking",
        epilog="""
Example usage:
  python3 word_reaper.py --method html --url https://example.com
  python3 word_reaper.py --mentalize --input input.txt --output out.txt --leet --toggle
  python3 word_reaper.py --merge file1.txt file2.txt -o merged.txt
  python3 word_reaper.py --combinator file1.txt file2.txt -o combos.txt
        """
    )

    parser.add_argument('--method', metavar='METHOD', required=False, help='Scraping method: html, github, file')
    parser.add_argument('--url', help='Target URL to scrape (for html and github methods)')
    parser.add_argument('--input', help='Local file to load wordlist from (for file or --mentalize)')
    parser.add_argument('--tag', help='HTML tag to extract (only for HTML method)')
    parser.add_argument('--class', dest='class_name', help='HTML class (optional)')
    parser.add_argument('--id', help='HTML id (optional)')
    parser.add_argument('--output', '-o', default='wordlist.txt', help='Output file name')

    parser.add_argument('--ascii-art', action='store_true', help='Display the reaper ASCII art')

    parser.add_argument('--mentalize', action='store_true', help='Mutate words like Mentalist')
    parser.add_argument('--leet', action='store_true', help='Apply leetspeak')
    parser.add_argument('--toggle', action='store_true', help='Toggle casing (like hashcat)')
    parser.add_argument('--underscores', action='store_true', help='Insert underscores between words')
    parser.add_argument('--spaces', action='store_true', help='Insert spaces between words')
    parser.add_argument('--hyphens', action='store_true', help='Insert hyphens between words')

    parser.add_argument('--merge', nargs='+', help='Merge and deduplicate multiple wordlists')
    parser.add_argument('--combinator', nargs=2, metavar=('file1', 'file2'), help='Combine words from two files')

    args = parser.parse_args()

    if args.merge:
        merged = permutator.merge_files(args.merge)
        formatter.print_stats(merged)
        formatter.save_to_file(merged, args.output)
        print(f"\nWordlist saved to: {args.output}")
        return

    if args.combinator:
        words1 = open(args.combinator[0]).read().splitlines()
        words2 = open(args.combinator[1]).read().splitlines()
        combined = permutator.combinatorize(words1, words2)
        formatter.print_stats(combined)
        formatter.save_to_file(combined, args.output)
        print(f"\nWordlist saved to: {args.output}")
        return

    if args.mentalize:
        if not args.input:
            print("\nError: --input is required with --mentalize\n")
            sys.exit(1)
        base_words = file_loader.load(args.input)
        mutated_words = permutator.mentalize(
            base_words,
            leet=args.leet,
            toggle=args.toggle,
            underscores=args.underscores,
            spaces=args.spaces,
            hyphens=args.hyphens
        )
        formatter.print_stats(mutated_words)
        formatter.save_to_file(mutated_words, args.output)
        print(f"\nWordlist saved to: {args.output}")
        return

    if not args.method:
        print("\nError: --method is required unless using --ascii-art, --mentalize, --merge or --combinator\n")
        parser.print_help()
        sys.exit(1)

    raw_words = []

    if args.method == 'html':
        raw_words = html_scraper.scrape(args.url, args.tag, args.class_name, args.id)
    elif args.method == 'github':
        raw_words = github_scraper.scrape(args.url)
    elif args.method == 'file':
        if not args.input:
            print("\nError: --input is required when using --method file\n")
            sys.exit(1)
        raw_words = file_loader.load(args.input)
    else:
        sys.exit("Unsupported method.")

    cleaned_words = cleaner.clean_words(raw_words)
    formatter.print_stats(cleaned_words)
    formatter.save_to_file(cleaned_words, args.output)

    print(f"\nWordlist saved to: {args.output}")


if __name__ == '__main__':
    main()
