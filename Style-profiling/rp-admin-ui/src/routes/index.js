/* eslint-disable no-unused-vars */

import Vue from 'vue';
import VueRouter from 'vue-router';

//Status
import StatusView from '../views/StatusView.vue';

//Dataset
import CustomerView from '../views/CustomerView.vue';
import ProductView from '../views/ProductView.vue';
import ProductDetailView from '../views/ProductDetailView.vue';
import HistoryView from '../views/HistoryView.vue';

//Experiment
import ExperimentView from '../views/ExperimentView.vue';

//Monitoring
import MonitoringView from '../views/MonitoringView.vue';

//Store
import { store } from '../store/index.js';

Vue.use(VueRouter);

export const router = new VueRouter({
    mode: 'history',
    routes: [
      {
        path: '/',
        redirect: '/status',
      },
      {
        path: '/status',
        name: 'StatusView',
        component: StatusView,
        meta: {
          breadcrumbs: [
            { text: 'Status' },
         ]
        },
      },
      {
        path: '/customers',
        name: 'CustomerView',
        component: CustomerView,
        meta: {
          breadcrumbs: [
            { text: 'Dataset', disabled: true },
            { text: 'Customer' },
         ]
        },
      },
      {
        path: '/products',
        name: 'ProductView',
        component: ProductView,
        meta: {
          breadcrumbs: [
            { text: 'Dataset', disabled: true },
            { text: 'Product' },
         ]
        },
        beforeEnter: (to, from, next) => {
          // to.path가 from.path의 상위 start path와 일치확인
          // true - 필터 유지 O
          // false - 필터 유지 X
          to.params.filterMaintain = from.path.startsWith(to.path);
          next();
        },
      },
      {
        path: '/products/:product_id',
        name: 'ProductDetailView',
        component: ProductDetailView,
        meta: {
          breadcrumbs: (route) => ([
            { text: 'Dataset', disabled: true },
            { text: 'Product', to: { name: 'ProductView' }, exact: true },
            { text: 'Product Detail'},
          ])
        },
      },
      {
        path: '/histories',
        name: 'HistoryView',
        component: HistoryView,
        meta: {
          breadcrumbs: [
            { text: 'Dataset', disabled: true },
            { text: 'History' },
         ]
        },
      },
      {
        path: '/experiments',
        name: 'ExperimentView',
        component: ExperimentView,
        meta: {
          breadcrumbs: [
            { text: 'Experiment' },
         ]
        },
      },
      {
        path: '/monitoring',
        name: 'MonitoringView',
        component: MonitoringView,
        meta: {
          breadcrumbs: [
            { text: 'Monitoring' },
         ]
        },
      },
    ]
})
