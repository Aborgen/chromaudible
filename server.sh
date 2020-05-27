#!/usr/bin/env bash
set -e

buildDir=./build
serverDir=./back

hostName="0.0.0.0"
port="8000"
# From Ihunath's answer on stackoverflow: https://stackoverflow.com/a/677212
command -v ffmpeg >/dev/null 2>&1 || {
  echo >&2 "ffmpeg is required to run chromeaudible. Aborting."
  exit 1
}

[ -f /usr/local/lib/vamp/mtg-melodia.so ] || [ -f "$HOME/vamp/mtg-melodia.so" ] || ([ ! -z "$VAMP_PATH" ] && [ -f "$VAMP_PATH/mtg-melodia.so" ]) || {
  printf "Melodia is required to run chromeaudible [https://www.upf.edu/web/mtg/melodia]. Aborting.\n"
  exit 1
}

[ -d "$buildDir" ] || {
  printf "Please execute build.sh first. Aborting.\n"
  exit 1
}

# Activate already existing Python3 venv
source "$serverDir/bin/activate"

cd "$buildDir"
uvicorn --host "$hostName" --port "$port" main:app
