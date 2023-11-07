import argparse
from CharaCraft.generate import prompt
from CharaCraft.extract import dialogues, keywords
from CharaCraft.animate import webui
from CharaCraft.spider import run


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
    # extract
    # animate
    parser.add_argument('--me', type=str, default='traveler',
                        help='Name of you. Defaults to traveler.')

    parser.add_argument('--first_response', type=str, default='Nice to meet you.',
                        help='First response of you. Defaults to Nice to meet you.')

    parser.add_argument('--prompt', type=str, default='default',
                        help='Prompt file name. Defaults to prompt.')
    # animate

    args = parser.parse_args()

    if args.module == 'generate':
        if args.function == 'prompt':
            if not args.name:
                print('Name of target character is required.')
                return
            prompt.main(args)
        else:
            print("Invalid function. Choose from 'prompt'. ")

    elif args.module == 'extract':
        if args.function == 'dialogues':
            if not args.name:
                print('Name of target character is required.')
                return
            dialogues.main(args)
        elif args.function == 'keywords':
            if not args.name or not args.keywords:
                print('Name of target character and keywords are required.')
                return
            keywords.main(args)
        else:
            print("Invalid function. Choose from 'dialogues', 'keywords'. ")

    elif args.module == 'animate':
        if args.function == 'webui':
            if not args.name:
                print('Name of target character is required.')
                return
            webui.main(args)
        else:
            print("Invalid function. Choose from 'webui'. ")

    elif args.module == 'spider':
        if args.function == 'run':
            # examine required arguments
            if not args.urls or not args.depths:
                print('At least one URL and one depth are required.')
                return
            run.main(args)
        else:
            print("Invalid function. Choose from 'run'. ")
    else:
        print("Invalid module. Choose from 'generate', 'extract', 'animate'.")


if __name__ == "__main__":
    main()
