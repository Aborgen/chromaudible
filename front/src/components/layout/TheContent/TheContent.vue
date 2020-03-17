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
