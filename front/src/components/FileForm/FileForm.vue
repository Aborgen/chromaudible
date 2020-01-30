<template>
  <form @submit.prevent='handleSubmit' :class="formName + '_form'">
    <label for="upload">{{ inputLabel }}</label>
    <input id="upload" name="upload" type="file" :class="formName + '_input'">
    <input type="submit" value="submit">
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
