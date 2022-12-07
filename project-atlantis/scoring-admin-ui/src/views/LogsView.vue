<template>
  <v-card class="pa-4">
    <v-card-actions>
      <v-select
        class="ma-1" style="max-width:240px" clearable
        label="검출/인식 결과"
        :items="logFilters.successes"
        :value="logList.filter.success"
        @change="changeFilterSuccess"
      />
      <v-select
        class="ma-1" style="max-width:240px" clearable
        label="문제집"
        :items="logFilters.workbooks"
        :value="logList.filter.workbook_id"
        @change="changeFilterWorkbook"
      />
      <v-select
        class="ma-1" style="max-width:240px" clearable
        label="페이지"
        :items="logFilters.pages"
        :value="logList.filter.page_id"
        @change="changeFilterPage"
      />
    </v-card-actions>
    <v-card-text>
      <v-data-table
        hide-default-footer

        show-expand
        single-expand
        :expanded.sync="expanded"

        :loading="logListLoading"

        :headers="logHeaders"
        :items="logList.logs"
        item-key="_id"
      >
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <v-container row>
              <v-card flat class="ma-1" width="200">
                <v-card-text>
                  <v-img :src="resolveUrl(item.input_url)" />
                </v-card-text>
              </v-card>
              <v-divider vertical v-if="item.scoring && item.scoring.length" />
              <v-card flat class="ma-1" width="200">
                <v-card-text>
                  <v-img :src="resolveUrl(item.boxed_url)" />
                </v-card-text>
              </v-card>
              <v-card flat class="ma-1" width="200" v-if="item.scoring && item.scoring.length">
                <v-card-subtitle><b>인식결과</b></v-card-subtitle>
                <v-card-text>
                  <p v-for="score in item.scoring" :key="score.prob_num">
                    {{ score.prob_num }}번: {{ score.answers.join(', ') }}
                  </p>
                </v-card-text>
              </v-card>
              <v-divider vertical v-if="item.scoring && item.scoring.length" />
              <v-card flat class="ma-1" width="200" v-if="item.scoring && item.scoring.length">
                <v-card-subtitle><b>채점(입력)</b></v-card-subtitle>
                <v-card-text>
                  <p v-for="score in item.scoring" :key="score.prob_num">
                    {{ score.prob_num }}번: {{ Array.isArray(score.custom_answers) ? score.custom_answers.join(', ') : "" }}
                  </p>
                </v-card-text>
              </v-card>
              <v-card flat class="ma-1" width="200" v-if="item.scoring && item.scoring.length">
                <v-card-subtitle><b>채점(결과)</b></v-card-subtitle>
                <v-card-text>
                <p v-for="score in item.scoring" :key="score.prob_num">
                  {{ score.prob_num }}번: {{ ((score.correct === 1) ? "정답": ((score.correct === 0) ? "오답" : "")) }}
                </p>
                </v-card-text>
              </v-card>
            </v-container>
          </td>
        </template>
      </v-data-table>
    </v-card-text>
    <v-card-text>
      <v-pagination
        :value="logList.pagination.value"
        :length="logList.pagination.length"
        :total-visible="10"
        @input="movePage"
        @next="nextPage"
        @previous="prevPage"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiLogsView',

  data() {
    return {
      //
      initWorkbooks: [],
      initPages: [],

      //
      logFilters: {
        successes: [
          {text: '성공', value: 1},
          {text: '실패', value: 0},
        ],
        workbooks: [],
        pages: [],
      },
      expanded: [],
      logHeaders: [
        {text: '결과', value: 'success', sortable: false, filterable: false, groupable: false},
        {text: '문제집', value: 'workbook.name', sortable: false, filterable: false, groupable: false},
        {text: '페이지', value: 'page.page_num', sortable: false, filterable: false, groupable: false},
        {text: '사용자', value: 'user_id', sortable: false, filterable: false, groupable: false},
        {text: '날짜', value: 'reg_date', sortable: false, filterable: false, groupable: false},
      ],
      logListLoading: false,
      logList: {
        filter: {success: null, workbook_id: null, page_id: null},
        // search: "",
        sort_by: '',
        pagination: {value: 1, length: 0,},
        logs: []
      }
    };
  },

  mounted() {

    this.logListLoading = true;
    Promise.all([
      this.$store.dispatch('FETCH_WORKBOOKS_ALL'),
      this.$store.dispatch('FETCH_PAGES_ALL'),
      this.$store.dispatch('FETCH_LOGS', {}),
    ]).then(([resWorkbooks, resPages, logList]) => {
      //
      this.initWorkbooks = resWorkbooks.results;
      this.initPages = resPages.results;
      this.logList = logList;

      //
      this.logList.logs = this.logList.logs.map((log) => {
        return {...log, success: (log.success === 1 ? '성공' : '실패')};
      });

      //
      this.logFilters.workbooks = this.initWorkbooks.map((workbook) => {
        return {text: workbook.name, value: workbook._id};
      });
    })
    .catch(() => {
      this.$eventBus.$emitSnackbar('로그 목록을 가져올 수 없습니다.');
    })
    .finally(() => {
      this.logListLoading = false;
    });
  },

  methods: {
    resolveUrl: (image_url) => resolveImageUrl(image_url),

    fetchLogs(params) {

      this.logListLoading = true;
      return this.$store.dispatch('FETCH_LOGS', params)
        .then((logList) => {
          this.logList = logList;

          //
          this.logList.logs = this.logList.logs.map((log) => {
            return {...log, success: (log.success === 1 ? '성공' : '실패')};
          });

        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('로그 목록을 가져올 수 없습니다.');
        })
        .finally(() => {
          this.logListLoading = false;
        });
    },
    changeFilterSuccess(success) {
      const params = {...this.logList.filter, success, page: 1};

      this.logList.filter.success = success;
      this.fetchLogs(params);
    },
    changeFilterWorkbook(workbook_id) {
      //
      this.logList.filter.page_id = null;
      this.logFilters.pages = this.initPages.filter((page) => {
        return page.workbook_id === workbook_id;
      }).map((page) => {
        return {text: page.page_num, value: page._id};
      });

      //
      const params = {...this.logList.filter, workbook_id, page: 1};

      this.logList.filter.workbook_id = workbook_id;
      this.fetchLogs(params);
    },
    changeFilterPage(page_id) {
      const params = {...this.logList.filter, page_id, page: 1};

      this.logList.filter.page_id = page_id;
      this.fetchLogs(params);
    },
    movePage(number) {
      const params = {...this.logList.filter, page: number};

      this.fetchLogs(params);
    },
    nextPage() {
      const params = {...this.logList.filter, page: this.logList.pagination.value + 1};

      this.fetchLogs(params);
    },
    prevPage() {
      const params = {...this.logList.filter, page: this.logList.pagination.value - 1};

      this.fetchLogs(params);
    },

  },
};
</script>

<style scoped>

</style>