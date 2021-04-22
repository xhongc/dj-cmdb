import Vue from 'vue'
import Vuex from 'vuex'

import cookie from './cookie'

Vue.use(Vuex)
const state = {
  userInfo: {},
  token: cookie.getCookie('token') || ''
}
export default new Vuex.Store({
  state,
  getters: {},
  mutations: {
    setUserInfo (state, token) {
      state.token = token
    }
  },
  actions: {}
})
