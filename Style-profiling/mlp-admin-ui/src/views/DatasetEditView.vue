<template>
  <v-card max-width="600">
    <v-card-title>Dataset Edit</v-card-title>
    <v-card-text>
      <v-form
          ref="form"
          lazy-validation
      >                
        <v-row>
          <v-col cols="3">
            <v-card-subtitle class="pa-2 pl-0">ML Task :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <v-select
              dense
              v-model="datasetEditDto.ml_task"
              :items="[{text:getMLTaskName(datasetEditDto.ml_task), value:datasetEditDto.ml_task}]"
              disabled
            >
            </v-select>
          </v-col>
          <v-col cols="3">
            <v-card-subtitle class="pa-2 pl-0">Name<v-icon x-small color="red">mdi-asterisk</v-icon> :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <v-text-field
              label="Dataset Name"
              dense
              required  
              :rules="[v => !!v || 'Required.']"
              v-model="datasetEditDto.name"
            ></v-text-field>
          </v-col>
          <v-col cols="3">
            <v-card-subtitle class="pa-2 pl-0">Description :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <v-textarea
              name="input-7-1"
              label="Dataset Description"
              hint="Dataset Description"
              v-model="datasetEditDto.description"
            ></v-textarea>
          </v-col>
          <v-col cols="3">
            <v-card-subtitle class="pa-2 pl-0">Cover Image :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <v-container class="pa-0 text-center">
              <v-file-input 
                small-chips
                prepend-icon="mdi-camera"
                label="Cover Image"
                accept="image/*"
                @change="changeFile"
              >
              </v-file-input>
              <v-img :src="getCoverImage(datasetEditDto.cover_image)" contain width="300"/>
            </v-container>
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
        large 
        color="primary" 
        @click="save"       
      >SAVE</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
    data: () => ({
      datasetEditDto: {},
      files: null,
    }),
    created() {
      this.$store.dispatch('FETCH_DATASET', this.$route.params.dataset_id)
        .then(res => {
          console.log('DatasetDetailView - created - fetch dataset',res);
          this.datasetEditDto = res;
          //this.datasetEditDto.cover_image = this.getCoverImage(this.datasetEditDto.cover_image);
        })
        .catch(error => { console.log(error) });
    },
    methods: {
      changeFile(file) {
        this.files = file;
      },
      cancel() {
        this.$router.back();
      },
      async save() {
        console.log(this.datasetEditDto);
        const validateForm = this.$refs.form.validate();
        if(validateForm) {

          if(this.files) {
            const { image_url } = await this.$store.dispatch('UPLOAD_FILES', {dataset_id: this.$route.params.dataset_id, files: this.files});
            console.log('dataset edit - save - cover_image ', image_url); 
            this.datasetEditDto.cover_image = image_url;
          }
          this.$store.dispatch('UPDATE_DATASET', this.datasetEditDto)
            .then(res => {
              console.log('UPDATE_DATASET - res', res);
              this.$router.push({name:'DatasetDetailView', params: {dataset_id: this.$route.params.dataset_id}})
            })
            .catch(error => { console.log(error) });
        } else {
          console.log('실패');
        }
      }
    }
}
</script>