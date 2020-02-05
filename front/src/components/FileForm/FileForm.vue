<template>
  <form @submit.prevent='handleSubmit' :class="formName + '_form'">
    <label for="upload">{{ inputLabel }}</label>
    <input id="upload" name="upload" type="file" :class="formName + '_input'" :disabled='formDisabled'>
    <input type="submit" value="submit" :disabled='formDisabled'>
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
    }
  }
}
</script>
