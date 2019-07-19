<template>
  <v-layout v-if="$store.state.isUserLoggedIn" column>
    <v-flex xs6>
      <div class="white elevation-6">
        <v-toolbar dark color="darkRed">
          <v-toolbar-title>Todos</v-toolbar-title>
        </v-toolbar>
        <div row wrap expand class="pl-4 pr-4 pt-4 pb-4">
          <div>
            <v-toolbar flat color="white">
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on }">
                  <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
                </template>
                <v-card>
                  <v-card-title>
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
                          <v-switch v-model="editedItem.completed" label="Completed"></v-switch>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.created_at" label="Created At"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.finished_at" label="Finished At"></v-text-field>
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
            </v-toolbar>
            <v-data-table
              :headers="headers"
              :items="todos"
              class="elevation-1 text-xs-center"
            >
              <template v-slot:items="props">
                <td class="text-xs-center">{{ props.item.todo_title }}</td>
                <td class="text-xs-center">{{ props.item.todo_body }}</td>
                <td class="text-xs-center">{{ props.item.completed }}</td>
                <td class="text-xs-center">{{ props.item.created_at }}</td>
                <td class="text-xs-center">{{ props.item.finished_at }}</td>
                <td class="justify-center layout px-0">
                  <v-icon
                    small
                    class="mr-2"
                    @click="editItem(props.item)"
                  >
                    edit
                  </v-icon>
                  <v-icon
                    small
                    @click="deleteItem(props.item)"
                  >
                    delete
                  </v-icon>
                </td>
              </template>
            </v-data-table>
          </div>
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthenticationService from '../../services/AuthenticationService'

export default {
  data: () => ({
    dialog: false,
    headers: [
      { text: 'Todo Title', align: 'left', sortable: false, value: 'todo_title' },
      { text: 'Description', value: 'todo_body' },
      { text: 'Completed', value: 'completed' },
      { text: 'Created At', value: 'created_at' },
      { text: 'Finished At', value: 'finished_at' },
      { text: 'Actions', value: 'name', sortable: false }
    ],
    todos: [],
    editedIndex: -1,
    editedItem: {
      todo_title: '',
      todo_body: '',
      completed: false,
      created_at: '',
      finished_at: ''
    },
    defaultItem: {
      todo_title: '',
      todo_body: '',
      completed: false,
      created_at: '',
      finished_at: ''
    }
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    }
  },

  watch: {
    dialog (val) {
      val || this.close()
    }
  },

  created () {
    this.initialize()
  },
  methods: {
    async getTodos () {
      const response = await AuthenticationService.getTodos()
      console.log(response.data)
    },
    navigateTo (route) {
      this.$router.push(route)
    },
    initialize () {
      this.todos = [
        {
          todo_title: 'Frozen Yogurt',
          todo_body: 6.0,
          created_at: 24,
          finished_at: 4.0,
          completed: false
        },
        {
          todo_title: 'Ice cream sandwich',
          todo_body: 237,
          created_at: 9.0,
          finished_at: 37,
          completed: false
        },
        {
          todo_title: 'Eclair',
          todo_body: 262,
          created_at: 16.0,
          finished_at: 23,
          completed: false
        }
      ]
    },

    editItem (item) {
      this.editedIndex = this.todos.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem (item) {
      const index = this.todos.indexOf(item)
      confirm('Are you sure you want to delete this item?') && this.todos.splice(index, 1)
    },

    close () {
      this.dialog = false
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
</style>
