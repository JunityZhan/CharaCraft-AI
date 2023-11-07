import argparse
import subprocess


def parse_arguments():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(description='Run a Scrapy spider.')
    parser.add_argument('--urls', nargs='+', required=True,
                        help='Target URLs to scrape. At least one URL is required.')
    parser.add_argument('--depths', nargs='+', type=int, required=True,
                        help='Depth limit for each corresponding URL. Must match the number of URLs provided.')
    parser.add_argument('--dynamic', action='store_true',
                        help='Whether to use dynamic scraping. Defaults to False.')

    args = parser.parse_args()

    if len(args.urls) != len(args.depths):
        raise ValueError('Number of URLs must match the number of depth limits provided.')

    return args


def main():
    """Main function to run the Scrapy spider with given arguments."""
    args = parse_arguments()

    for url, depth in zip(args.urls, args.depths):
        subprocess.run(['python', './spider/spider_helper.py', url, str(depth), '1' if args.dynamic else '0'])


if __name__ == '__main__':
    main()
