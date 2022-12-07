<template>
  <v-container fluid>
    <v-card>
      <v-carousel 
        hide-delimiters
        height="100"
        @change="params.offset = $event" 
      >
        <v-carousel-item
          v-for="(n, i) in total_results"
          :key="i"
        >
          <v-sheet
            height="100%"
            tile
          >
            <v-row
              class="fill-height"
              align="center"
              justify="center"
            >
              <div class="text-h5">
                <v-card-title v-text="file_name"></v-card-title>
                <v-card-subtitle class="text-center">
                  ({{n}}/{{total_results}}) 
                </v-card-subtitle>
              </div>
            </v-row>
          </v-sheet>
        </v-carousel-item>
      </v-carousel>
      <v-divider></v-divider>
      <v-container fluid>
          <TextTagging
              v-if="ml_task == 0"
              :params="params"
              @setFileName="setFileName"
              @setMLTask="setMLTask"
          />
          <ImageTagging
              v-if="ml_task == 1"
              :params="params"
              @setFileName="setFileName"
              @setMLTask="setMLTask"
          />
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import ImageTagging from '../components/ImageTaggingComponent.vue';
import TextTagging from '../components/TextTaggingComponent.vue';
export default {
  components: {
    ImageTagging,
    TextTagging,
  },
  data: () => ({
    annotations: [],
    total_results: 0,
    ml_task: null,
    params: {},
    file_name: null,
  }),
  created() {
    this.total_results = this.$route.params.total_results;
    this.ml_task = this.$route.params.ml_task;
    this.params = { 
      dataset_id : this.$route.params.dataset_id, 
      bundle_ids: this.$route.params.bundle_ids,
      label_status: this.$route.params.label_status,
      limit: 1,
      offset: 0,
      maintain: false,
    };
  },
  methods: {
    setFileName(file_name) {
      this.file_name = file_name;
    },
    setMLTask(ml_task) {
      this.ml_task = ml_task;
    },
    setTotalResults(total_results) {
      this.total_results = total_results;
    },
  }
}
</script>