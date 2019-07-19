<template>
  <v-toolbar fixed color="primary">
    <v-toolbar-title class="mr-4">
      <span @click="navigateTo({name:'home'})" class="home">
        Todos App
      </span>
    </v-toolbar-title>
    <v-toolbar-items>
      <v-btn v-if="$store.state.isUserLoggedIn" flat class="primary" @click="navigateTo('todos')">Todos</v-btn>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn v-if="!$store.state.isUserLoggedIn" flat class="primary" @click="navigateTo('login')">Login</v-btn>
      <v-btn v-if="!$store.state.isUserLoggedIn" flat class="primary" @click="navigateTo('register')">Register</v-btn>
      <v-btn v-if="$store.state.isUserLoggedIn" flat class="primary" @click="logout()">Log Out</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
export default {
  name: 'Navbar',
  methods: {
    navigateTo (route) {
      this.$router.push(route)
    },
    logout () {
      this.$store.dispatch('setToken', null)
      this.$store.dispatch('setUser', null)
      this.$router.push({
        'name': 'home'
      })
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
