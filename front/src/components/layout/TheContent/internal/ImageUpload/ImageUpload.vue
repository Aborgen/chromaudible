<template>
<section class='imageUpload'>
  <file-form
    :handleSubmit='playImage'
    :input-label='currentLabel'
    form-name='imageUpload'
  />
</section>
</template>

<script>
import FileForm from 'components/FileForm/FileForm';
//import MusicPlayer from 'utils/MusicPlayer';

async function playImage() {
  const imageFile = document.getElementById('upload').files[0];
  const res = await uploadImage('http://localhost:5000/upload', imageFile);
  if (!res.ok) {
    throw new Error(res.statusText);
  }

  const text = await res.json();
  this.currentLabel = text;
  /*
  const { melody, volumeChanges, timbreTexture } = await res.json();
  const context = new AudioContext();
  context.suspend();
  const gain = context.createGain();
  gain.gain.setValueAtTime(0.25, context.currentTime);
  gain.connect(context.destination);
  const player = new MusicPlayer(context, melody, volumeChanges, timbreTexture);
  player.play();
  */
}

async function uploadImage(url, imageFile) {
  let data = new FormData();
  data.append('type', 'image');
  data.append('file', imageFile);
  return await fetch(url, {
    method: 'POST',
    body: data
  });
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
      currentLabel: "Upload your image!"
    }
  }
}
</script>

