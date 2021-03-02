import Vue from 'vue'
import Router from 'vue-router'
import home from '@/views/Home.vue'
import model from '@/views/Model.vue'
import resource from '@/views/Resource.vue'
import field from '@/views/Field.vue'
import relation from '@/views/Relation.vue'
import topo from '@/views/Topo.vue'
Vue.use(Router)

const includPush = Router.prototype.push
/* eslint-disable */
Router.prototype.push = function push(location) {
  return includPush.call(this, location).catch(err => err)

}

export default new Router({
  mode: 'history',
  routes: [{
    path: '/',
    name: 'home',
    component: home,
    children: [{
        path: '/model/',
        name: 'model',
        component: model
      },
      {
        path: '/resource/',
        name: 'resource',
        component: resource
      },
      {
        path: '/field/',
        name: 'field',
        component: field
      },
      {
        path: '/relation/',
        name: 'relation',
        component: relation
      },
      {
        path: '/topo/',
        name: 'topo',
        component: topo
      }
    ]
  }]
})
