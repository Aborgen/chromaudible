<template>
<section :class="classFromParent + ' content-container'">
  <header>Time to do the thing</header>
  <section class='button-group'>
    <button @click='currentMode = ModeEnum.AUDIO'>Upload Audio</button>
    <button @click='currentMode = ModeEnum.IMAGE'>Upload Image</button>
  </section>
  <audio-upload v-if=     "currentMode === ModeEnum.AUDIO" />
  <image-upload v-else-if="currentMode === ModeEnum.IMAGE" />
</section>
</template>

<script>
import AudioUpload from './internal/AudioUpload/AudioUpload';
import ImageUpload from './internal/ImageUpload/ImageUpload';
import ModeEnum from './internal/misc/ModeEnum';

function setAudioMode() {
  if (this.currentMode !== ModeEnum.AUDIO) {
    this.currentMode = ModeEnum.AUDIO;
  }
}

function setImageMode() {
  if (this.currentMode !== ModeEnum.IMAGE) {
    this.currentMode = ModeEnum.IMAGE;
  }
}

export default {
  name: 'TheContent',
  components: {
    AudioUpload,
    ImageUpload
  },
  data: function() {
    return {
      currentMode: ModeEnum.AUDIO,
      ModeEnum
    }
  },
  methods: {
    setAudioMode,
    setImageMode
  },
  props: {
    'classFromParent': {
      type: String,
      required: true
    }
  }
}
</script>
