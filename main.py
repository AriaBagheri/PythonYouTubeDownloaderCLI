import secrets
from enum import Enum

import pytube.request
from pytube import YouTube
import typer

pytube.request.default_range_size = 524288


class VideoResolution(str, Enum):
    q_max = "max"
    q_1080 = "1024p"
    q_720 = "720p"
    q_360 = "360p"
    q_min = "min"


def main(link: str = typer.Option("", help="Link of the YouTube Video to Download"),
         resolution: VideoResolution = typer.Option(VideoResolution.q_max,
                                                    help="You can select the resolution to download your file at."),
         audio_only: bool = False):
    while not link:
        link = typer.prompt("Please input a youtube video link to be downloaded: ")

    yt = YouTube(link)
    typer.echo(f"\nTitle: {yt.title}\n")
    typer.echo(f"Number of Views: {yt.views}\n")
    typer.echo(f"Length of Video: {yt.length}\n")

    if audio_only:
        ys = yt.streams.get_audio_only()
    elif resolution == VideoResolution.q_max:
        ys = yt.streams.get_highest_resolution()
    elif resolution == VideoResolution.q_min:
        ys = yt.streams.get_lowest_resolution()
    else:
        ys = yt.streams.get_by_resolution(resolution.value)

    with typer.progressbar(length=ys.filesize, show_eta=True, show_percent=True, color=True) as progress:
        def progress_callback(bytes_remaining):
            progress.update(ys.filesize - bytes_remaining)

        yt.register_on_progress_callback(lambda _, __, x: progress_callback(x))
        ys.download("downloads/", filename=secrets.token_hex(8) + "." + ys.default_filename.split(".")[-1])
        typer.echo("\nDownload Completed!")


if __name__ == "__main__":
    typer.run(main)
