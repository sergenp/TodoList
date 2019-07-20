<template>
  <v-layout v-if="$store.state.isUserLoggedIn" row>
    <v-flex xs12>
      <div class="white elevation-6">
        <v-toolbar dark color="darkRed">
          <v-toolbar-title>Todos</v-toolbar-title>
        </v-toolbar>
        <div row wrap expand class="pl-4 pr-4 pt-4 pb-4">
          <v-toolbar flat color="white">
            <v-dialog v-model="editItemDialog" max-width="1000px">
              <template v-slot:activator="{ on }">
                <v-btn color="lightRed" dark class="mb-2" v-on="on">Add New Todo</v-btn>
              </template>
              <v-card>
                <v-card-title color="accent">
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.todo_title" label="Todo Title"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.todo_body" label="Description"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.created_at" label="Created At">
                          <v-date-picker v-model="editedItem.created_at" no-title scrollable>
                            <v-spacer></v-spacer>
                            <v-btn flat color="primary">
                              Cancel
                            </v-btn>
                            <v-btn flat color="primary">
                              OK
                            </v-btn>
                          </v-date-picker>
                        </v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.completed_at" label="Completed At"></v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="lightRed" flat @click="close">Cancel</v-btn>
                  <v-btn color="lightRed" flat @click="save">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-spacer></v-spacer>
            <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
          </v-toolbar>
          <v-data-table :loading="todosLoading" :headers="headers" :items="todos" :search="search">
            <template v-slot:items="props">
              <td class="text-xs-left">{{ props.item.todo_title }}</td>
              <td class="text-xs-left">{{ props.item.todo_body }}</td>
              <td class="text-xs-left completed">
                <v-checkbox @click="setCompleted(props.item)" v-model="props.item.completed" primary hide-details></v-checkbox>
              </td>
              <td class="text-xs-left">{{ props.item.created_at }}</td>
              <td class="text-xs-left">{{ props.item.completed_at }}</td>
              <td class="justify-center layout px-0">
                <v-icon small class="mr-2" @click="editItem(props.item)">
                  edit
                </v-icon>
                <v-icon small @click="deleteItem(props.item)">
                  delete
                </v-icon>
              </td>
            </template>
          </v-data-table>
          <v-btn :disabled="saveToDbDialog" :loading="saveToDbDialog" class="white--text" color="lightRed" @click="saveToDbDialog=true">Save The List</v-btn>
          <v-dialog v-model="saveToDbDialog" hide-overlay persistent width="250">
            <v-card color="primary" dark>
              <v-card-text class="text-xs-center">
                Saving list to Database
                <v-progress-linear indeterminate color="accent" class="mb-0"></v-progress-linear>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-dialog v-model="savedSuccessDialog" hide-overlay persistent width="250">
            <v-card color="primary" dark>
              <v-card-text class="text-xs-center">
                Saved Successfully
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthenticationService from '../../services/AuthenticationService'
import moment from 'moment'

export default {
  data: () => ({

    search: '',
    editItemDialog: false,
    saveToDbDialog: false,
    savedSuccessDialog: false,
    todosLoading: true,
    headers: [
      { text: 'Title', align: 'left', value: 'todo_title' },
      { text: 'Description', value: 'todo_body' },
      { text: 'Completed', value: 'completed' },
      { text: 'Created At', value: 'created_at' },
      { text: 'Completed At', value: 'completed_at' },
      { text: 'Actions', value: 'name', sortable: false }
    ],
    todos: [],
    editedIndex: -1,
    editedItem: {
      todo_title: '',
      todo_body: '',
      completed: false,
      created_at: null,
      completed_at: null
    },
    defaultItem: {
      todo_title: '',
      todo_body: '',
      completed: false,
      created_at: null,
      completed_at: null
    }
  }),
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    }
  },
  watch: {
    editItemDialog (val) {
      val || this.close()
    },
    async saveToDbDialog (val) {
      if (!val) return
      await this.saveTodos()
      this.saveToDbDialog = false
      this.savedSuccessDialog = true
    },
    savedSuccessDialog (val) {
      setTimeout(() => {
        this.savedSuccessDialog = false
      }, 1000)
    }
  },
  created () {
    this.initialize()
  },
  methods: {
    async saveTodos () {
      const response = await AuthenticationService.saveTodos(this.todos)
      console.log(response.data)
    },
    getCurrentDate () {
      return moment().format('MMMM Do YYYY, h:mm:ss a')
    },
    navigateTo (route) {
      this.$router.push(route)
    },

    async initialize () {
      const response = await AuthenticationService.getTodos(this.todos)
      this.todos = response.data
      this.todosLoading = false
    },

    editItem (item) {
      this.editedIndex = this.todos.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.editItemDialog = true
    },

    deleteItem (item) {
      const index = this.todos.indexOf(item)
      confirm('Are you sure you want to delete this item?') && this.todos.splice(index, 1)
    },

    setCompleted (item) {
      const index = this.todos.indexOf(item)
      this.todos[index].completed_at = this.getCurrentDate()
    },

    close () {
      this.editItemDialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },

    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.todos[this.editedIndex], this.editedItem)
      } else {
        this.todos.push(this.editedItem)
      }
      this.close()
    }
  }
}
</script>

<style scoped>
.completed {
  cursor: pointer;
}
.completed:hover {
  color: black;
}
</style>
