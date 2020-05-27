<img src="https://user-images.githubusercontent.com/28365047/83079065-d96e1a00-a02f-11ea-86f4-f60cf9102f1e.png" align="center" title="Chromaudible's homepage"></img>
<img src="https://user-images.githubusercontent.com/28365047/83079236-3ff33800-a030-11ea-8fde-f671e8ace2a9.png" align="right" width=300 alt="Example of an image produced by Chromaudible" title="Example of an image produced by Chromaudible"></img>

Chromaudible is a toy project for encoding the essence of a song into an image (example to the right). The image, in turn, can be played utilizing the Web Audio API. As of now, it is intended to work only on songs that have vocals. Any other sound file is unlikely to provide a good result.

The lion's share of the work is done by the following two libraries:
* [Spleeter](https://github.com/deezer/spleeter) -- Responsible for isolating vocals for a cleaner audio file for further use
* [Melodia](https://www.upf.edu/web/mtg/melodia) -- Performs melody extraction, which is what is then encoded in the images produced by Chromaudible

# Dependencies
Most of the dependencies are handled for the backend and frontend with pip and npm, respectively. Outside of that, you need:
1) A Python3 version < 3.8
2) ffmpeg
3) Melodia (https://www.upf.edu/web/mtg/melodia). Per Melodia's license, I am unable to distribute it, so it must be installed separately.
4) npm

# Setup
1) Create a virtual environment inside the back directory. Install dependencies within the virtual environment with pip
    * ```cd back```
    * ```python3 -m venv ./```
      * This must be done with a Python3 version < 3.8, due to spleeter requirements.
    * ```source bin/activate```
    * ```pip3 install -r requirements.txt```
    * ```deactivate```
    * ```cd ../```
2) Install npm dependencies
    * ```npm --prefix='./front' install```
3) Create a production build of the Vue frontend, as well as place all necessary files into a new directory called build
    * ```./build.sh```
4) Run the Starlette server with Uvicorn within the Python virtual environment
    * ```./server.sh```

# Usage
After processing by the server, an uploaded audio file is converted into an image\
NOTE: the shown image is a downsampled thumbnail. The image should be downloaded by clicking the hypelink.
<img src="https://user-images.githubusercontent.com/28365047/83079063-d8d58380-a02f-11ea-99f3-a2fe51c743d9.png" title="Image ready to be downloaded after uploading audio file"></img>

Images are then able to be played utilizing the Web Audio API!\
NOTE: Chromaudible accepts any image file, not only an audio canvas generated from the Audio tab. The resulting sound has the potential to be interesting...
<img src="https://user-images.githubusercontent.com/28365047/83076405-539ba000-a02a-11ea-9ab6-ce506240bdac.png" title="Player ready after uploading image"></img>

