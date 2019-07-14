<template>
  <v-toolbar fixed color="primary">
    <v-toolbar-title class="mr-4">
      <span @click="navigateTo({name:'home'})" class="home">
        Todos App
      </span>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn flat class="primary" @click="navigateTo('login')">Login</v-btn>
      <v-btn flat class="primary" @click="navigateTo({name:'register'})">Register</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
export default {
  name: 'Navbar',
  methods: {
    navigateTo (route) {
      this.$router.push(route)
    }
  }
}
</script>

<style scoped>
.home {
  cursor: pointer;
  color: white;
}
.home:hover {
  color: black;
}
</style>
