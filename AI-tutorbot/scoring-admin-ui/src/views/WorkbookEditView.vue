<template>
  <v-card max-width="640" class="pa-4">
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
          label="이름"
          required
          :rules="[v => ((!!v) && (String(v) && !!(v.trimEnd()))) || 'required']"
          :value="editedWorkbook.name"
          @change="(value) => changValue('name', value)"
        />
        <v-textarea
          label="설명"
          :value="editedWorkbook.description"
          @change="(value) => changValue('description', value)"
        />
        <v-file-input label="표지" accept="image/*" @change="changeImage" />
        <v-img contain position="top left" class="ma-2" max-width="480" :src="image_url" />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="() => this.$router.back()">취소</v-btn>
      <v-btn :disabled="!valid" color="primary" @click="saveWorkbook">저장</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiWorkbookEditView',

  data() {
    return {
      valid: null,
      workbook_id: '',
      initWorkbook: {},
      editedWorkbook: {
        name: '',
        description: '',
        image_url: '',
      },
      local_file: null,
    };
  },

  mounted() {
    this.workbook_id = this.$route.params.workbook_id;
    this.$store.dispatch('FETCH_WORKBOOK', this.workbook_id)
      .then((workbook) => {
        this.initWorkbook.name = workbook.name;
        this.initWorkbook.description = workbook.description;
        this.initWorkbook.image_url = workbook.image_url;
        this.editedWorkbook = window.structuredClone(this.initWorkbook);
      })
      .catch(() => {
        this.$eventBus.$emitHomeModal('문제집 정보을 가져올 수 없습니다.');
      });
  },

  computed: {
    image_url() {
      let image_url = resolveImageUrl(this.editedWorkbook.image_url) || '';
      if(this.local_file) {
        image_url = URL.createObjectURL(this.local_file);
      }

      return image_url;
    },
  },

  methods: {
    changValue(key, value) {
      this.editedWorkbook[key] = value;
    },
    changeImage(file) {
      this.local_file = file;
    },

    async saveWorkbook() {

      // TODO: upload-image
      if (this.local_file) {
        const res = await this.$store.dispatch('UPLOAD_IMAGES', this.local_file);
        let {paths} = res;

        if (!Array.isArray(paths) || paths.length < 1) {
          this.$eventBus.$emitSnackbar('이미지를 업로드 할 수 없습니다.');
          return;
        }

        this.editedWorkbook.image_url = paths[0];
      }

      //
      this.editedWorkbook.name = this.editedWorkbook.name.trim();
      this.editedWorkbook.description = this.editedWorkbook.description.trim();

      //
      let dto = {};
      if (this.editedWorkbook.name !== this.initWorkbook.name) {
        dto.name = this.editedWorkbook.name;
      }
      if (this.editedWorkbook.description !== this.initWorkbook.description) {
        dto.description = this.editedWorkbook.description;
      }
      if (this.editedWorkbook.image_url !== this.initWorkbook.image_url) {
        dto.image_url = this.editedWorkbook.image_url;
      }

      //
      if (Object.keys(dto).length === 0) {
        this.$router.back();
      } else {
        const workbook_id = this.workbook_id;

        this.$store.dispatch('UPDATE_WORKBOOK', {workbook_id, dto})
          .then(() => {
            this.$router.back();
          })
          .catch(() => {
            this.$eventBus.$emitSnackbar('문제집 수정을 할 수 없습니다.');
          });
      }
    },
  },
};
</script>

<style scoped>

</style>