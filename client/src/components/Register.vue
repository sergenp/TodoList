<template>
  <v-layout column>
    <v-flex xs6>
      <panel title="Register">
        <form>
          <v-text-field label="Email" v-model="email"></v-text-field>
          <br />
          <v-text-field label="Password" type="password" v-model="password" autocomplete="new-password"></v-text-field>
        </form>
        <br />
        <div class="danger-alert" v-html="error" />
        <br />
        <v-btn dark class="lightRed" @click="register">Register</v-btn>
      </panel>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthenticationService from '../../services/AuthenticationService'
export default {
  name: 'Register',
  data () {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async register () {
      try {
        const response = await AuthenticationService.register({
          email: this.email,
          password: this.password
        })
        this.$store.dispatch('setToken', response.data.token)
        this.$store.dispatch('setUser', response.data.user)
        this.$router.push({
          'name': 'myTodos'
        })
      } catch (error) {
        this.error = error.response.data.error
      }
    }
  }
}
</script>

<style scoped>
</style>
