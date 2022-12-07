/* eslint-disable no-unused-vars */

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const _DEFAULT_LIMIT = 10;

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
    UPLOAD_IMAGES(context, files) {
      //
      if (!Array.isArray(files)) {
        files = [files, ];
      }

      //
      const headers = {'Content-Type': 'multipart/form-data'};
      let form = new FormData();
      // form.append('images', files)
      files.forEach(file => {
        form.append('images', file);
      });

      console.log('UPLOAD_IMAGES: form - ', form);
      return window.$axios.post('/images/upload', form, {headers})
        .then(res => {
          console.log('UPLOAD_IMAGES: res - ', res);
          return res.data;
        })
        .catch(error => {
          console.log(error);
          return {};
        });
    },

    FETCH_WORKBOOKS(context, { applied, sort_by, page }) {
      const params = {
        applied: (typeof(applied) !== 'undefined') ? applied : null,
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0)) ? ((page - 1) * _DEFAULT_LIMIT) : 0,
        limit: _DEFAULT_LIMIT,
      };

      //
      console.log('FETCH_WORKBOOKS: params - ', params);
      return window.$axios.get('/api/v1/workbooks', {params})
        .then(res => {
          console.log('FETCH_WORKBOOKS: res - ', res);

          const response = res.data;
          const filter = new URLSearchParams(response.filtering);

          applied = parseInt(filter.get('applied'));
          if(!Number.isInteger(applied)) {
            applied = null;
          }

          return {
            filter: {applied},
            // search: "",
            // sort_by: response.sort_by || '',
            pagination: {
              value: Math.floor(response.offset / _DEFAULT_LIMIT) + 1,    // value는 1부터 시작함.
              length: Math.ceil(response.total_results / _DEFAULT_LIMIT),
            },
            workbooks: response.results
          };
        });
    },
    FETCH_WORKBOOKS_ALL(context) {
      let params = { offset: 0, limit: 0 };

      //
      console.log('FETCH_WORKBOOKS_ALL(total_results): params - ', params);
      return window.$axios.get('/api/v1/workbooks', {params})
        .then(res => {
          //
          console.log('FETCH_WORKBOOKS_ALL(total_results): res - ', res);
          params.limit = res.data.total_results;

          console.log('FETCH_WORKBOOKS_ALL(results): params - ', params);
          return window.$axios.get('/api/v1/workbooks', {params});
        })
        .then(res => {
          console.log('FETCH_WORKBOOKS_ALL(results): res - ', res);
          return res.data;
        });
    },
    FETCH_WORKBOOK(context, workbook_id) {
      const url = `/api/v1/workbooks/${workbook_id}`;

      //
      console.log('FETCH_WORKBOOK: url - ', url);
      return window.$axios.get(url)
        .then(res => {
          console.log('FETCH_WORKBOOK: res - ', res);
          return res.data;
        });
    },
    CREATE_WORKBOOK(context, dto) {
      //
      console.log('CREATE_WORKBOOK: data - ', dto);
      return window.$axios.post('/api/v1/workbooks', dto)
        .then(res => {
          console.log('CREATE_WORKBOOK: res - ', res);
          return res.data;
        });
    },
    UPDATE_WORKBOOK(context, {workbook_id, dto}) {
      const url = `/api/v1/workbooks/${workbook_id}`;

      //
      console.log('UPDATE_WORKBOOK: data - ', dto);
      return window.$axios.patch(url, dto)
        .then(res => {
          console.log('UPDATE_WORKBOOK: res - ', res);
          return res.data;
        });
    },
    DELETE_WORKBOOK(context, workbook_id) {
      const url = `/api/v1/workbooks/${workbook_id}`;

      //
      console.log('DELETE_WORKBOOK: url - ', url);
      return window.$axios.delete(url)
        .then(res => {
          console.log('DELETE_WORKBOOK: res - ', res);
          return res.data;
        });
    },

    FETCH_PAGES(context, {workbook_id, labeled, sort_by, page}) {
      const params = {
        workbook_id: (typeof(workbook_id) !== 'undefined') ? workbook_id : null,
        labeled: (typeof(labeled) !== 'undefined') ? labeled : null,
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0)) ? ((page - 1) * _DEFAULT_LIMIT) : 0,
        limit: _DEFAULT_LIMIT,
      };

      //
      console.log('FETCH_PAGES: params - ', params);
      return window.$axios.get('/api/v1/pages', {params})
        .then(res => {
          console.log('FETCH_PAGES: res - ', res);

          const response = res.data;
          const filter = new URLSearchParams(response.filtering);

          labeled = parseInt(filter.get('labeled'));
          if(!Number.isInteger(labeled)) {
            labeled = null;
          }

          return {
            filter: {labeled},
            // search: "",
            sort_by: response.sort_by || '',
            pagination: {
              value: Math.floor(response.offset / _DEFAULT_LIMIT) + 1,    // value는 1부터 시작함.
              length: Math.ceil(response.total_results / _DEFAULT_LIMIT),
            },
            pages: response.results
          };
        });
    },
    FETCH_PAGES_ALL(context) {
      let params = { offset: 0, limit: 0 };

      //
      console.log('FETCH_PAGES_ALL(total_results): params - ', params);
      return window.$axios.get('/api/v1/pages', {params})
        .then(res => {
          //
          console.log('FETCH_PAGES_ALL(total_results): res - ', res);
          params.limit = res.data.total_results;

          console.log('FETCH_PAGES_ALL(results): params - ', params);
          return window.$axios.get('/api/v1/pages', {params});
        })
        .then(res => {
          console.log('FETCH_PAGES_ALL(results): res - ', res);
          return res.data;
        });
    },
    FETCH_PAGE_COUNT(context, {workbook_id, labeled}) {
      const params = {
        workbook_id: (typeof(workbook_id) !== 'undefined') ? workbook_id : null,
        labeled: (typeof(labeled) !== 'undefined') ? labeled : null,
      };

      //
      console.log('FETCH_PAGE_COUNT: params - ', params);
      return window.$axios.get('/api/v1/pages/count', {params})
        .then(res => {
          console.log('FETCH_PAGE_COUNT: res - ', res);
          return res.data.count;
        });
    },
    FETCH_PAGE(context, page_id) {
      const url = `/api/v1/pages/${page_id}`;

      //
      console.log('FETCH_PAGE: url - ', url);
      return window.$axios.get(url)
        .then(res => {
          console.log('FETCH_PAGE: res - ', res);
          return res.data;
        });
    },
    CREATE_PAGE(context, dto) {
      //
      console.log('CREATE_PAGE: data - ', dto);
      return window.$axios.post('/api/v1/pages', dto)
        .then(res => {
          console.log('CREATE_PAGE: res - ', res);
          return res.data;
        });
    },
    UPDATE_PAGE(context, {page_id, dto}) {
      const url = `/api/v1/pages/${page_id}`;

      //
      console.log('UPDATE_PAGE: data - ', dto);
      return window.$axios.patch(url, dto)
        .then(res => {
          console.log('UPDATE_PAGE: res - ', res);
          return res.data;
        });
    },
    DELETE_PAGE(context, page_id) {
      const url = `/api/v1/pages/${page_id}`;

      //
      console.log('DELETE_PAGE: url - ', url);
      return window.$axios.delete(url)
        .then(res => {
          console.log('DELETE_PAGE: res - ', res);
          return res.data;
        });
    },

    DETECT_AND_RECOGNIZE(context, {input_url, log = 1, user_id = 'admin'}) {
      const dto = {input_url, log, user_id};

      //
      console.log('DETECT_AND_RECOGNIZE: data - ', dto);
      return window.$axios.post('/api/v1/infer/dnr', dto)
        .then(res => {
          console.log('DETECT_AND_RECOGNIZE: res - ', res);
          return res.data;
        });
    },
    SCORE(context, {page_id, predictions, log_id = null}) {
      const dto = {page_id, predictions, log_id};

      //
      console.log('SCORE: data - ', dto);
      return window.$axios.post('/api/v1/infer/score', dto)
        .then(res => {
          console.log('SCORE: res - ', res);
          return res.data;
        });
    },
    FETCH_LOGS(context, {success, workbook_id, page_id, sort_by, page}) {
      const params = {
        success: (typeof(success) !== 'undefined') ? success : null,
        workbook_id: (typeof(workbook_id) !== 'undefined') ? workbook_id : null,
        page_id: (typeof(page_id) !== 'undefined') ? page_id : null,
        sort_by: (typeof(sort_by) !== 'undefined') ? sort_by : null,
        offset: ((typeof(page) === 'number') && (page > 0)) ? ((page - 1) * _DEFAULT_LIMIT) : 0,
        limit: _DEFAULT_LIMIT,
      };

      //
      console.log('FETCH_LOGS: params - ', params);
      return window.$axios.get('/api/v1/logs', {params})
        .then(res => {
          console.log('FETCH_LOGS: res - ', res);

          const response = res.data;
          const filter = new URLSearchParams(response.filtering);

          success = parseInt(filter.get('success'));
          if(!Number.isInteger(success)) {
            success = null;
          }
          workbook_id = filter.get('workbook_id') || null;
          page_id = filter.get('page_id') || null;

          return {
            filter: {success, workbook_id, page_id},
            // search: "",
            sort_by: response.sort_by || '',
            pagination: {
              value: Math.floor(response.offset / _DEFAULT_LIMIT) + 1,    // value는 1부터 시작함.
              length: Math.ceil(response.total_results / _DEFAULT_LIMIT),
            },
            logs: response.results
          };
        });
    },

    FETCH_VERSIONS(context) {
      const url = `/api/v1/version`;

      //
      console.log('FETCH_VERSIONS: url - ', url);
      return window.$axios.get(url)
        .then(res => {
          console.log('FETCH_VERSIONS: res - ', res);
          return res.data;
        });
    },
    REINDEX(context) {
      const url = `/api/v1/pages/reindex`;

      //
      console.log('REINDEX: url - ', url);
      return window.$axios.post(url)
        .then(res => {
          console.log('REINDEX: res - ', res);
          return res.data;
        });
    },
  },
  modules: {
  }
});
