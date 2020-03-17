<template>
<section :class="classFromParent + ' content-container'">
  <section class='button-group'>
    <button class='flex-button' @click='setAudioMode'
            :id='currentMode === ModeEnum.AUDIO && "selected-button"'>Audio</button>
    <button class='flex-button' @click='setImageMode'
            :id='currentMode === ModeEnum.IMAGE && "selected-button"'>Image</button>
  </section>
  <section class='interactive-container'>
    <audio-upload v-if             ="currentMode === ModeEnum.AUDIO"
                  :base-url        ='baseUrl'
                  :handle-error    ='handleError'
                  class-from-parent='interactive-item'
    />
    <image-upload v-else-if        ="currentMode === ModeEnum.IMAGE"
                  :base-url        ='baseUrl'
                  :handle-error    ='handleError'
                  class-from-parent='interactive-item'
    />
  </section>
</section>
</template>

<script>
import AudioUpload from './internal/AudioUpload/AudioUpload';
import ImageUpload from './internal/ImageUpload/ImageUpload';
import ModeEnum from './internal/misc/ModeEnum';

function resetState() {
  this.allowedRetries = 3;
}

function setAudioMode() {
  if (this.currentMode === ModeEnum.AUDIO) {
    return;
  }

  this.resetState();
  this.currentMode = ModeEnum.AUDIO;
}

function setImageMode() {
  if (this.currentMode === ModeEnum.IMAGE) {
    return;
  }

  this.resetState();
  this.currentMode = ModeEnum.IMAGE;
}

function handleError(errorCode, func) {
  if (errorCode === this.lastHTTPCode && this.allowedRetries > 0) {
    this.allowedRetries--;
  }
  else if (this.lastHTTPCode !== 0) {
    this.allowedRetries++;
  }

  this.lastHTTPCode = errorCode;
  const stopTrying = this.allowedRetries <= 0;
  const message = 'The server is unavailable. Please try again later.';
  const timeout = stopTrying ? 4000 : 3000;
  setTimeout(() => func(stopTrying, message), timeout);
}

export default {
  name: 'TheContent',
  components: {
    AudioUpload,
    ImageUpload
  },
  data: function() {
    return {
      baseUrl: 'http://localhost:5000',
      currentMode: ModeEnum.AUDIO,
      ModeEnum,
      lastHTTPCode: 0,
      allowedRetries: 2
    }
  },
  methods: {
    setAudioMode,
    setImageMode,
    handleError,
    resetState
  },
  props: {
    classFromParent: {
      type: String,
      required: true
    }
  }
}
</script>

<style>
  .button-group {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    align-items: stretch;
    margin: 15px 50px;
    box-shadow: 25px 10px 13px 2px rgba(60, 79, 94, 0.8);
  }

  .content-container {
    display: flex;
    flex-flow: column nowrap;
  }

  #selected-button {
    flex: 1.5;
    transition-property: flex;
    transition-duration: 10ms;
  }

  .flex-button {
    flex: 1;
    background: #d7d9b1;
    margin: 0 -15px;
    padding: 0;
    border: 3px solid black;
    font-size: 7rem;
    letter-spacing: 0.5rem;
    font-variant-caps: small-caps;
  }

  .flex-button:hover {
    background: #827191;
    cursor: pointer;
  }

  .flex-button:focus {
    background: #84acce !important;
  }

  .flex-button:first-of-type {
    border-left: 0;
  }

  .flex-button:last-of-type {
    border-right: 0;
  }

  .interactive-container {
    display: flex;
    flex: 1 0 50%;
    justify-content: flex-start;
    align-items: center;
    flex-flow: column nowrap;
    background: #b0cadf;
    border-radius: 3rem;
/*    margin: 2rem 10rem; */
  }

  .interactive-item {
    background: #d7d9b1;
    margin: 10rem 4rem 0 4rem;
  }
</style>
