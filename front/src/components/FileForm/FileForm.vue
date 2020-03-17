<template>
  <form @submit.prevent='handleSubmit' :class="formName + '_form file-form'">
    <section class='upload-group file-form-item'>
      <label for="upload">{{ inputLabel }}</label>
      <input id="upload" name="upload" type="file"
        :class="formName + '_input'" :disabled='formDisabled'
        :accept='acceptedTypes'
      >
    </section>
    <input class='file-form-item' type="submit" value="submit" :disabled='formDisabled'>
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
    justify-content: space-between;
    align-items: stretch;
    flex-flow: row wrap;
    font-size: 2rem;
  }

  .upload-group {
    display: flex;
    flex-flow: column nowrap;
    justify-content: space-between;
    text-align: left;
  }
</style>
