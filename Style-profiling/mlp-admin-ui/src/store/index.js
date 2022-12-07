/* eslint-disable no-unused-vars */

import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'
import qs from "qs";
axios.defaults.paramsSerializer = params => {
  return qs.stringify(params, {arrayFormat: 'repeat', skipNulls: true});
}

Vue.use(Vuex);

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;


export const store = new Vuex.Store({
  state: {
    datasetView: {},
    annotationView: {},
    versionedDatasetView: {},
    experimentView: {},
  },
  getters: {
    fetchedDatasetViewFilter(state) {
      return state.datasetView;
    },
    fetchedAnnotationViewFilter(state) {
      return state.annotationView;
    },
    fetchedVersionedDatasetViewFilter(state) {
      return state.versionedDatasetView;
    },
    fetchedExperimentViewFilter(state) {
      return state.experimentView;
    },
  },
  mutations: {
    SET_DATASETS(state, filter) {
      state.datasetView = filter;
    },
    SET_ANNOTATIONS(state, filter) {
      state.annotationView = filter;
    },
    SET_VERSIONEDDATASETVIEW(state, filter) {
      state.versionedDatasetView = filter;
    },
    SET_EXPERIMENTS(state, filter) {
      state.experimentView = filter;
    },
  },
  actions: {
    CREATE_TENSORBOARD_URL(context, experiment_id) {
      return axios.post(`/api/v1/tensorboards`, { experiment_ids : experiment_id })
        .then(res => {
          console.log('store - GET_TENSORBOARD_URL - res', res);
          return {
            url: res.data.url,
            status: res.status
          };
        })
        .catch(error => { 
          console.log(error); 
          return {
            status: error.response.status
          };
        });
    },
    GET_TEXT_CONTENT(context, url) {
      return axios.get(`${url}`)
        .then(res => {
          console.log('store - GET_TEXT_CONTENT', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    UPLOAD_FILES(context, {dataset_id, bundle_id, files}) {
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      console.log(typeof(files),files);
      const frm = new FormData();
      (typeof(dataset_id) !== 'undefined') ? frm.append('dataset_id', dataset_id) : frm.append('dataset_id', null);
      (typeof(bundle_id) !== 'undefined') ? frm.append('bundle_id', bundle_id) : frm.append('bundle_id', '');
      (typeof(files) !== 'undefined') ? frm.append('files', files) : frm.append('files', null);

      return axios.post(`/files/upload`, frm, {headers: headers})
        .then(res => {
          console.log('store - fileupload - cover image', res);
          const response = res.data;
          return { image_url : response.url };
        })
        .catch(error => { 
          console.log(error);
          return { image_url : null }; 
        });
    },
    FETCH_DATASETS(context, {ml_task, sort_by, page, limit}){
      const filter = { 
        ml_task: (typeof(ml_task) !== 'undefined') ? ml_task : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.datasetView) === JSON.stringify(filter));
      context.commit('SET_DATASETS', filter);
      page = filterChk ? page : 1;
      const pagenation = {
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0) && (typeof(limit) !== 'undefined')) ? ((page - 1) * limit) : 0,
      };
      
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_DATASET_ALL - params', params);
      return axios.get(`/api/v1/datasets`, {params})
        .then(res => {
          const response = res.data;
          console.log('store - FETCH_DATASET_ALL - res', res);

          return {
            total_results: response.total_results,
            limit: response.limit,
            pagenation: {
                page: Math.floor(response.offset / response.limit) + 1,   
                length: Math.ceil(response.total_results / response.limit),
            },
            datasets : response.results,
          };
        })
        .catch(error => { console.log(error); });
    },
    CREATE_DATASET(context, {ml_task, name, description}) {
      const params = {
        ml_task: (typeof(ml_task) !== 'undefined') ? ml_task : null,
        name: (typeof(name) !== 'undefined') ? name : null,
        description: (typeof(description) !== 'undefined') ? description : null,
      }

      console.log('store - CREATE_DATASET - params', params);
      return axios.post(`/api/v1/datasets`, params)
        .then(res => {
          const response = res.data;
          console.log('store - CREATE_DATASET - res', res);

          return response;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_DATASET(context, dataset_id) {
      return axios.get(`/api/v1/datasets/${dataset_id}`)
        .then(res => {
          const response = res.data;
          
          console.log('FETCH_DATASET_ALL - res', res);
          
          return {
            _id: response._id,
            ml_task: response.ml_task,
            name: response.name,
            description: response.description,
            labeled_data: response.labeled_data,
            total_data: response.total_data,
            cover_image: response.cover_image,
          };

        })
        .catch(error => { console.log(error); });
    },
    UPDATE_DATASET(context, {_id, name, description, cover_image}) {
      const params = {
        _id: (typeof(_id) !== 'undefined') ? _id : null,
        name: (typeof(name) !== 'undefined') ? name : null,
        description: (typeof(description) !== 'undefined') ? description : null,
        cover_image: (typeof(cover_image) !== 'undefined') ? cover_image : null,
      }

      //cover_iamge 처리 필요.
      return axios.patch(`/api/v1/datasets/${_id}`, params)
        .then(res => {
          console.log('store - UPDATE_DATASET - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    DELETE_DATASET(context, dataset_id) {
      return axios.delete(`/api/v1/datasets/${dataset_id}`)
        .then(res => {
            const response = res.data;

            return response;
        })
        .catch(error => { console.log(error); });

    },
    CREATE_BUNDLE(context, {dataset_id, name, description}) {
      const params = {
        dataset_id: (typeof(dataset_id) !== 'undefined') ? dataset_id : null,
        name: (typeof(name) !== 'undefined') ? name : null,
        description: (typeof(description) !== 'undefined') ? description : null,
      }

      console.log('store - CREATE_BUNDLE - params', params);
      return axios.post(`/api/v1/bundles`, params)
        .then(res => {
          const response = res.data;

          return response;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_BUNDLES(context, dataset_id) {
      const params = { dataset_id : (typeof(dataset_id) !== 'undefined') ? dataset_id : null };
      return axios.get(`/api/v1/bundles`, {params})
        .then(res => {
          console.log('store - FETCH_BUNDLES - res', res);
          const response = res.data;

          return response;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_BUNDLE(context, bundle_id) {
      return axios.get(`/api/v1/bundles/${bundle_id}`)
        .then(res => {
            const response = res.data;

            return response;
        })
        .catch(error => { console.log(error); });
    },
    UPDATE_BUNDLE(context, {_id, name, description, attributes}) {
      const params = {
        name: (typeof(name) !== 'undefined') ? name : null,
        description: (typeof(description) !== 'undefined') ? description : null,
        attributes: (typeof(attributes) !== 'undefined') ? attributes : null,
      }
      console.log('store - UPDATE_BUNDLE - params', params);
      return axios.patch(`/api/v1/bundles/${_id}`, params)
        .then(res => {
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    DELETE_BUNDLE(context, bundle_id) {
      return axios.delete(`/api/v1/bundles/${bundle_id}`)
        .then(res => {
            const response = res.data;

            return response;
        })
        .catch(error => { console.log(error); });

    },
    FETCH_ANNOTATIONS(context, {maintain, dataset_id, sort_by, page, limit, bundle_ids, label_status, attribute, versioned_dataset_id, split, offset}) {
      const filter = { 
        dataset_id: (typeof(dataset_id) !== 'undefined') ? dataset_id : null,
        bundle_id: (typeof(bundle_ids) !== 'undefined') ? bundle_ids : null,
        versioned_dataset_id: (typeof(versioned_dataset_id) !== 'undefined') ? versioned_dataset_id : null,
        attribute: (typeof(attribute) !== 'undefined') ? attribute : null,
        split: (typeof(split) !== 'undefined') ? split : null,
        labeled: (typeof(label_status) !== 'undefined') ? label_status : null,
        limit: limit,
      }
      
      const filterChk = (JSON.stringify(context.state.annotationView) === JSON.stringify(filter));
      if((typeof(maintain) === 'undefined') ? true : maintain){
        context.commit('SET_ANNOTATIONS', filter);
      }
      console.log('filter', context.state.annotationView);
      page = filterChk ? page : 1;     
      const pagenation = {
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: (typeof(offset) !== 'undefined') !== 'undefined' ? offset : ((typeof(page) === 'number') && (page > 0) && (typeof(limit) !== 'undefined')) ? ((page - 1) * limit) : 0,
      };
      
      const params = {...filter, ...pagenation};
      
      console.log('FETCH_ANNOTATIONS - params', params);
      return axios.get(`/api/v1/annotations`, { params: params })
        .then(res => {
          const response = res.data;
          console.log('store - FETCH_ANNOTATIONS - res', res);
          
          return {
            total_results: response.total_results,
            limit: response.limit,
            pagenation: {
              page: Math.floor(response.offset / response.limit) + 1,   
              length: Math.ceil(response.total_results / response.limit),
            },
            annotations : response.results,
          };
        })
        .catch(error => { console.log(error); })
    },
    FETCH_ANNOTATION(context, annotation_id) {
      return axios.get(`/api/v1/annotations/${annotation_id}`)
        .then(res => {
          const response = res.data;          
          console.log('store - FETCH_ANNOTATION', response);
          return response;
        })
        .catch(error => { console.log(error); })
    },
    PATCH_ANNOTATION(context, {annotation_id, done, labels}) {
      const params = {
        done: (typeof(done) !== 'undefined') ? done : null,
        labels: (typeof(labels) !== 'undefined') ? labels : null,
      }
      return axios.patch(`/api/v1/annotations/${annotation_id}`, params)
        .then(res => {
          const response = res.data;
          console.log('store - PATCH_ANNOTATION', response);
        })
        .catch(error => { console.log(error); })
    },
    CREATE_LABEL(context, {dataset_id, name, color}) {
      const params = {
        dataset_id: (typeof(dataset_id) !== 'undefined') ? dataset_id : null,
        name: (typeof(name) !== 'undefined') ? name : null,
        color: (typeof(color) !== 'undefined') ? color : null,
      }
      return axios.post(`/api/v1/labels`, params)
        .then(res => {
          const response = res.data;
          console.log('store - CREATE_LABEL', response);
          return {
            label_id: response._id,
            name: response.name,
            color: response.color,
          };
        })
        .catch(error => { console.log(error) });
    },
    PATCH_LABEL(context, {label_id, name, color}) {
      const params = {
        name: (typeof(name) !== 'undefined') ? name : null,
        color: (typeof(color) !== 'undefined') ? color : null,
      }
      return axios.patch(`/api/v1/labels/${label_id}`, params)
        .then(res => {
          const response = res.data;
          console.log('store - PATCH_LABEL', response);
          return response;
        })
        .catch(error => { console.log(error) });
    },
    FETCH_VERSIONEDDATASETS(context, {ml_task, sort_by, page, limit, dataset_id, status}){      
      const filter = { 
        ml_task: (typeof(ml_task) !== 'undefined') ? ml_task : null,
        dataset_id: (typeof(dataset_id) !== 'undefined') ? dataset_id : null,
        status: (typeof(status) !== 'undefined') ? status : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.versionedDatasetView) === JSON.stringify(filter));
      context.commit('SET_VERSIONEDDATASETVIEW', filter);
      page = filterChk ? page : 1;     
      const pagenation = {
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0) && (typeof(limit) !== 'undefined')) ? ((page - 1) * limit) : 0,
      };
      
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_VERSIONEDDATASETS - params', params);
      return axios.get(`/api/v1/versioned-datasets`, {params})
        .then(res => {
          const response = res.data;
          console.log('store - FETCH_VERSIONEDDATASETS - res', res);

          return {
            limit: response.limit,
            pagenation: {
              page: Math.floor(response.offset / response.limit) + 1,   
              length: Math.ceil(response.total_results / response.limit),
            },
            versionedDatasets : response.results,
          };
        })
        .catch(error => { console.log(error); });
    },
    FETCH_VERSIONEDDATASET(context, versioneddataset_id){
      
      console.log('store - FETCH_VERSIONEDDATASET - versioneddataset_id', versioneddataset_id);
      return axios.get(`/api/v1/versioned-datasets/${versioneddataset_id}`)
        .then(res => {
          console.log('store - FETCH_VERSIONEDDATASET - res', res);

          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    DELETE_VERSIONEDDATASET(context, versioneddataset_id){
      
      console.log('store - DELETE_VERSIONEDDATASET - versioneddataset_id', versioneddataset_id);
      return axios.delete(`/api/v1/versioned-datasets/${versioneddataset_id}`)
        .then(res => {
          console.log('store - DELETE_VERSIONEDDATASET - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    CREATE_VERSIONEDDATASET(context, {dataset, bundles, preprocessing, augmentation, name, split}) {
      const params = {
        dataset_id: (typeof(dataset) !== 'undefined') ? dataset : null,
        bundle_ids: (typeof(bundles) !== 'undefined') ? bundles : null,
        preprocessing: (typeof(preprocessing) !== 'undefined') ? preprocessing : null,
        augmentation: (typeof(augmentation) !== 'undefined') ? augmentation : null,
        name: (typeof(name) !== 'undefined') ? name : null,
        split: (typeof(split) !== 'undefined') ? split : null,
      };

      params.preprocessing = params.preprocessing.filter(r => r.activate === 1);
      params.augmentation = params.augmentation.filter(r => r.activate === 1);
      
      console.log('store - CREATE_VERSIONEDDATASET - params', params);
      return axios.post(`/api/v1/versioned-datasets`, params)
        .then(res => {
          console.log('store - CREATE_VERSIONEDDATASET - res', res);
          return res.data;
        })
        .catch(error => { console.log(error) });
    },
    FETCH_EXPERIMENTS(context, {ml_task, sort_by, page, limit, dataset_id, status}) {      
      const filter = { 
        ml_task: (typeof(ml_task) !== 'undefined') ? ml_task : null,
        dataset_id: (typeof(dataset_id) !== 'undefined') ? dataset_id : null,
        status: (typeof(status) !== 'undefined') ? status : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.experimentView) === JSON.stringify(filter));
      context.commit('SET_EXPERIMENTS', filter);
      page = filterChk ? page : 1;     
      const pagenation = {
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0) && (typeof(limit) !== 'undefined')) ? ((page - 1) * limit) : 0,
      };
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_EXPERIMENTS - params', params);
      return axios.get(`/api/v1/experiments`, {params})
        .then(res => {
          const response = res.data;
          console.log('store - FETCH_EXPERIMENTS - res', res);

          return {
            pagenation: {
              page: Math.floor(response.offset / response.limit) + 1,   
              length: Math.ceil(response.total_results / response.limit),
              limit: response.limit,
            },
            experiments : response.results,
          };
        })
        .catch(error => { console.log(error); });
    },
    FETCH_EXPERIMENT(context, experiment_id) {
      return axios.get(`/api/v1/experiments/${experiment_id}`)
        .then(res => {
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_MODELS(context, {ml_task}) {
      const params = {
        ml_task: (typeof(ml_task) !== 'undefined') ? ml_task : null,
      }
      console.log('store - FETCH_MODELS - params', params);
      return axios.get(`/api/v1/models`, {params})
        .then(res => {
          const response = res.data;
          console.log('store - FETCH_MODELS - res', response);
          return response.results;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_FUNCTIONS(context, {ml_task}) {
      const params = {
        ml_task: (typeof(ml_task) !== 'undefined') ? ml_task : null,
      };
      console.log('store - FETCH_FUNCTIONS - params', params);
      return axios.get(`/api/v1/functions`, {params})
        .then(res => {
          const response = res.data;
          console.log('store - FETCH_FUNCTIONS - res', response);
          return response.results;
        })
        .catch(error => { console.log(error); });
    },
    CREATE_EXPERIMENT(context, {dataset_id, versioned_dataset_id, model_id, name}) {
      const params = {
        dataset_id: (typeof(dataset_id) !== 'undefined') ? dataset_id : null,
        versioned_dataset_id: (typeof(versioned_dataset_id) !== 'undefined') ? versioned_dataset_id : null,
        model_id: (typeof(model_id) !== 'undefined') ? model_id : null,
        name: (typeof(name) !== 'undefined') ? name : null,
      };
      return axios.post(`/api/v1/experiments`, params)
        .then(res => {
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    PATCH_EXPERIMENT(context, {experiment_id, editExperimentDto}) {
      const params = (typeof(editExperimentDto) !== 'undefined') ? editExperimentDto : null;
      console.log('store - PATCH_EXPERIMENT - params', params);
      return axios.patch(`/api/v1/experiments/${experiment_id}`, params)
        .then(res => {
          console.log('store - PATCH_EXPERIMENT - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });

    },
    DELETE_EXPERIMENT(context, experiment_id) {
      return axios.delete(`/api/v1/experiments/${experiment_id}`)
        .then(res => {
          console.log('store - DELETE_EXPERIMENT - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    }
  },
  modules: {
  }
});