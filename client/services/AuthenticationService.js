import Api from './Api'

export default {
    register (credentials) {
        return Api().post('register', credentials)
    }, 
    login (credentials) {
        return Api().post('login', credentials)
    },
    getTodos () {
        return Api().get('todos')
    },
    addTodos (todos) {
        return Api().post('addTodo', todos)
    }
}
