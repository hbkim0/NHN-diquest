<template>
  <div>
    <v-card class="pa-4">
      <v-dialog persistent width="500" v-model="deleteWorkbookDialog.show">
        <v-card>
          <v-card-title>문제집 삭제</v-card-title>
          <v-card-text>
            <p>문제집에 포함되어 있는 모든 페이지들도 함께 삭제 됩니다.</p>
            <p>그래도 계속 진행하시겠습니까?</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="closeDeleteWorkbookDialog">취소</v-btn>
            <v-btn color="error" @click="deleteWorkbook">삭제</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-container row>
        <v-avatar size="240" tile>
          <v-img contain :src="resolveUrl(workbook.image_url)" />
        </v-avatar>
        <div>
          <v-card-title> {{ workbook.name }} </v-card-title>
          <v-card-subtitle > {{ workbook.description }} </v-card-subtitle>
          <v-card-text />
          <v-card-text v-if="workbook.applied === 1">
            <v-icon>mdi-checkbox-multiple-marked-circle-outline</v-icon>
            자동 채점에 반영
          </v-card-text>
          <v-card-text v-else-if="workbook.applied === 0">
            자동 채점에 미반영
          </v-card-text>
        </div>
      </v-container>
      <v-card-actions v-if="workbook.applied === 0">
        <v-spacer />
        <v-btn :to="{name: 'WorkbookEditView', params: {workbook_id}}">수정</v-btn>
        <v-btn color="warning" @click="() => {deleteWorkbookDialog.show = true}">삭제</v-btn>
      </v-card-actions>
    </v-card>

    <v-spacer class="ma-6" />

    <v-card class="pa-4">
      <v-dialog persistent width="500" v-model="createPageDialog.show">
        <v-card>
          <v-card-title>페이지 생성</v-card-title>
          <v-card-text>
            <v-form
              ref="form"
              v-model="createPageDialog.valid"
            >
              <v-text-field
                label="이름"
                required
                :rules="[v => ((!!v) && (String(v) && !!(v.trimEnd()))) || 'required']"
                :value="createPageDialog.page_num"
                @change="(value) => changCreatePageDialogValue('page_num', value)"
              />
              <v-textarea label="설명" :value="createPageDialog.description" @change="(value) => changCreatePageDialogValue('description', value)"/>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="closeCreatePageDialog">취소</v-btn>
            <v-btn :disabled="!createPageDialog.valid" color="primary" @click="createPage">생성</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog persistent width="500" v-model="deletePageDialog.show">
        <v-card>
          <v-card-title>페이지 삭제</v-card-title>
          <v-card-text>
            <p>이미지와 라벨링 데이터 모두가 삭제 됩니다.</p>
            <p>그래도 계속 진행하시겠습니까?</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="closeDeletePageDialog">취소</v-btn>
            <v-btn color="error" @click="deletePage">삭제</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-card-title>
        페이지 목록
      </v-card-title>
      <v-card-subtitle>
        페이지 수: {{pageCount.labeled}} (라벨링) / {{pageCount.total}} (전체)
      </v-card-subtitle>
      <v-card-actions>
        <v-select
          class="ma-1" style="max-width:240px" clearable
          label="라벨링 여부"
          :items="pageFilters.labeled"
          :value="pageList.filter.labeled"
          @change="changeFilterLabeled"
        />
        <v-select
          class="ma-1" style="max-width:240px" clearable
          label="정렬"
          :items="pageSortBy"
          :value="pageList.sort_by"
          @change="changeSortBy"
        />
        <v-spacer />
        <v-btn
          color="primary"
          @click="() => {createPageDialog.show = true}"
          v-if="!(workbook.applied)"
        >
          새 페이지
        </v-btn>
      </v-card-actions>
      <v-card-text v-if="!(pageList.pages.length)">
        <p class="text-center">
          {{$vuetify.lang.t('$vuetify.noDataText')}}
        </p>
      </v-card-text>
      <v-card-text v-else>
        <v-container row>
          <v-card
            class="ma-4"
            v-for="page in this.pageList.pages"
            :key="page._id"
          >
            <v-card-text>
              <v-avatar tile width="248" height="320">
                <v-img contain :src="resolveUrl(page.original_url)" />
              </v-avatar>
            </v-card-text>
            <v-card-title>{{page.page_num}}</v-card-title>
            <v-card-subtitle>{{page.description}}&nbsp;</v-card-subtitle>
            <v-divider />
            <v-card-actions>
              <v-icon v-if="page.labeled">mdi-checkbox-multiple-marked-circle-outline</v-icon>
              <v-spacer />
              <v-btn
                icon
                :to="{name: 'PageEditView', params: {workbook_id, page_id: page._id}}"
                v-if="!(workbook.applied)"
              >
                <v-icon>mdi-square-edit-outline</v-icon>
              </v-btn>
              <v-btn
                icon
                @click="() => showDeletePageDialog(page._id)"
                v-if="!(workbook.applied)"
              >
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>
              <v-btn
                icon
                :to="{name: 'PageDetailView', params: {workbook_id, page_id: page._id}}"
                v-if="!!(workbook.applied)"
              >
                <v-icon>mdi-magnify-expand</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-container>
      </v-card-text>
      <v-card-text v-if="pageList.pagination.length">
        <v-pagination
          :value="pageList.pagination.value"
          :length="pageList.pagination.length"
          :total-visible="10"
          @input="movePage"
          @next="nextPage"
          @previous="prevPage"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiWorkbookDetailView',

  data() {
    return {
      deleteWorkbookDialog: {
        show: false
      },
      workbook_id: '',
      workbook: {
        name: '',
        description: '',
        image_url: '',
        applied: null,
      },

      //
      createPageDialog: {
        show: false,
        valid: null,
        page_num: '',
        description: '',
      },
      deletePageDialog: {
        show: false,
        page_id: '',
      },

      //
      pageFilters: {
        labeled: [
          {text: '라벨링 됨', value: 1},
          {text: '라벨링 안됨', value: 0},
        ]
      },
      pageSortBy: [
        {text: '이름↑', value: 'page_num'},
        {text: '이름↓', value: '-page_num'},
      ],
      pageCount: {
        labeled: 0,
        total: 0,
      },
      pageList: {
        filter: {labeled: null},
        // search: "",
        sort_by: '',
        pagination: {value: 1, length: 0,},
        pages: []
      },
    };
  },

  mounted() {
    this.workbook_id = this.$route.params.workbook_id;

    Promise.all([
      this.$store.dispatch('FETCH_WORKBOOK', this.workbook_id),
      this.$store.dispatch('FETCH_PAGE_COUNT', {workbook_id: this.workbook_id, labeled: 1}),
      this.$store.dispatch('FETCH_PAGE_COUNT', {workbook_id: this.workbook_id}),
      this.$store.dispatch('FETCH_PAGES', {workbook_id: this.workbook_id}),
    ]).then(([workbook, labeledCount, totalCount, pageList]) => {
      //
      this.workbook.name = workbook.name;
      this.workbook.description = workbook.description;
      this.workbook.image_url = workbook.image_url;
      this.workbook.applied = workbook.applied;

      //
      this.pageCount.labeled = labeledCount;
      this.pageCount.total = totalCount;

      //
      this.pageList = pageList;
    }).catch(() => {
      this.$eventBus.$emitHomeModal('문제집 정보을 가져올 수 없습니다.');
    });
  },

  methods: {
    resolveUrl: (image_url) => resolveImageUrl(image_url),

    closeDeleteWorkbookDialog() {
      this.deleteWorkbookDialog.show = false;
    },
    deleteWorkbook() {
      this.$store.dispatch('DELETE_WORKBOOK', this.workbook_id)
        .then(() => {
          this.closeDeleteWorkbookDialog();
          this.$router.back();
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('문제집을 삭제 할 수 없습니다.');
        });
    },

    //
    changCreatePageDialogValue(key, value) {
      this.createPageDialog[key] = value;
    },
    closeCreatePageDialog() {

      //
      this.$refs.form.reset();

      //
      this.createPageDialog.show = false;
    },
    createPage() {
      let dto = {
        workbook_id: this.workbook_id,
        page_num: this.createPageDialog.page_num.trim(),
        description: this.createPageDialog.description.trim(),
      };

      this.$store.dispatch('CREATE_PAGE', dto)
        .then((page) => {
          this.$router.push({name: 'PageEditView', params: {workbook_id: this.workbook_id, page_id: page._id}});

          //
          this.closeCreatePageDialog();
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('페이지 생성을 할 수 없습니다.');
        });
    },
    showDeletePageDialog(page_id) {
      this.deletePageDialog.page_id = page_id;
      this.deletePageDialog.show = true;
    },
    closeDeletePageDialog() {
      this.deletePageDialog.show = false;
      this.deletePageDialog.page_id = '';
    },
    deletePage() {
      this.$store.dispatch('DELETE_PAGE', this.deletePageDialog.page_id)
        .then(() => {
          const params = {
            workbook_id: this.workbook_id,
            labeled: this.pageList.filter.labeled,
            sort_by: this.pageList.sort_by,
            page: ((this.pageList.pages.length > 1) ?
                    (this.pageList.pagination.value) :
                    (this.pageList.pagination.value - 1)
                  ),
          };

          return Promise.all([
            this.fetchPageCounts(),
            this.fetchPages(params)
          ]);
        })
        .then(() => {
          this.closeDeletePageDialog();
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('페이지를 삭제 할 수 없습니다.');
        });
    },

    //
    fetchPageCounts() {
      return Promise.all([
        this.$store.dispatch('FETCH_PAGE_COUNT', {workbook_id: this.workbook_id, labeled: 1}),
        this.$store.dispatch('FETCH_PAGE_COUNT', {workbook_id: this.workbook_id}),
      ]).then(([labeledCount, totalCount]) => {
        //
        this.pageCount.labeled = labeledCount;
        this.pageCount.total = totalCount;
      })
      .catch(() => {
        this.$eventBus.$emitSnackbar('페이지 목록을 가져올 수 없습니다.');
      });
    },
    fetchPages(params) {
      return this.$store.dispatch('FETCH_PAGES', params)
        .then((pageList) => {
          this.pageList = pageList;
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('페이지 목록을 가져올 수 없습니다.');
        });
    },
    changeFilterLabeled(labeled) {
      const params = {
        workbook_id: this.workbook_id,
        labeled: labeled,
        sort_by: this.pageList.sort_by,
        page: 1,
      };

      this.pageList.filter.labeled = labeled;
      this.fetchPages(params);
    },
    changeSortBy(sort_by) {
      const params = {
        workbook_id: this.workbook_id,
        labeled: this.pageList.filter.labeled,
        sort_by: sort_by,
        page: 1,
      };

      this.pageList.sort_by = sort_by;
      this.fetchPages(params);
    },
    movePage(number) {
      const params = {
        workbook_id: this.workbook_id,
        labeled: this.pageList.filter.labeled,
        sort_by: this.pageList.sort_by,
        page: number,
      };

      this.fetchPages(params);
    },
    nextPage() {
      const params = {
        workbook_id: this.workbook_id,
        labeled: this.pageList.filter.labeled,
        sort_by: this.pageList.sort_by,
        page: this.pageList.pagination.value + 1,
      };

      this.fetchPages(params);
    },
    prevPage() {
      const params = {
        workbook_id: this.workbook_id,
        labeled: this.pageList.filter.labeled,
        sort_by: this.pageList.sort_by,
        page: this.pageList.pagination.value - 1,
      };

      this.fetchPages(params);
    },
  },
};
</script>

<style scoped>

</style>