import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueRouter from 'vue-router'

import AddTodo from "@/components/AddTodo"
import EditTodo from "@/components/EditTodo"
import TodoItem from "@/components/Todos"

Vue.config.productionTip = false
Vue.prototype.$http = axios;
Vue.use(VueRouter);

// create a vuerouter instance
const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [{
    path: '/',
    component: TodoItem,
    name: 'home'
  },
    {
      path: '/add-todo',
      component: AddTodo,
      name: 'add-todo'
    },
    {
      path: '/edit-todo/:id',
      component: EditTodo,
      name: 'edit-todo'
    },
  ]
});

// pass the router to the app config
new Vue({
  router: router,
  render: h => h(App),
}).$mount('#app');
