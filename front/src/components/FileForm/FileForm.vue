<template>
  <form :class="formName + '_form'" method='POST' :action='action'>
    <label for="upload">{{ inputLabel }}</label>
    <input name="upload" type="file" :class="formName + '_input'">
    <input type="submit" value="submit">
  </form>
</template>

<script>
export default {
  name: 'FileForm',
  props: {
    formName: {
      type: String,
      required: true
    },
    inputLabel: {
      type: String,
      required: true
    },
    action: {
      type: String,
      required: true,
      default: '#'
    }
  }
}
</script>
