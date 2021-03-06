import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist'

Vue.use(Vuex)

const vuexPersist = new VuexPersist({
  storage: window.localStorage
})
// tracking global states using Vuex
const store = new Vuex.Store({
  strict: true,
  state: {
    token: null,
    user: null,
    isUserLoggedIn: false,
    UserTodos: []
  },
  mutations: {
    setToken (state, token) {
      state.token = token
      if (token) {
        state.isUserLoggedIn = true
      } else {
        state.isUserLoggedIn = false
      }
    },
    setUser (state, user) {
      state.user = user
    },
    setUserTodos (state, UserTodos) {
      state.UserTodos = UserTodos
    }
  },
  actions: {
    setToken ({ commit }, token) {
      commit('setToken', token)
    },
    setUser ({ commit }, user) {
      commit('setUser', user)
    },
    setUserTodos ({ commit }, UserTodos) {
      commit('setUserTodos', UserTodos)
    }
  },
  plugins: [vuexPersist.plugin]
})

export default store
