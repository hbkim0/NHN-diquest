import Vue from 'vue';
import VueRouter from 'vue-router';

import WorkbookView from '../views/WorkbookView.vue';
import WorkbookDetailView from '../views/WorkbookDetailView.vue';
import WorkbookEditView from '../views/WorkbookEditView.vue';
import PageDetailView from '../views/PageDetailView.vue';
import PageEditView from '../views/PageEditView.vue';
import PageLabelingView from '../views/PageLabelingView.vue';
import TestView from '../views/TestView.vue';
import LogsView from '../views/LogsView.vue';
import SystemView from '../views/SystemView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: '/workbooks',
  },
  {
    path: '/workbooks',
    name: 'WorkbookView',
    component: WorkbookView,
    meta: {
      breadcrumbs: [
        {text: '문제집'},
      ]
    }
  },
  {
    path: '/workbooks/:workbook_id',
    name: 'WorkbookDetailView',
    component: WorkbookDetailView,
    meta: {
      breadcrumbs: [
        {text: '문제집', exact: true, to: '/workbooks'},
        {text: '문제집 상세'},
      ]
    }
  },
  {
    path: '/workbooks/:workbook_id/edit',
    name: 'WorkbookEditView',
    component: WorkbookEditView,
    meta: {
      breadcrumbs: (route) => ([
        {text: '문제집', exact: true, to: '/workbooks'},
        {text: '문제집 상세', exact: true, to: {name: 'WorkbookDetailView', params: route.params}},
        {text: '문제집 수정'},
      ])
    }
  },
  {
    path: '/workbooks/:workbook_id/:page_id',
    name: 'PageDetailView',
    component: PageDetailView,
    meta: {
      breadcrumbs: (route) => ([
        {text: '문제집', exact: true, to: '/workbooks'},
        {text: '문제집 상세', exact: true, to: {name: 'WorkbookDetailView', params: route.params}},
        {text: '페이지 상세'},
      ])
    }
  },
  {
    path: '/workbooks/:workbook_id/:page_id/edit',
    name: 'PageEditView',
    component: PageEditView,
    meta: {
      breadcrumbs: (route) => ([
        {text: '문제집', exact: true, to: '/workbooks'},
        {text: '문제집 상세', exact: true, to: {name: 'WorkbookDetailView', params: route.params}},
        {text: '페이지 수정'},
      ])
    }
  },
  {
    path: '/workbooks/:workbook_id/:page_id/labeling',
    name: 'PageLabelingView',
    component: PageLabelingView,
    meta: {
      breadcrumbs: (route) => ([
        {text: '문제집', exact: true, to: '/workbooks'},
        {text: '문제집 상세', exact: true, to: {name: 'WorkbookDetailView', params: route.params}},
        {text: '페이지 수정', exact: true, to: {name: 'PageEditView', params: route.params}},
        {text: '라벨링'},
      ])
    }
  },
  {
    path: '/test',
    name: 'TestView',
    component: TestView,
    meta: {
      breadcrumbs: [
        {text: '테스트'}
      ]
    }
  },
  {
    path: '/logs',
    name: 'LogsView',
    component: LogsView,
    meta: {
      breadcrumbs: [
        {text: '로그'}
      ]
    }
  },
  {
    path: '/system',
    name: 'SystemView',
    component: SystemView,
    meta: {
      breadcrumbs: [
        {text: '시스템'}
      ]
    }
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
