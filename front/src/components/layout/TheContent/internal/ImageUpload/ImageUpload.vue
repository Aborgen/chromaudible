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

function resetState(stopTrying=false, parentMessage='') {
  if (stopTrying) {
    this.currentLabel = parentMessage;
    this.formDisabled = true;
    return;
  }

  this.currentLabel = "Upload your music!";
  this.formDisabled = false;
}

async function playImage() {
  if (this.formDisabled) {
    return;
  }
  
  const input = document.getElementById('upload');
  if (input.files.length === 0) {
    this.currentLabel = 'Please choose an image to submit';
    this.formDisabled = false;
    return;
  }

  const imageFile = input.files[0];
  this.formDisabled = true;
  this.currentLabel = 'Awaiting response from server...';
  const url = `${this.baseUrl}/upload`;
  const res = await uploadImage(url, imageFile);
  if (!res.ok) {
    let message = ''
    if (res.status === 503) {
      message = 'Cannot connect to the server';
    }
    else {
      const error = await res.json();
      message = error.message;
    }

    this.currentLabel = `${message}: (Error code: ${res.status})`;
    this.handleError(res.status, this.resetState.bind(this));
    return;
  }

  player.play();
}

async function uploadImage(url, imageFile) {
  let data = new FormData();
  data.append('type', 'image');
  data.append('file', imageFile);
  return await fetchCatch(url, {
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
