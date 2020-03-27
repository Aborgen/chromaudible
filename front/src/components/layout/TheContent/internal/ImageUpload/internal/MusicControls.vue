<template>
<section class='music-controls'>
  <section class='music-controls__display'>{{ displayText }}</section>
  <section class='music-controls__button-group'>
    <button :class="player.status === StatusEnum.PLAYING && 'status-button__active'"
            class='status-button'
            id='play-button' @click='play'>&#9658;</button>
    <button :class="player.status === StatusEnum.PAUSED && 'status-button__active'"
            class='status-button' 
            id='pause-button' @click='pause'>&#9646;&#9646;</button>
  </section>
</section>
</template>

<script>
import { MusicPlayer, StatusEnum } from 'utils/MusicPlayer';

function play() {
  if (this.player.status === StatusEnum.PLAYING || !this.canPlay) {
    return;
  }

  this.player.play();
  this.displayText = 'Now Playing';
  this.isPlaying = true;
}

function pause() {
  if (this.player.status === StatusEnum.PAUSED || !this.canPlay) {
    return;
  }

  this.player.pause();
  this.displayText = 'Paused';
  this.isPlaying = false;
}

function toggle() {
  if (this.player.status === StatusEnum.PLAYING) {
    this.pause();
  }
  else if (this.player.status === StatusEnum.PAUSED) {
    this.play()
  }
}

function auditMelodyParts() {
  if (!(this.melodyParts['melody'] &&
        this.melodyParts['volumeChanges'] &&
        this.melodyParts['timbreTexture'])) {
    this.displayText = 'Unable to play image: something went wrong';
    return false;
  }

  return true;
}

function init() {
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const context = new AudioContext();
  context.suspend();
  const { melody, volumeChanges, timbreTexture } = this.melodyParts;
  const gain = context.createGain();
  gain.gain.setValueAtTime(0.25, context.currentTime);
  gain.connect(context.destination);
  this.player = new MusicPlayer(context, melody, volumeChanges, timbreTexture, () => {
    this.displayText = 'Finished';
    this.canPlay = false;
    this.alertParentDone();
  });
}

export default {
  name: 'MusicControls',
  methods: {
    auditMelodyParts,
    init,
    pause,
    play,
    toggle
  },
  data() {
    return {
      displayText: "----",
      player: {},
      StatusEnum,
      canPlay: true
    }
  },
  props: {
    alertParentDone: {
      type: Function,
      required: true
    },
    melodyParts: {
      type: Object,
      required: true
    }
  },
  mounted() {
    if (this.auditMelodyParts()) {
      this.init();
    }
    else {
      this.canPlay = false;
    }
  }
}
</script>

<style scoped>
  .music-controls {
    color: #bad6c8;
    display: flex;
    flex-flow: column nowrap;
    justify-content: space-around;
    align-items: stretch;
    box-shadow: 0.8rem 0.5rem 0.5rem -0.2rem #2E0303;
    margin: 3rem 1rem 10rem 1rem;
    font-size: 0.5em;
    min-width: 50%;
    max-width: 0;
    box-sizing: border-box;
  }

  .music-controls__display {
    background: #131b23;
    flex: 1;
    border: 0.25rem inset #816c61;
    padding: 0.5rem 2rem;
    word-break: break-word;
  }

  .music-controls__button-group {
    background: #816c61;
    display: flex;
    flex: 1;
    flex-flow: row nowrap;
    justify-content: space-between;
    align-items: stretch;
  }

  .status-button {
    background: #8b311b;
    border-color: #7dacc8;
    flex: 1;
    color: #bad6c8;
    line-height: 5rem;
    cursor: pointer;
  }

  .status-button__active {
    background: #6b2514;
  }

  #play-button {
    font-size: 1em;
  }
</style>
