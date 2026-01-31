#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import argcomplete

from urllib.parse import urlparse, parse_qs


def clean_youtube_url(url):
    if "/watch?v=" not in url:
        return url
    parsed = urlparse(url)
    video_id = parse_qs(parsed.query).get("v")
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id[0]}"
    return url


def ask_to_continue():
    response = input("Do you wish to continue? (y/n): ").lower()
    if response != "y":
        print("Interrupted")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Adm v3.0",
        epilog="Have fun!",
    )

    subparsers = parser.add_subparsers(dest="command")

    vid_parser = subparsers.add_parser("vid")
    vid_parser.add_argument("url")
    vid_parser.add_argument("dir", nargs="?", default="")

    imp_parser = subparsers.add_parser("imp")
    imp_parser.add_argument("url")

    subparsers.add_parser("youtube")
    subparsers.add_parser("vpn")

    docker_parser = subparsers.add_parser("docker")
    docker_parser.add_argument("action", choices=["stopall"])

    subparsers.add_parser("color-pallete")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    cmd = args.command

    if cmd == "vid":
        subprocess.run(
            [
                "yt-dlp",
                "-f",
                "bestvideo+bestaudio",
                "-S",
                "res:720",
                "--embed-metadata",
                "--embed-subs",
                "--embed-thumbnail",
                "--download-archive",
                os.path.expanduser("~/Videos/.yt-dlp-download-archive"),
                "-P",
                os.path.expanduser(f"~/Videos/{args.dir}"),
                clean_youtube_url(args.url),
            ]
        )
    elif cmd == "imp":
        subprocess.run(
            [
                "yt-dlp",
                "-f",
                "bestvideo+bestaudio",
                "-S",
                "res:720",
                "--embed-metadata",
                "--embed-subs",
                "--embed-thumbnail",
                "--download-archive",
                os.path.expanduser("~/Videos/imp-videos/.yt-dlp-download-archive"),
                "-P",
                os.path.expanduser("~/Videos/imp-videos"),
                clean_youtube_url(args.url),
            ]
        )
    elif cmd == "youtube":
        subprocess.run(["./main.pl"], cwd=os.path.expanduser("~/projects/yt-offline"))
    elif cmd == "vpn":
        subprocess.run(
            [
                "sudo",
                "openvpn",
                "--config",
                os.path.expanduser("~/vpn/mullvad_pl_all.conf"),
            ]
        )
    elif cmd == "docker":
        if args.action == "stopall":
            result = subprocess.run(
                ["docker", "ps", "-q"], capture_output=True, text=True, check=True
            )
            container_ids = result.stdout.strip().split()
            if container_ids:
                subprocess.run(["docker", "stop"] + container_ids)
    elif cmd == "backup-full-system":
        command = [
            "sudo",
            "rsync",
            "-aAXHv",
            "--delete",
        ]
        excludes = [
            "/dev/*",
            "/proc/*",
            "/sys/*",
            "/tmp/*",
            "/run/*",
            "/mnt/*",
            "/media/*",
            "/lost+found/",
            "/home/*/.local/share/Trash/*",
            "/home/*/.cache/BraveSoftware/*",
        ]
        for pattern in excludes:
            command.extend(["--exclude", pattern])
        command.extend(["/", "/mnt/backup"])
        print("WARNING! Review this command carefully!")
        print("Command to be executed:\n")
        print(" ".join(command))
        print()
        ask_to_continue()
        subprocess.run(command)
    elif cmd == "color-pallete":
        for i in range(256):
            print(f"\x1b[48;5;0m\x1b[38;5;{i}m{i:3d}", end="")
            print(f"\x1b[48;5;{i}m{i:3d}\x1b[38;5;0m", end="")
            if i == 15 or (i > 15 and (i - 15) % 12 == 0):
                print("\x1b[48;5;0m")
        pass
    else:
        print("Invalid command", file=sys.stderr)
