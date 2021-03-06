import Api from './Api'

export default {
    register (credentials) {
        return Api().post('register', credentials)
    }, 
    login (credentials) {
        return Api().post('login', credentials)
    },
    getTodos () {
        return Api().get('getTodos')
    },
    saveTodos (todos) {
        return Api().post('saveTodos', todos)
    }
}
