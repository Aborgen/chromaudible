<template>
<section class='musicControls'>
  <section class='musicControls_display'>
    <span>{{ displayText }}</span>
  </section>
  <section class='musicControls_buttons'>
    <button id='playButton'>play</button>
    <button id='pauseButton'>pause</button>
  </section>
</section>
</template>

<script>
import { MusicPlayer, StatusEnum } from 'utils/MusicPlayer';

function play() {
  if (this.player.status === StatusEnum.PLAYING) {
    return;
  }

  this.player.play();
  this.displayText = 'Now Playing';
}

function pause() {
  if (this.player.status === StatusEnum.PAUSED) {
    return;
  }

  this.player.pause();
  this.displayText = 'Paused';
}

function toggle() {
  if (this.player.status === StatusEnum.PLAYING) {
    this.pause();
  }
  else if (this.player.status === StatusEnum.PAUSED) {
    this.play()
  }
}

function init() {
  document.getElementById('playButton').addEventListener('click', this.play, {once: true});
  document.getElementById('pauseButton').addEventListener('click', this.toggle);

  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const context = new AudioContext();
  context.suspend();
  const { melody, volumeChanges, timbreTexture } = this.melodyParts;
  const gain = context.createGain();
  gain.gain.setValueAtTime(0.25, context.currentTime);
  gain.connect(context.destination);
  this.player = new MusicPlayer(context, melody, volumeChanges, timbreTexture, () => {
    this.displayText = 'Finished';
    this.alertParentDone();
  });
}

export default {
  name: 'MusicControls',
  methods: {
    init,
    pause,
    play,
    toggle
  },
  data() {
    return {
      displayText: "Ready",
      player: {}
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
    this.init();
  }
}
</script>
