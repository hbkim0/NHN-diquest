<template>
  <v-card max-width="600">
      <v-card-title>Upload</v-card-title>
      <v-card-text>
        <v-form
          ref="form"
          lazy-validation
        >                
          <v-row>
            <v-col cols="3">
              <v-card-subtitle class="pa-2 pl-0">Dataset :</v-card-subtitle>
            </v-col>
            <v-col cols="9">
              <v-select
                outlined
                required
                dense
                disabled
                item-text="name"
                item-value="_id"
                :items="datasets"
                v-model="selectedDataset"
                @change="fetchBundles()"
              >
              </v-select>
            </v-col>
            <v-col cols="3">
              <v-card-subtitle class="pa-2 pl-0">Bundle :</v-card-subtitle>
            </v-col>
            <v-col cols="9">
              <v-select
                outlined
                required
                dense
                item-text="name"
                item-value="_id"
                :items="bundles"
                v-model="selectedBundle"
              >
              </v-select>                        
            </v-col>
            <v-col cols="3">
              <v-card-subtitle class="pa-2 pl-0">Files :</v-card-subtitle>
            </v-col>
            <v-col cols="9">
              <v-file-input
                v-model="files"
                multiple
                small-chips
                prepend-icon="mdi-camera"
                label="Files"
                :accept="fileType"
                counter
                :show-size="1000"
              >
                <template v-slot:selection="{ index, text }">
                  <v-chip
                    label
                    small
                    close
                    color="green"
                    text-color="white"
                    @click:close="removeFile(index)"
                  >
                    {{ text }}
                  </v-chip>
                </template>
              </v-file-input>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions class="justify-end">
          <v-btn 
            large
            @click="cancel"
          >CANCEL</v-btn>
          <v-btn 
            v-if="selectedBundle != null && files.length !== 0"
            large 
            color="primary" 
            @click="upload"
          >UPLOAD</v-btn>
      </v-card-actions>
      <v-dialog persistent width="500" v-model="dialog.show.upload">
        <v-card>
          <v-card-title>{{!dialog.success ? 'Uploading' : 'Uploaded'}}</v-card-title>
          <v-card-text>
            <v-progress-linear 
              height="20"
              :value="(dialog.successCnt/files.length)*100"
              buffer-value="100"
              striped
              rounded
            >
            </v-progress-linear>
          </v-card-text>
          <v-card-text class="text-right">
            ( {{dialog.successCnt}} / {{files.length}} )
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn 
              v-if="!dialog.success"
              large 
              @click="dialog.show.upload = false"
            >CANCEL</v-btn>
            <v-btn
              v-else
              large 
              color="warning" 
              @click="done"
            >DONE</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-card>
</template>

<script>
export default {
    data: () => ({
      dialog: {
        show: {
            upload: false,
        },
        success: false,
        successCnt: 0,
      },
      mlTask: null,
      files: [],
      datasets: [],
      bundles: [],
      selectedDataset: '',
      selectedBundle: null,
    }),
    computed: {
      fileType(){
        let type = '';
        if (this.mlTask === 0) {
            type = 'text/*';
        } else if (this.mlTask === 1) {
            type = 'image/*';
        }
        return type;
      }
    },
    created() {
      console.log('DatasetUploadView - created', this.$route.params);
      this.selectedDataset = this.$route.params.dataset_id;      
      this.fetchDatasets();
    },
    methods: {
      fetchDatasets() {
        this.$store.dispatch('FETCH_DATASETS', {})
        .then(res => {
          this.datasets = res.datasets;
          this.fetchBundles();
        })
        .catch(error => { console.log(error) });
      },
      fetchBundles() {
        const dataset = this.datasets.find((r) => r._id === this.selectedDataset);
        this.mlTask = dataset.ml_task;

        this.$store.dispatch('FETCH_BUNDLES', this.selectedDataset)
          .then(res => {
            this.bundles = [...res.results];
            this.selectedBundle = (this.$route.params.bundle_id !== null) ? this.$route.params.bundle_id : null;
          })
          .catch(error => { console.log(error) });
      },
      removeFile(index) {
        this.files.splice(index,1);
      },
      async upload() {
        this.dialog.show.upload = true;
        //파일 업로드가 구현되어야함
        await this.files.forEach((file) => {
          
          this.$store.dispatch('UPLOAD_FILES', { dataset_id: this.$route.params.dataset_id, bundle_id: this.selectedBundle, files: file });
          
          this.dialog.successCnt += 1;
          
          if(this.files.length === this.dialog.successCnt) {  
            this.dialog.success = true;
          }
        });
      },
      cancel() {
        this.$router.back();
      },
      done() {
        this.files = [];
        this.dialog.show.upload = false;
        this.dialog.successCnt = 0;
      },

    }
}
</script>