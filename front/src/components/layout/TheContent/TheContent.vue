<template>
<section :class="classFromParent + ' content-container'">
  <header>Time to do the thing</header>
  <button @click='setAudioMode'>Upload Audio</button>
  <button @click='setImageMode'>Upload Image</button>
  <audio-upload v-if="currentMode === ModeEnum.AUDIO" />
  <div v-else-if="currentMode === ModeEnum.IMAGE">WATCH THIS SPACE</div>
</section>
</template>

<script>
import AudioUpload from './internal/AudioUpload/AudioUpload';
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
    AudioUpload
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
