<template>
  <v-card class="pa-4">
    <v-card-title>버전 정보</v-card-title>
    <v-card-text>
      <p>- 페이지 인식 모델: <em>ver.{{ versions.search_model }}</em></p>
      <p> - 손글씨 인식 모델: <em>ver.{{ versions.recognition_model }}</em></p>
      <p> - 자동채점 서비스: <em>ver.{{ versions.scroing_service }}</em></p>
      <p> - 자동채점 관리도구: <em>ver.{{ versions.admin_ui }}</em></p>
    </v-card-text>
    <v-card-actions>
      <v-tooltip right>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
            :loading="loading_reindex"
            @click="doPageReindex"
          >
            페이지 재인덱싱
          </v-btn>
        </template>
        <div style="max-width:320px">
          페이지 인식 모델이 변경된 경우, 자동채점 서비스에 저장된 페이지들의 인텍스를 조정해야 합니다. 수 분의 시간이 걸릴 수 있습니다.
        </div>
      </v-tooltip>
    </v-card-actions>
  </v-card>
</template>

<script>
const adminUiVersion = process.env.VUE_APP_VERSION;

export default {
  name: 'ScoringAdminUiSystemView',

  data() {
    return {
      versions: {
        search_model: '',
        recognition_model: '',
        scroing_service: '',
        admin_ui: adminUiVersion
      },
      loading_reindex: false,
    };
  },

  mounted() {
    this.$store.dispatch('FETCH_VERSIONS')
      .then((res) => {
        this.versions.search_model = res.search_model;
        this.versions.recognition_model = res.recognition_model;
        this.versions.scroing_service = res.scroing_service;
      })
      .catch(() => {
        this.$eventBus.$emitSnackbar('버전 정보을 가져올 수 없습니다.');
      });
  },

  methods: {
    doPageReindex() {
      this.loading_reindex = true;
      this.$store.dispatch('REINDEX')
        .then((res) => {
          return res.updated_cnt;
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('재인덱싱 작업을 수행할 수 없습니다.');
        })
        .finally(() => {
          this.loading_reindex = false;
        })
    }
  },
};
</script>

<style scoped>

</style>