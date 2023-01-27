import csv
from datetime import date
from os import chdir, path, system

import moviepy.editor as mp
import pytube.exceptions
from art import tprint
from pytube import YouTube as YT
from pytube import Playlist
from termcolor import colored
from tqdm import tqdm


def donwload_audio_YT(link: str) -> None:

    if "playlist" in link:

        playlist = Playlist(link)

        if not path.exists(f"./{str(playlist.title)}"):
            system(f"mkdir '{str(playlist.title).replace('/','-')}'")
        chdir(str(playlist.title).replace('/', '-'))

        for link in playlist.video_urls:
            print(colored(f"\n\n{YT(link).title}\n", "blue"))
            YT(link).streams.get_highest_resolution().download()

        return None

    print(colored(f"\n\n{YT(link).title}\n", "blue"))
    YT(link).streams.get_by_itag("251").download()


def download_video_YT(link: str) -> None:

    if "playlist" in link:

        playlist = Playlist(link)

        if not path.exists(f"./{str(playlist.title)}"):
            system(f"mkdir '{str(playlist.title).replace('/','-')}'")
        chdir(str(playlist.title).replace('/', '-'))

        for link in playlist.video_urls:
            print(colored(f"\n\n{YT(link).title}\n", "blue"))
            YT(link).streams.get_highest_resolution().download()

        return None

    print(colored(f"\n\n{YT(link).title}\n", "blue"))
    YT(link).streams.get_highest_resolution().download()


def main():
    try:
        system('clear')
        tprint("Youtube scraper", "small")

        links = list()

        menu = int(input(
            "Choose which type of content you downloading.\n 1.Educational \n 2.Entertainment\n>> "
        ))

        match menu:
            case 1:

                with open("_yt_educational.csv") as csvfile:
                    for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
                        links.append(row[0])

                if not path.exists(f"./{date.today()}"):
                    system(f"mkdir {date.today()}")
                chdir(f"{date.today()}")

                if not path.exists("./Educational"):
                    system("mkdir Educational")
                chdir("Educational")

                print(colored("\n\tDonwloading start.\n", "green"))

                for i in tqdm(range(len(links))):
                    try:
                        download_video_YT(link=links[i])
                    except pytube.exceptions.RegexMatchError:
                        print(
                            (colored(
                                f"\n\n\tLink - {links[i]} is invalid\n", 'red'))
                        )

                        continue

                print(colored("\n\tDonwloading complete.\n", "green"))

            case 2:

                with open("_yt_entertainment.csv") as csvfile:
                    for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
                        links.append(row[0])

                if not path.exists(f"./{date.today()}"):
                    system(f"mkdir {date.today()}")
                chdir(f"{date.today()}")

                if not path.exists("./Entertainment"):
                    system("mkdir Entertainment")
                chdir("Entertainment")

                print(colored("\n\tDonwloading start.\n", "green"))

                for i in tqdm(range(len(links))):
                    try:
                        donwload_audio_YT(link=links[i])
                    except pytube.exceptions.RegexMatchError:
                        print(
                            (
                                colored(
                                    f"\n\n\tLink - {links[i]} is invalid\n",
                                    'red'
                                )
                            )
                        )

                        continue

                print(colored("\n\tDonwloading complete.\n", "green"))

    except KeyboardInterrupt:
        print(
            colored(
                "\n\tProgramm closed by Ctrl+C\n",
                'red'
            )
        )
    except ValueError:
        print(
            colored(
                "\n\tYou haven't selected a menu item or enter wrong value in input.\n",
                'red'
            )
        )


if __name__ == "__main__":

    main()
