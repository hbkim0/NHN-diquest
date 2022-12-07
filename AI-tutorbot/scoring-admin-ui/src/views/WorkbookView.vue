<template>
  <v-card class="pa-4">
    <v-dialog persistent width="500" v-model="createDialog.show">
      <v-card>
        <v-card-title>문제집 생성</v-card-title>
        <v-card-text>
          <v-form
            ref="form"
            v-model="createDialog.valid"
          >
            <v-text-field
              label="이름"
              required
              :rules="[v => ((!!v) && (String(v) && !!(v.trimEnd()))) || 'required']"
              :value="createDialog.name"
              @change="(value) => changCreateDialogValue('name', value)"
            />
            <v-textarea label="설명" :value="createDialog.description" @change="(value) => changCreateDialogValue('description', value)"/>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeCreateDialog">취소</v-btn>
          <v-btn :disabled="!createDialog.valid" color="primary" @click="createWorkbook">생성</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog persistent width="500" scrollable v-model="applyDialog.show">
      <v-card>
        <v-card-title>문제집 반영</v-card-title>
        <v-card-subtitle>자동채점에 반영 할 문제집을 선택해 주세요.</v-card-subtitle>
        <v-card-text>
          <v-switch
            inset hide-details color="primary"
            false-value="0" true-value="1"

            v-for="workbook in applyDialog.workbooks"
            :key="workbook._id"
            :disabled="workbook.disabled"
            :loading="workbook.loading"
            :label="workbook.name"
            v-model="workbook.applied"
            @change="(value) => changeApply(workbook, value)"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeApplyDialog">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-card-actions>
      <v-select
        class="ma-1" style="max-width:240px" clearable
        label="상태"
        :items="workbookFilters.applied"
        :value="workbookList.filter.applied"
        @change="changeFilterApplied"
      />
      <v-text-field
        v-if="false"
        class="ma-1" style="max-width:320px"
        append-outer-icon="mdi-magnify" clearable disabled
        label="검색"
      />
      <v-spacer />
      <v-btn color="primary" @click="() => {createDialog.show = true}">새 문제집</v-btn>
      <v-btn color="primary" @click="showApplyDialog">반영하기</v-btn>
    </v-card-actions>
    <v-card-text v-if="!(workbookList.workbooks.length)">
      <p class="text-center">
        {{$vuetify.lang.t('$vuetify.noDataText')}}
      </p>
    </v-card-text>
    <v-card-text v-else>
      <v-container row>
        <v-card
          width="640" class="ma-2" hover
          v-for="workbook in workbookList.workbooks"
          :key="workbook._id"
          :to="{name: 'WorkbookDetailView', params: {workbook_id: workbook._id}}"
        >
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title>
                <v-icon v-if="workbook.applied">mdi-checkbox-multiple-marked-circle-outline</v-icon>
                {{ workbook.name }}
              </v-card-title>
              <v-card-subtitle>
                {{ workbook.description }}
              </v-card-subtitle>
            </div>
            <v-avatar class="ma-3" size="192" tile>
              <v-img contain :src="resolveUrl(workbook.image_url)" />
            </v-avatar>
          </div>
        </v-card>
      </v-container>
    </v-card-text>
    <v-card-text v-if="workbookList.pagination.length">
      <v-pagination
        :value="workbookList.pagination.value"
        :length="workbookList.pagination.length"
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
  name: 'ScoringAdminUiWorkbookView',

  data() {
    return {
      createDialog: {
        show: false,
        valid: null,
        name: '',
        description: '',
      },
      applyDialog: {
        show: false,
        workbooks: [],
        changed: false,
      },
      appliedList: [
        {text: '전체', value: null},
        {text: '반영', value: 1},
        {text: '미반영', value: 0},
      ],

      //
      workbookFilters: {
        applied: [
          {text: '반영', value: 1},
          {text: '미반영', value: 0},
        ],
      },
      workbookList: {
        filter: {
          applied: null,
        },
        // search: "",
        // sort_by: '',
        pagination: {value: 1, length: 0,},
        workbooks: [],
      }
    };
  },

  mounted() {
    this.$store.dispatch('FETCH_WORKBOOKS', {})
      .then((workbookList) => {
        this.workbookList = workbookList;
      })
      .catch(() => {
        this.$eventBus.$emitModal('문제집 목록을 가져올 수 없습니다.');
      });
  },

  methods: {
    resolveUrl: (image_url) => resolveImageUrl(image_url),

    //
    changCreateDialogValue(key, value) {
      this.createDialog[key] = value;
    },
    closeCreateDialog() {

      //
      this.$refs.form.reset();

      //
      this.createDialog.show = false;
    },
    createWorkbook() {
      const dto = {
        name: this.createDialog.name.trim(),
        description: this.createDialog.description.trim(),
      };

      this.$store.dispatch('CREATE_WORKBOOK', dto)
        .then((workbook) => {
          this.$router.push({name: 'WorkbookEditView', params: {workbook_id: workbook._id}});
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('문제집 생성을 할 수 없습니다.');
        })
        .finally(() => {
          this.closeCreateDialog();
        });
    },

    //
    closeApplyDialog() {
      //
      if (this.applyDialog.changed) {
        const params = {
          applied: this.workbookList.filter.applied,
          page: this.workbookList.pagination.value,
        };

        this.fetchWorkbooks(params);
      }

      //
      this.applyDialog = {show: false, workbooks: [], changed: false};
    },
    showApplyDialog() {
      this.$store.dispatch('FETCH_WORKBOOKS_ALL', {})
        .then((res) => {
          this.applyDialog.workbooks = res.results.map(
            ({_id, name, applied, valid}) => ({_id, name, disabled: (valid !== 1), applied: (applied === 1 ? '1' : '0'), loading: false})
          );
          this.applyDialog.show = true;
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('문제집 목록을 가져올 수 없습니다.');
        });
    },
    changeApply(workbook, value) {
      workbook.loading = true;
      this.$store.dispatch('UPDATE_WORKBOOK', {workbook_id: workbook._id, dto: {applied: (value === '1' ? 1 : 0)}})
        .then((res) => {
          this.applyDialog.changed = true;

          workbook.applied = (res.applied === 1 ? '1' : '0');
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('문제집을 적용 할 수 없습니다.');

          workbook.applied = (value === '1' ? '0' : '1');
        })
        .finally(() => {
          workbook.loading = false;
        });
    },

    //
    fetchWorkbooks(params) {
      return this.$store.dispatch('FETCH_WORKBOOKS', params)
        .then((workbookList) => {
          this.workbookList = workbookList;
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('문제집 목록을 가져올 수 없습니다.');
        });
    },
    changeFilterApplied(applied) {
      const params = {
        applied,
        page: 1,
      };

      this.workbookList.filter.applied = applied;
      this.fetchWorkbooks(params);
    },

    //
    movePage(number) {
      const params = {
        applied: this.workbookList.filter.applied,
        page: number,
      };

      this.fetchWorkbooks(params);
    },
    nextPage() {
      const params = {
        applied: this.workbookList.filter.applied,
        page: this.workbookList.pagination.value + 1,
      };

      this.fetchWorkbooks(params);
    },
    prevPage() {
      const params = {
        applied: this.workbookList.filter.applied,
        page: this.workbookList.pagination.value - 1,
      };

      this.fetchWorkbooks(params);
    },
  },
};
</script>

<style scoped>

</style>