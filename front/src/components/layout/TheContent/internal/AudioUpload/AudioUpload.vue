<template>
<section class='audioUpload'>
  <file-form
    :handleSubmit='playMusic'
    :input-label='currentLabel'
    form-name='audioUpload'
  />
</section>
</template>

<script>
import FileForm from 'components/FileForm/FileForm';
import MusicPlayer from 'utils/MusicPlayer';

async function playMusic() {
  const audioFile = document.getElementById('upload').files[0];
  const res = await getMelody('http://localhost:5000/upload', audioFile);
  if (!res.ok) {
    throw new Error(res.statusText);
  }

  const melody = await res.json();
  const context = new AudioContext();
  context.suspend();
  const gain = context.createGain();
  gain.gain.setValueAtTime(0.25, context.currentTime);
  gain.connect(context.destination);
  const player = new MusicPlayer(context, melody);
  player.play();
}

async function getMelody(url, audioFile) {
  let data = new FormData();
  data.append('type', 'audio');
  data.append('file', audioFile);
  return await fetch(url, {
    method: 'POST',
    body: data
  });
}

export default {
  name: 'AudioUpload',
  components: {
    FileForm
  },
  methods: {
    playMusic
  },
  data() {
    return {
      currentLabel: "Upload your music!"
    }
  }
}
</script>

