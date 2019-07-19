<template>
  <v-layout column>
    <v-flex xs12>
      <panel title="Add Todos">
        <form>
          <v-text-field label="Todo Title" v-model="todoDict.todo_title"></v-text-field>
          <br />
          <v-textarea v-model="todoDict.todo_body" placeholder="Todo Text"></v-textarea>
        </form>
        <br />
        <div class="danger-alert" v-html="error" />
        <br />
        <v-btn dark class="lightRed" @click="addTodo(todoDict)">Add</v-btn>
        <v-btn dark class="lightRed" @click="getTodos()">Get</v-btn>
      </panel>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthenticationService from '../../services/AuthenticationService'

export default {
  data () {
    return {
      todos: [],
      todoDict: {
        todo_id: null,
        todo_title: null,
        todo_body: null,
        completed: false
      }
    }
  },
  methods: {
    addTodo (todo) {
      this.todos.push(todo)
      console.log(this.todos)
    },
    async getTodos () {
      const response = await AuthenticationService.getTodos()
      console.log(response.data)
    }
  }
}
</script>

<style scoped>
</style>
