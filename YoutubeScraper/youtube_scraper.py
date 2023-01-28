import csv
import shutil
from multiprocessing import Pool
from datetime import date
from os import (chdir, getcwd, listdir, mkdir, path, remove, rename, rmdir,
                system)

import moviepy.editor as mp
import pytube.exceptions
from art import tprint
from pytube import Playlist
from pytube import YouTube as YT
from termcolor import colored
from tqdm import tqdm


def donwload_audio_YT(link: str) -> None:

    if "playlist" in link:

        playlist = Playlist(link)

        if not path.exists(f"./{str(playlist.title)}"):
            system(f'mkdir "{str(playlist.title).replace("/","-")}"')
        chdir(path.join(str(playlist.title).replace('/', '-')))

        for link in playlist.video_urls:
            print(colored(f"\n\n{YT(link).title}\n", "blue"))
            YT(link).streams.get_highest_resolution().download()

        return None

    print(
        colored
        (
            f"\n\n{YT(link).title}\n",
            "blue"
        )
    )
    YT(link).streams.get_by_itag("251").download()


def download_combine(link: str) -> None:
    title = str(YT(link).title).replace(
        ':', '').replace('/', '').replace("\\", "")
    print(
        colored(
            f"\n\n{title}\n",
            "blue"
        )
    )

    main_path = getcwd()

    if not path.exists(f"temp_{title}"):
        mkdir(f"temp_{title}")
    chdir(f"temp_{title}")

    YT(link).streams.filter(mime_type='audio/mp4').first().download()
    rename(listdir()[0], "1.mp4")

    YT(link).streams.filter(
        mime_type='video/mp4').order_by('resolution').desc().first().download()
    rename(listdir()[1], "2.mp4")
    mp.VideoFileClip("2.mp4").write_videofile(f'{title}.mp4', audio="1.mp4")

    remove("1.mp4")
    remove("2.mp4")
    shutil.move(listdir()[0], main_path)
    chdir("..")
    rmdir(f"temp_{title}")

    return None


def download_video_YT(link: str, quality: int) -> None:

    if "playlist" in link:

        playlist = Playlist(link)

        if not path.exists(f"./{str(playlist.title)}"):
            system(f'mkdir "{str(playlist.title).replace("/","-")}"')
        chdir(path.join(str(playlist.title).replace('/', '-')))

        if quality == 1:
            with Pool(5) as p:
                p.map(download_combine, playlist.video_urls)
        else:
            for link in playlist.video_urls:
                title = str(YT(link).title).replace(
                    ':', '').replace('/', '').replace("\\", "")
                print(
                    colored(
                        f"\n\n{title}\n",
                        "blue"
                    )
                )
                YT(link).streams.get_highest_resolution().download()
                continue

        return None

    title = str(YT(link).title).replace(
        ':', '').replace('/', '').replace("\\", "")
    print(
        colored(
            f"\n\n{title}\n",
            "blue"
        )
    )

    if quality == 1:
        download_combine(link=link, title=title)
    if quality == 2:
        YT(link).streams.get_highest_resolution().download()

    return None


def main():
    try:
        system('clear')
        tprint("Youtube scraper", "small")

        links = list()

        menu = int(input(
            "Select the type of file you would like to download on your PC.\n 1.Video \n 2.Audio\n>> "
        ))

        quality = 1

        if menu == 1:
            try:
                quality = int(input(
                    "\t\t Quality of video.\n\n 1.High.\n 2.Normal.\n>> "
                ))
            except ValueError:
                print("All videos will be downloaded in high quality.")

        with open("yt_links.csv") as csvfile:
            for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
                links.append(row[0])

        match menu:
            case 1:

                if not path.exists(f"./{date.today()}"):
                    system(f"mkdir {date.today()}")
                chdir(path.join(f"{date.today()}"))

                if not path.exists("./Video"):
                    system("mkdir Video")
                chdir(path.join("Video"))

                print(
                    colored(
                        "\n\tDonwloading start.\n",
                        "green"
                    )
                )

                for i in tqdm(range(len(links))):
                    try:
                        download_video_YT(link=links[i], quality=quality)
                    except pytube.exceptions.RegexMatchError:
                        print(
                            (
                                colored(
                                    f"\n\n\tLink - {links[i]} is invalid\n",
                                    "red"
                                )
                            )
                        )

                        continue

                print(
                    colored(
                        "\n\tDonwloading complete.\n",
                        "green"
                    )
                )

            case 2:

                if not path.exists(f"./{date.today()}"):
                    system(f"mkdir {date.today()}")
                chdir(path.join(f"{date.today()}"))

                if not path.exists("./Audio"):
                    system("mkdir Audio")
                chdir(path.join("Audio"))

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
