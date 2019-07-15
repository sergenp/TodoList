// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import {sync} from 'vuex-router-sync'
import store from './store/store'
import Panel from './components/global/Panel'
import colors from 'vuetify/es5/util/colors'

Vue.config.productionTip = false
Vue.use(Vuetify, {
  theme: {
    darkred: colors.red.darken1,
    lightred: colors.red.lighten1,
    primary: colors.red.darken2,
    secondary: colors.red.lighten4,
    accent: colors.indigo.base
  }
})
sync(store, router)
Vue.component('panel', Panel)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
