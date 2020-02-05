<template>
<section class='audioUpload'>
  <file-form
    :handle-submit='convertToImage'
    :input-label='currentLabel'
    :form-disabled='formDisabled'
    form-name='audioUpload'
  />
</section>
</template>

<script>
import FileForm from 'components/FileForm/FileForm';

async function convertToImage() {
  const audioFile = document.getElementById('upload').files[0];
  const res = await getMelody('http://localhost:5000/upload', audioFile);
  if (!res.ok) {
    throw new Error(res.statusText);
  }

  this.currentLabel = 'Obtained melody!';
  // Result will be an object { timestamp: hexColor }. Will draw a canvas
  // With this in some way.
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
    convertToImage
  },
  data() {
    return {
      currentLabel: "Upload your music!"
    }
  }
}
</script>

