<template>
<section class='image-upload'
         :class='classFromParent'
>
  <file-form
    :handle-submit='playImage'
    :input-label='currentLabel'
    :form-disabled='formDisabled'
    accepted-types='image/*'
    form-name='image-upload'
  />
</section>
</template>

<script>
import fetchCatch from 'utils/FetchCatch';
import FileForm from 'components/FileForm/FileForm';
import MusicPlayer from 'utils/MusicPlayer';

function playImage() {
  const imageFile = document.getElementById('upload').files[0];
  this.formDisabled = true;
  this.currentLabel = 'Awaiting response from server...';
  uploadImage('http://localhost:5000/upload', imageFile).then(((res) => {
    this.currentLabel = 'Playing image';
    doIt(res, this);
  }).bind(this));
}

function doIt(res, that) {
  const { melody, volumeChanges, timbreTexture } = res;
  const context = new AudioContext();
  context.suspend();
  const gain = context.createGain();
  gain.gain.setValueAtTime(0.25, context.currentTime);
  gain.connect(context.destination);
  const player = new MusicPlayer(context, melody, volumeChanges, timbreTexture, () => {
    that.currentLabel = 'JOB DONE';
    that.formDisabled = false;
  });

  player.play();
}

async function uploadImage(url, imageFile) {
  let data = new FormData();
  data.append('type', 'image');
  data.append('file', imageFile);
  const res = await fetch(url, {
    method: 'POST',
    body: data
  });

  if (!res.ok) {
    throw new Error(res.statusText);
  }

  return await res.json();
}

export default {
  name: 'ImageUpload',
  components: {
    FileForm
  },
  methods: {
    playImage
  },
  data() {
    return {
      currentLabel: "Upload your image!",
      formDisabled: false
    }
  }
}
</script>

<style scoped>
  .image-upload_form {
    flex: 0 0 5%;
    border: 2px solid black;
  }
</style>
