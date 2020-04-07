<template>
<section :class="classFromParent + ' content-container'">
  <section class='button-group'>
    <button class='flex-button' @click='setAudioMode'
            id='flex-button__first'
            :class='currentMode === ModeEnum.AUDIO && "selected-button"'>Audio</button>
    <button class='flex-button' @click='setImageMode'
            id='flex-button__second'
            :class='currentMode === ModeEnum.IMAGE && "selected-button"'>Image</button>
  </section>
  <section class='interactive-container'>
    <keep-alive>
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
    </keep-alive>
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
      baseUrl: `${process.env.VUE_APP_SERVER_ADDRESS}:${process.env.VUE_APP_SERVER_PORT}`,
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
    justify-content: stretch;
    align-items: stretch;
    margin: 1rem 3rem;
  }

  .content-container {
    display: flex;
    flex-flow: column nowrap;
    height: 100%;
  }

  .selected-button {
    flex: 1.1 !important;
    top: -0.1rem !important;
    transition: top 0.2s cubic-bezier(.23,1,.32,1);
    transition: flex 0.2s cubic-bezier(.23,1,.32,1);
    z-index: 2;
  }

  #flex-button__first.selected-button {
    box-shadow: 0.8rem 0.8rem 1rem -0.2rem #2E0303;
  }

  #flex-button__second.selected-button {
    box-shadow: -0.8rem 0.8rem 1rem -0.2rem #2E0303;
  }

  .flex-button {
    display: block;
    flex: 1;
    background: #d7d9b1;
    padding: 4rem;
    margin: 0;
    border: 0.2rem solid black;
    font-size: 7rem;
    letter-spacing: 0.5rem;
    font-variant-caps: small-caps;
    position: relative;
    top: 0;
    cursor: pointer;
    box-sizing: border-box;
    line-height: 7rem;
  }

  .flex-button:hover {
    background: #827191;
  }

  .flex-button:focus {
    background: #84acce;
  }

  #flex-button__first {
    border-left: 0 !important;
  }

  #flex-button__second {
    border-right: 0 !important;
  }

  .interactive-container {
    display: flex;
    height: 100%;
    align-items: center;
    justify-content: flex-start;
    flex-flow: column nowrap;
    background: #b0cadf;
    border-radius: 3rem;
    margin: 1rem 7rem;
    font-size: 1.5em
  }

  .interactive-item {
    display: flex;
    background: #d7d9b1;
    flex-flow: column nowrap;
    align-items: center;
    justify-content: center;
    margin-top: 7rem;
  }
</style>
