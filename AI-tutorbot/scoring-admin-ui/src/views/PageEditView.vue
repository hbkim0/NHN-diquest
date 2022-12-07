<template>
  <v-card max-width="800" class="pa-4">
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
          label="이름"
          required
          :rules="[v => ((!!v) && (String(v) && !!(v.trimEnd()))) || 'required']"
          :value="editedPage.page_num"
          @change="(value) => changValue('page_num', value)"
        />
        <v-textarea
          label="설명"
          :value="editedPage.description"
          @change="(value) => changValue('description', value)"
        />
        <v-row>
          <v-col>
            <v-file-input label="원본 이미지" accept="image/*" @change="(file) => {this.original_local_file = file}" />
            <v-img contain position="top left" class="ma-2" max-width="320" :src="original_url"/>
          </v-col>
          <v-col>
            <v-file-input label="촬영 이미지" accept="image/*" @change="(file) => {this.sample_local_file = file}" />
            <v-img contain position="top left" class="ma-2" max-width="320" :src="sample_url"/>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="() => this.$router.back()">취소</v-btn>
      <v-btn :disabled="!valid" color="primary" @click="savePage">저장</v-btn>
      <v-btn :disabled="original_url === ''" color="primary" @click="goToLabelingView">라벨링</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiPageEditView',

  data() {
    return {
      valid: null,
      workbook_id: '',
      page_id: '',
      initPage: {},
      editedPage: {
        page_num: '',
        description: '',
        original_url: '',
        sample_url: '',
      },
      original_local_file: null,
      sample_local_file: null
    };
  },

  mounted() {
    //
    this.workbook_id = this.$route.params.workbook_id;
    this.page_id = this.$route.params.page_id;

    //
    Promise.all([
      this.$store.dispatch('FETCH_WORKBOOK', this.workbook_id),
      this.$store.dispatch('FETCH_PAGE', this.page_id),
    ]).then(([workbook, page]) => {

      if (workbook.applied) {
        this.$eventBus.$emitHomeModal('자동채점에 적용된 페이지는 수정할 수 없습니다.');
        return;
      }

      //
      this.initPage.page_num = page.page_num;
      this.initPage.description = page.description;
      this.initPage.original_url = page.original_url;
      this.initPage.sample_url = page.sample_url;

      //
      this.editedPage = window.structuredClone(this.initPage);
    })
    .catch(() => {
      this.$eventBus.$emitHomeModal('페이지 정보을 가져올 수 없습니다.');
    });
  },

  computed: {
    original_url() {
      let original_url = resolveImageUrl(this.editedPage.original_url) || '';
      if(this.original_local_file) {
        original_url = URL.createObjectURL(this.original_local_file);
      }

      return original_url;
    },
    sample_url() {
      let sample_url = resolveImageUrl(this.editedPage.sample_url) || '';
      if(this.sample_local_file) {
        sample_url = URL.createObjectURL(this.sample_local_file);
      }

      return sample_url;
    },
  },

  methods: {
    changValue(key, value) {
      this.editedPage[key] = value;
    },

    async getPageUpdateDto() {
      // TODO: upload-image
      if (this.original_local_file || this.sample_local_file) {
        let files = [];

        if (this.original_local_file) {
          files.push(this.original_local_file);
        }
        if (this.sample_local_file) {
          files.push(this.sample_local_file);
        }

        const res = await this.$store.dispatch('UPLOAD_IMAGES', files);
        let {paths} = res;

        if (!Array.isArray(paths) || paths.length != files.length) {
          this.$eventBus.$emitSnackbar('이미지를 업로드 할 수 없습니다.');
          return;
        }

        let idx = 0;
        if (this.original_local_file) {
          this.editedPage.original_url = paths[idx++];
        }
        if (this.sample_local_file) {
          this.editedPage.sample_url = paths[idx++];
        }
      }

      //
      this.editedPage.page_num = this.editedPage.page_num.trim();
      this.editedPage.description = this.editedPage.description.trim();

      //
      let dto = {};
      if (this.editedPage.page_num !== this.initPage.page_num) {
        dto.page_num = this.editedPage.page_num;
      }
      if (this.editedPage.description !== this.initPage.description) {
        dto.description = this.editedPage.description;
      }
      if (this.editedPage.original_url !== this.initPage.original_url) {
        dto.original_url = this.editedPage.original_url;
      }
      if (this.editedPage.sample_url !== this.initPage.sample_url) {
        dto.sample_url = this.editedPage.sample_url;
      }

      return dto;
    },

    async savePage() {
      const dto = await this.getPageUpdateDto();

      //
      if (Object.keys(dto).length === 0) {
        this.$router.back();
      } else {
        const page_id = this.page_id;

        this.$store.dispatch('UPDATE_PAGE', {page_id, dto})
          .then(() => {
            this.$router.back();
          })
          .catch(() => {
            this.$eventBus.$emitSnackbar('페이지 수정을 할 수 없습니다.');
          });
      }
    },
    async goToLabelingView() {
      const dto = await this.getPageUpdateDto();
      const pageLabelingView = {
        name: 'PageLabelingView',
        params: {
          workbook_id: this.workbook_id,
          page_id: this.page_id,
        }
      };

      //
      if (Object.keys(dto).length === 0) {
        this.$router.push(pageLabelingView);
      } else {
        const page_id = this.page_id;

        this.$store.dispatch('UPDATE_PAGE', {page_id, dto})
          .then(() => {
            this.$router.replace(pageLabelingView);
          })
          .catch(() => {
            this.$eventBus.$emitSnackbar('페이지 수정을 할 수 없습니다.');
          });
      }
    }
  },
};
</script>

<style scoped>

</style>