<template>
  <form @submit.prevent='handleSubmit' :class="formName + '_form file-form'">
    <section class='upload-group file-form-item'>
      <label for="upload">{{ inputLabel }}</label>
      <input id="upload" name="upload" type="file"
        :class="formName + '_input'" :disabled='formDisabled'
        :accept='acceptedTypes'
      >
    </section>
    <input id='submit' class='file-form-item' type="submit" value="submit" :disabled='formDisabled'>
  </form>
</template>

<script>
export default {
  name: 'FileForm',
  props: {
    handleSubmit: {
      type: Function,
      required: true
    },
    formDisabled: {
      type: Boolean,
      required: true
    },
    formName: {
      type: String,
      required: true
    },
    inputLabel: {
      type: String,
      required: true
    },
    acceptedTypes: {
      type: String,
      required: true
    }
  }
}
</script>


<style scoped>
  .file-form {
    display: flex;
    flex-flow: row wrap;
    align-items: stretch;
    border: 0.18rem solid black;
    box-sizing: border-box;
    width: auto;
    height: auto;
    min-width: auto;
    min-height: auto;
    padding: 0;
    margin: 0;
    font-size: 2rem;
  }

  .upload-group {
    display: flex;
    flex-flow: column wrap;
    align-items: stretch;
    justify-content: flex-end;
    text-align: left;
    flex-basis: 80%;
  }

  #submit {
    -webkit-appearance:none;
    text-decoration: none;
    margin: 0;
    flex: 1;
  }

  #upload, #submit, .upload-group label {
    font-size: inherit;
    min-width: 0;
    cursor: pointer;
  }

  #upload::-webkit-file-upload-button, #submit {
    background: #ffffff;
    -webkit-border-radius: 1rem;
    border: none;
    padding: 1rem;
    margin: 0;
  }

  #upload {
    width: 100%;
  }
</style>
