import argparse
from CharaCraft import generate, extract, animate, spider
from chara_craft import CharaCraft


def main():
    parser = argparse.ArgumentParser(description="Run submodules in my_project.")

    parser.add_argument('module', choices=['generate', 'extract', 'animate', 'spider'], help='The module to run')

    parser.add_argument('function', choices=['prompt', 'dialogues', 'keywords', 'webui', 'run'],
                        help='The function to run')

    parser.add_argument('--name', type=str,
                        help='Name of target character. Defaults to traveler.')
    # spider
    parser.add_argument('--urls', nargs='+',
                        help='Target URLs to scrape. At least one URL is required.')

    parser.add_argument('--depths', nargs='+', type=int,
                        help='Depth limit for each corresponding URL. Must match the number of URLs provided.')

    parser.add_argument('--dynamic', action='store_true',
                        help='Whether to use dynamic scraping. Defaults to False.')
    # spider
    # extract
    parser.add_argument('--files', nargs='+',
                        help='File names of target character in data folder. If not provided, all files will be used.')

    parser.add_argument('--keywords', nargs='+', type=str,
                        help='Name of target character. You should only provide one character once.')

    parser.add_argument('--num_context', type=int, default=2,
                        help='Number of context lines to include before and after the target character lines. Defaults to 2.')

    parser.add_argument('--dialogues', action='store_true',
                        help='Whether it is a dialogue. Defaults to False.')
    parser.add_argument('--pair', action='store_true',
                        help='Whether to extract dialogues between two characters. Defaults to False.')
    # extract
    # animate
    parser.add_argument('--me', type=str, default='traveler',
                        help='Name of you. Defaults to traveler.')

    parser.add_argument('--first_response', type=str, default='Nice to meet you.',
                        help='First response of you. Defaults to Nice to meet you.')

    parser.add_argument('--prompt', type=str, default='default',
                        help='Prompt file name. Defaults to prompt.')
    # animate
    # generate
    parser.add_argument('--attributes', nargs='+', type=str,
                        help='Attributes of target character. You should only provide one attribute once.')
    # generate
    args = parser.parse_args()

    characraft = CharaCraft()
    characraft.update(**vars(args))
    characraft.run()


if __name__ == "__main__":
    main()
