/* eslint-disable no-unused-vars */

import Vue from 'vue';
import VueRouter from 'vue-router';

import HomeView from '../views/HomeView.vue';

import MLTaskView from '../views/MLTaskView.vue';

import DatasetView from '../views/DatasetView.vue';
import DatasetDetailView from '../views/DatasetDetailView.vue';
import DatasetEditView from '../views/DatasetEditView.vue';
import DatasetUploadView from '../views/DatasetUploadView.vue';

import BundleEditView from '../views/BundleEditView.vue';

import AnnotationView from '../views/AnnotationView.vue';
import LabelingView from '../views/LabelingView.vue';

import VersionedDatasetView from '../views/VersionedDatasetView.vue';
import VersionedDatasetDetailView from '../views/VersionedDatasetDetailView.vue';
import VersionedDatasetGenerateView from '../views/VersionedDatasetGenerateView.vue';

import ExperimentView from '../views/ExperimentView.vue';
import ExperimentEditView from '../views/ExperimentEditView.vue';
import ExperimentDetailView from '../views/ExperimentDetailView.vue';

import SystemView from '../views/SystemView.vue';


Vue.use(VueRouter);

export const router = new VueRouter({
    mode: 'history',
    routes: [
        {
          path: '/',
          redirect: '/home',
        },
        {
          path: '/home',
          name: 'HomeView',
          component: HomeView,
          meta: {
            breadcrumbs: [
              { text: 'HOME' },
            ]
          },
        },
        {
          path: '/mltask',
          name: 'MLTaskView',
          component: MLTaskView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'MLTask' },
           ]
          },
        },
        {
          path: '/datasets',
          name: 'DatasetView',
          component: DatasetView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'Dataset' },
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
          path: '/datasets/:dataset_id',
          name: 'DatasetDetailView',
          component: DatasetDetailView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'Dataset', to: '/dataset', exact: true },
              { text: 'Dataset Detail' },
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
          path: '/datasets/:dataset_id/edit',
          name: 'DatasetEditView',
          component: DatasetEditView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Dataset', to: {name: 'DatasetView'}, exact: true },
              { text: 'Dataset Detail', to: {name: 'DatasetDetailView', params: route.params}, exact: true },
              { text: 'Edit Dataset' },
            ])
          },
        },
        {
          path: '/datasets/:dataset_id/upload',
          name: 'DatasetUploadView',
          component: DatasetUploadView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Dataset', to: {name: 'DatasetView'}, exact: true },
              { text: 'Dataset Detail', to: {name: 'DatasetDetailView', params: route.params}, exact: true },
              { text: 'Upload' },
            ])
          },
        },
        {
          path: '/datasets/:dataset_id/bundles/:bundle_id',
          name: 'BundleEditView',
          component: BundleEditView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Dataset', to: {name: 'DatasetView'}, exact: true },
              { text: 'Dataset Detail', to: {name: 'DatasetDetailView', params: route.params}, exact: true },
              { text: 'Edit Bundle' },
            ])
          },
        },
        {
          path: '/annotations',
          name: 'AnnotationView',
          component: AnnotationView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'Annotation' },
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
          path: '/annotations/labeling',
          name: 'LabelingView',
          component: LabelingView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Annotation', to: {name: 'AnnotationView'}, exact:true },
              { text: 'Labeling', },
            ])
          },
        },
        {
          path: '/versioneddatasets',
          name: 'VersionedDatasetView',
          component: VersionedDatasetView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'Versioned Dataset' },
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
          path: '/versioneddatasets/generate',
          name: 'VersionedDatasetGenerateView',
          component: VersionedDatasetGenerateView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Versioned Dataset', to: {name: 'VersionedDatasetView'}, exact:true },
              { text: 'Versioned Dataset Generate' },
            ])
          },
        },
        {
          path: '/versioneddatasets/:versioneddataset_id',
          name: 'VersionedDatasetDetailView',
          component: VersionedDatasetDetailView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Versioned Dataset', to: {name: 'VersionedDatasetView'}, exact:true},
              { text: 'Versioned Dataset Detail' },
            ])
          },
        },
        {
          path: '/experiments',
          name: 'ExperimentView',
          component: ExperimentView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'Experiment' },
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
          path: '/experiments/:experiment_id/edit',
          name: 'ExperimentEditView',
          component: ExperimentEditView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Experiment', to: {name: 'ExperimentView'}, exact: true },
              { text: 'Edit Experiment' },
            ])
          },
        },
        {
          path: '/experiments/:experiment_id',
          name: 'ExperimentDetailView',
          component: ExperimentDetailView,
          meta: {
            breadcrumbs: (route) => ([
              { text: 'HOME', to: '/' },
              { text: 'Experiment', to: {name: 'ExperimentView'}, exact: true },
              { text: 'Experiment Detail' },
            ])
          },
        },
        {
          path: '/system',
          name: 'SystemView',
          component: SystemView,
          meta: {
            breadcrumbs: [
              { text: 'HOME', to: '/' },
              { text: 'System' },
            ]
          },
        },
    ]
})
