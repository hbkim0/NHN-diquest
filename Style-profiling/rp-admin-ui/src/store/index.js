/* eslint-disable no-unused-vars */

import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'
import qs from "qs";
import defaultState from './state.js';

Vue.use(Vuex);

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;
axios.defaults.paramsSerializer = params => {
  return qs.stringify(params, {arrayFormat: 'repeat', skipNulls: true});
}
//Mockup 테스트용
//axios.defaults.baseURL = '';


export const store = new Vuex.Store({
  state: {
    productView: {
      identifier: null,
      gender: null,
      label: null,
      name: null,
      limit: 50,
    },
    historyView: {},
    customerView: {},
    monitoringView: {},
  },
  getters: {
    fetchedProductViewFilter(state) {
      return state.productView;
    },
  },
  mutations: {
    INIT_STATE(state) {
      Object.assign(state, defaultState);
    },
    SET_PRODUCTS(state, filter) {
      state.productView = filter;
    },
    SET_HISTORIES(state, filter) {
      state.historyView = filter;
    },
    SET_CUSTOMERS(state, filter) {
      state.customerView = filter;
    },
    SET_EXPERIMENTS(state, filter) {
      state.monitoringView = filter;
    },
  },
  actions: {
    INIT_STATE({commit}) {
      commit('INIT_STATE');
    },
    FETCH_CUSTOMERS(context, {identifier, gender, sort_by, page, limit}) {
      const filter = { 
        identifier : (typeof(identifier) !== 'undefined') ? identifier : null,
        gender : (typeof(gender) !== 'undefined') ? gender : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.customerView) === JSON.stringify(filter));
      console.log('store - FETCH_CUSTOMERS - filterChk', filterChk);
      context.commit('SET_CUSTOMERS', filter);
      page = filterChk ? page : 1;
      const pagenation = {
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0) && (typeof(limit) !== 'undefined')) ? ((page - 1) * limit) : 0,
      };
      
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_CUSTOMERS - params', params);
      return axios.get(`/api/v1/datasets/customers`, { params })
        .then(res => {
          console.log('store - FETCH_CUSTOMERS - res', res);
          const response = res.data;
          return {
            pagenation: {
              page: Math.floor(response.offset / response.limit) + 1, 
              length: Math.ceil(response.total_results / response.limit),
              limit: response.limit,
            },
            customers : response.results,
          };
        })
        .catch(error => { console.log(error); });
    },
    FETCH_HISTORIES(context, {customer, product, startDate, endDate, sort_by, page, limit}) {
      const filter = { 
        customer : (typeof(customer) !== 'undefined') ? customer : null,
        product : (typeof(product) !== 'undefined') ? product : null,
        start : (typeof(startDate) !== 'undefined') ? startDate : null,
        end : (typeof(endDate) !== 'undefined') ? endDate : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.historyView) === JSON.stringify(filter));
      console.log('store - FETCH_HISTORIES - filterChk', filterChk);
      context.commit('SET_HISTORIES', filter);
      page = filterChk ? page : 1;
      const pagenation = {  
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (typeof(limit) !== 'undefined') && (page > 0)) ? ((page - 1) * limit) : 0,
      };
      
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_HISTORIES - params', params);
      return axios.get(`/api/v1/datasets/historys`, { params })
        .then(res => {
          console.log('store - FETCH_HISTORIES - res', res);
          const response = res.data;
          return {
            pagenation: {
              page: Math.floor(response.offset / response.limit) + 1,  
              length: Math.ceil(response.total_results / response.limit),
              limit: response.limit,
            },
            histories : response.results,
          };
        })
        .catch(error => { console.log(error); });
    },
    FETCH_PRODUCTS(context, {identifier, label, gender, name, sort_by, page, limit}) {
      const filter = { 
        identifier : (typeof(identifier) !== 'undefined') ? identifier : null,
        label : (typeof(label) !== 'undefined') ? label : null,
        gender : (typeof(gender) !== 'undefined') ? gender : null,
        name : (typeof(name) !== 'undefined') ? name : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.productView) === JSON.stringify(filter));
      console.log('store - FETCH_PRODUCTS - filterChk', context.state.productView,filter,filterChk);
      context.commit('SET_PRODUCTS', filter);
      page = filterChk ? page : 1;
      const pagenation = { 
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (typeof(limit) !== 'undefined') && (page > 0)) ? ((page - 1) * limit) : 0,
      };
      
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_PRODUCTS - params', params);
      return axios.get(`/api/v1/datasets/products`, { params })
        .then(res => {
          console.log('store - FETCH_PRODUCTS - res', res);
          const response = res.data;
          return {
            labels: response.info,
            limit: response.limit,
            pagenation: {
              page: Math.floor(response.offset / response.limit) + 1, 
              length: Math.ceil(response.total_results / response.limit),
            },
            products : response.results,
          };
        })
        .catch(error => { console.log(error); });
    },
    FETCH_PRODUCT(context, id) {
      console.log('store - FETCH_PRODUCT - params', id);
      return axios.get(`/api/v1/datasets/products/${id}`)
        .then(res => {
          console.log('store - FETCH_PRODUCT - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_AUTOCOMPLETE(context, name) {
      const params = { 
        q : (typeof(name) !== 'undefined') ? name : null,
      };
      console.log('store - FETCH_AUTOCOMPLETE - params', params);
      return axios.get(`/api/v1/datasets/products/autocomplete`, { params })
        .then(res => {
          console.log('store - FETCH_AUTOCOMPLETE - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_STATUS(context, {start, end}) {
      const params = {
        start : (typeof(start) !== 'undefined') ? start : null,
        end : (typeof(end) !== 'undefined') ? end : null,
      };
      console.log('store - FETCH_STATUS - params', params);
      return axios.get(`/api/v1/datasets/status`, { params })
        .then(res => {
          console.log('store - FETCH_STATUS - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    INFER_TEXT(context, {name, description}) {
      const params = {
        name : (typeof(name) !== 'undefined') ? name : null,
        description : (typeof(description) !== 'undefined') ? description : null,
      };
      console.log('store - INFER_TEXT - params', params);
      return axios.post(`/api/v1/infer/text`, params)
        .then(res => {
          console.log('store - INFER_TEXT - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    INFER_IMAGE(context, {image}) {
      const params = {
        image : (typeof(name) !== 'undefined') ? image : null,
      };
      console.log('store - INFER_IMAGE - params', params);
      return axios.post(`/api/v1/infer/image`,  params)
        .then(res => {
          console.log('store - INFER_IMAGE - res', res);
          return res.data;
        })
        .catch(error => { console.log(error); });
    },
    FETCH_EXPERIMENTS(context, {seq_num_major, seq_num_minor, model_id, status, start, end, sort_by, page, limit}) {
      const filter = { 
        seq_num_major : (typeof(seq_num_major) !== 'undefined') ? seq_num_major : null,
        seq_num_minor : (typeof(seq_num_minor) !== 'undefined') ? seq_num_minor : null,
        model_id : (typeof(model_id) !== 'undefined') ? model_id : null,
        status : (typeof(status) !== 'undefined') ? status : null,
        start : (typeof(start) !== 'undefined') ? start : null,
        end : (typeof(end) !== 'undefined') ? end : null,
        limit: limit,
      }
      const filterChk = (JSON.stringify(context.state.monitoringView) === JSON.stringify(filter));
      context.commit('SET_EXPERIMENTS', filter);
      page = filterChk ? page : 1;
      const pagenation = { 
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (typeof(limit) !== 'undefined') && (page > 0)) ? ((page - 1) * limit) : 0,
      };
      
      
      const params = {...filter, ...pagenation};
      console.log('store - FETCH_EXPERIMENTS - params', params);
      return axios.get(`/api/v1/experiments`, { params })
        .then(res => {
          console.log('store - FETCH_EXPERIMENTS - res', res);
          const response = res.data;
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
    CREATE_EXPERIMENT(context,{model_id, parameters}) {
      const params = {
        model_id : (typeof(model_id) !== 'undefined') ? model_id : null,
        parameters : (typeof(parameters) !== 'undefined') ? Object.entries(parameters).map(r => {
          const returnParameters = {};
          returnParameters['key'] = r[0];
          returnParameters['value'] = r[1];
          return returnParameters;
        }) : null,
      };
      console.log('store - CREATE_EXPERIMENT - params', params);
      return axios.post(`/api/v1/experiments`, params)
        .then(res => {
          console.log('store - CREATE_EXPERIMENT - res', res);
          return res.data;
        }) 
        .catch(error => { console.log(error) });
    },
    DELETE_EXPERIMENT(context, {experiment_id}) {
      return axios.delete(`/api/v1/experiments/${experiment_id}`)
        .then(res => {
          console.log('store - DELETE_EXPERIMENT - res', res);
          return res.data;
        }) 
        .catch(error => { console.log(error) });
    },
    PATCH_EXPERIMENT(context, {experiment_id, model_id, parameters, serving}) {
      const params = {
        model_id : (typeof(model_id) !== 'undefined') ? model_id : null,
        serving : (typeof(serving) !== 'undefined') ? serving : null,
        parameters : (typeof(parameters) !== 'undefined') ? Object.entries(parameters).map(r => {
          const returnParameters = {};
          returnParameters['key'] = r[0];
          returnParameters['value'] = r[1];
          return returnParameters;
        }) : null,
      };
      console.log('store - PATCH_EXPERIMENT - params', params);
      return axios.patch(`/api/v1/experiments/${experiment_id}`, params)
        .then(res => {
          console.log('store - PATCH_EXPERIMENT - res', res);
          return res.data;
        }) 
        .catch(error => { console.log(error) });
    },
    PATCH_EXPERIMENT_MONITORING(context, {experiment_id, parameters, serving}) {
      const params = {
        serving : (typeof(serving) !== 'undefined') ? serving : null,
        parameters : (typeof(parameters) !== 'undefined') ? parameters : null,
      };
      console.log('store - PATCH_EXPERIMENT_MONITORING - params', params);
      return axios.patch(`/api/v1/experiments/${experiment_id}`, params)
        .then(res => {
          console.log('store - PATCH_EXPERIMENT_MONITORING - res', res);
          return res.data;
        }) 
        .catch(error => { console.log(error) });
    },
    FETCH_SCHEDULES(context) {
      return axios.get(`/api/v1/schedules`, { })
        .then(res => {
          console.log('store - FETCH_SCHEDULE - res', res);
          return res.data;
        })
        .catch(error => { console.log(error) });
    },
    PATCH_SCHEDULE(context, {cron}) {
      const params = {
        cron : (typeof(cron) !== 'undefined') ? cron : null,
      };
      console.log('store - PATCH_SCHEDULE - params', params);
      return axios.patch(`/api/v1/schedules`, params)
        .then(res => {
          console.log('store - PATCH_SCHEDULE - res', res);
          return res.data;
        })
        .catch(error => { console.log(error) });
    },
    CREATE_SCHEDULE(context, {priority, cron}) {
      const params = {
        priority : (typeof(priority) !== 'undefined') ? priority : null,
        cron : (typeof(cron) !== 'undefined') ? cron : null,
      };
      console.log('store - CREATE_SCHEDULE - params', params);
      return axios.post(`/api/v1/schedules`, params)
        .then(res => {
          console.log('store - CREATE_SCHEDULE - res', res);
          return res.data;
        })
        .catch(error => { console.log(error) });
    },
    FETCH_MODELS(context) {
      return axios.get(`/api/v1/models`, { })
        .then(res => {
          console.log('store - FETCH_MODELS - res', res);
          return res.data.results;
        })
        .catch(error => { console.log(error) });
    },
  },
  modules: {
  }
});