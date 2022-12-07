<template>
  <v-card class="pa-4">
    <v-tabs v-model="tabs.current" @change="changeTab">
      <v-tab v-for="tab in tabs.list" :key="tab.value">
        {{ tab.text }}
      </v-tab>

      <!-- 검출 및 인식 -->
      <v-tab-item>
        <v-spacer class="ma-2" />
        <v-card flat>
          <v-card-actions>
            <v-file-input label="손글씨 이미지" accept="image/*" @change="(file) => this.initDnR(file)" />
            <v-btn color="primary" class="ml-8" :disabled="!dnr.local_file" :loading="dnr.loading" @click="doDnR">검출/인식</v-btn>
          </v-card-actions>
          <v-divider class="ml-2 mr-2" v-if="dnr.input_url" />
          <v-container row>
            <v-card flat max-width="320" v-if="dnr.input_url">
              <v-card-title>입력 이미지</v-card-title>
              <v-card-text>
                <v-img contain :src="resolveUrl(dnr.input_url)" />
              </v-card-text>
            </v-card>
            <div class="ma-2" />
            <v-card flat max-width="320" v-if="dnr.response">
              <v-card-title>검출 결과</v-card-title>
              <v-card-text v-if="!dnr.response.success">실패</v-card-text>
              <v-img v-if="dnr.response.success" contain :src="resolveUrl(dnr.response.boxed_url)" />
            </v-card>
            <div class="ma-2" />
            <v-card flat min-width="320" v-if="dnr.response && dnr.response.success">
              <v-card-title>인식 결과</v-card-title>
              <v-list>
                <v-list-item two-line>
                  <v-list-item-avatar tile>
                    <v-img position="top" :src="resolveUrl(dnr.response.workbook.image_url)" />
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>{{ dnr.response.workbook.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ dnr.response.workbook.description }}&nbsp;</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item two-line>
                  <v-list-item-avatar tile>
                    <v-img position="top" :src="resolveUrl(dnr.response.page.original_url)" />
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>{{ dnr.response.page.page_num }}</v-list-item-title>
                    <v-list-item-subtitle>{{ dnr.response.page.description }}&nbsp;</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-for="prediction in dnr.response.predictions" :key="prediction.prob_num">
                  <v-list-item-avatar>
                    <v-chip>{{ prediction.prob_num }}</v-chip>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>{{ prediction.answers.join(', ') }}&nbsp;</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-container>

          <v-card-actions v-if="dnr.response && dnr.response.success">
            <v-spacer />
            <v-btn color="primary" @click="goToScore">채점하기</v-btn>
          </v-card-actions>
        </v-card>
      </v-tab-item>

      <!-- 채점 -->
      <v-tab-item>
        <v-spacer class="ma-2" />
        <v-card>
          <v-container row>
            <v-card flat width="480">
              <v-card-text>
                <v-select
                  label="문제집"
                  :disabled="scoring.workbooks.length == 0"
                  :items="scoring.workbooks"
                  :value="scoring.selectedWorkbookId"
                  @change="selectWorkbook"
                />
                <v-select
                  label="페이지"
                  :disabled="scoring.pages.length == 0"
                  :items="scoring.pages"
                  :value="scoring.selectedPageId"
                  @change="selectPage"
                />
              </v-card-text>
              <v-card-subtitle v-if="scoring.predictions.length">학생 답</v-card-subtitle>
              <v-expansion-panels flat accordion multiple :value="scoring.predictions.map((v, i) => i)">
                <v-expansion-panel v-for="(prediction, p_idx) in scoring.predictions" :key="prediction.prob_num">
                  <v-expansion-panel-header>{{prediction.prob_num}} 번</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-text-field filled
                      v-for="(answer, a_idx) in prediction.answers" :key="a_idx"
                      :value= "answer"
                      @change="(value) => changeAnswer(p_idx, a_idx, value)"
                    >
                      <template v-slot:label>
                        <v-chip color="secondary" x-small>{{a_idx + 1}}</v-chip>
                      </template>
                    </v-text-field>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
              <v-card-actions v-if="scoring.predictions.length">
                <v-spacer />
                <v-btn color="primary" @click="doScore">채점하기</v-btn>
              </v-card-actions>
              <div v-if="scoring.response">
                <v-card-title>채점 결과</v-card-title>
                <v-list>
                  <v-list-item v-for="result in scoring.response" :key="result.prob_num">
                    <v-list-item-content>
                      <v-list-item-title>{{result.prob_num}}번: {{ result.correct ? "정답" : "오답" }}</v-list-item-title>
                    </v-list-item-content>
                    <v-tooltip top>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn small outlined v-bind="attrs" v-on="on">해설 보기</v-btn>
                      </template>
                      <span>
                        <v-img eager max-width="320" :src="resolveUrl(result.solving_url)" />
                      </span>
                    </v-tooltip>
                    <div class="ma-2" />
                    <v-tooltip top>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn small outlined v-bind="attrs" v-on="on">유사문제 보기</v-btn>
                      </template>
                      <span>
                        <v-img eager max-width="320" :src="resolveUrl(result.similar_url)" />
                      </span>
                    </v-tooltip>
                  </v-list-item>
                </v-list>
              </div>
            </v-card>
            <div class="ma-2" />
            <v-card flat max-width="640">
              <v-img :src="resolveUrl(scoring.selectedPage && scoring.selectedPage.original_url)" />
            </v-card>
          </v-container>
        </v-card>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiTestView',

  data() {
    return {
      //
      initWorkbooks: [],
      initPages: [],

      //
      tabs: {
        current: null,
        list: [
          {value: '0', text: '검출 및 인식'},
          {value: '1', text: '채점'},
        ]
      },

      //
      dnr: {
        local_file: null,
        loading: false,
        input_url: null,
        response: null
      },

      //
      scoring: {
        workbooks: [],
        pages: [],

        selectedWorkbookId: null,
        selectedPageId: null,
        selectedPage: null,
        selectedLogId: null,

        predictions: [],
        response: []
      },
    };
  },

  mounted() {
    //
    Promise.all([
      this.$store.dispatch('FETCH_WORKBOOKS_ALL'),
      this.$store.dispatch('FETCH_PAGES_ALL')
    ]).then(([resWorkbooks, resPages]) => {
      //
      this.initWorkbooks = resWorkbooks.results;
      this.initPages = resPages.results;

      //
      this.scoring.workbooks = this.initWorkbooks.map((workbook) => {
        return {value: workbook._id, text: workbook.name};
      });

      //
      if (this.initWorkbooks.length) {
        const [workbook, ] = this.initWorkbooks;

        this.selectWorkbook(workbook._id);
      }
    })
    .catch(() => {
      this.$eventBus.$emitModal('문제집 목록을 가져올 수 없습니다.');
    });
  },

  methods: {
    resolveUrl: (image_url) => resolveImageUrl(image_url),

    //
    changeTab(value) {
      this.tabs.current = value;
    },

    //
    initDnR(local_file = null) {
      this.dnr = {
        local_file,
        loading: false,
        input_url: null,
        response: null,
      };
    },
    doDnR() {
      this.dnr.loading = true;
      this.dnr.input_url = null;
      this.dnr.response = null;

      this.$store.dispatch('UPLOAD_IMAGES', this.dnr.local_file)
        .then(({paths}) => {
          if (!Array.isArray(paths) || paths.length < 1) {
            this.$eventBus.$emitSnackbar('이미지를 업로드 할 수 없습니다.');
            return;
          }

          const [input_url, ] = paths;
          this.dnr.input_url = input_url;

          return this.$store.dispatch('DETECT_AND_RECOGNIZE', {input_url});
        })
        .then((res) => {
          this.dnr.response = res;
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('검출/인식 작업을 수행할 수 없습니다.');
        })
        .finally(() => {
          this.dnr.loading = false;
        });
    },
    goToScore() {
      //
      const res = this.dnr.response;
      this.selectWorkbook(res.workbook._id, res.page._id);
      this.scoring.predictions = res.predictions.map((prediction) => {
        return {prob_num: prediction.prob_num, answers: prediction.answers};
      });
      this.scoring.selectedLogId = res.log_id;
      this.scoring.response = null;

      //
      this.tabs.current = 1;
    },

    //
    selectWorkbook(workbook_id, page_id = null) {
      //
      this.scoring.selectedWorkbookId = workbook_id;

      //
      this.scoring.pages = this.initPages.filter((page) => {
          return page.workbook_id === workbook_id;
        }).map((page) => {
          return {value: page._id, text: page.page_num};
        });

      //
      if (page_id == null) {
        if (this.scoring.pages.length) {
          page_id = this.scoring.pages[0].value;
        }
      }
      this.selectPage(page_id);

    },
    selectPage(page_id) {
      //
      this.scoring.selectedPageId = page_id;
      this.scoring.selectedPage = this.initPages.find((page) => {
        return page._id == page_id;
      }) || null;

      //
      const problems = (this.scoring.selectedPage ? this.scoring.selectedPage.problems : []);
      this.scoring.predictions = problems.map((problem) => {
        const labels = problem.labels || [];
        return {
          prob_num: problem.prob_num,
          answers: labels.map(() => '')
        };
      });

      //
      this.scoring.selectedLogId = null;
      this.scoring.response = null;
    },
    changeAnswer(p_idx, a_idx, value) {
      if (p_idx < this.scoring.predictions.length) {
        const problem = this.scoring.predictions[p_idx];

        if (a_idx < problem.answers.length) {
          problem.answers[a_idx] = value;
        }
      }
    },
    doScore() {
      const page_id = this.scoring.selectedPageId;
      const predictions = this.scoring.predictions;
      const log_id = this.scoring.selectedLogId;

      this.$store.dispatch('SCORE', {page_id, predictions, log_id})
        .then((res) => {
          this.scoring.response = res;
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('채점 작업을 수행할 수 없습니다.');
        });
    },
  },
};
</script>

<style scoped>

</style>