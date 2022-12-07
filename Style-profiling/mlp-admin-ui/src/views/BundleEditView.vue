<template>
  <v-card max-width="1024">
    <v-card-title>Bundle Edit</v-card-title>
    <v-card-text>
      <v-form
        ref="form"
        lazy-validation
      >                
        <v-row>
          <v-col cols="2">
            <v-card-subtitle class="pa-2 pl-0">Name<v-icon x-small color="red">mdi-asterisk</v-icon> :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <v-text-field
              label="Bundle Name"
              dense
              required  
              :rules="[v => !!v || 'Required.']"
              v-model="bundle.name"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="2">
            <v-card-subtitle class="pa-2 pl-0">Description :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <v-textarea
              name="input-7-1"
              label="Bundle Description"
              hint="Bundle Description"
              v-model="bundle.description"
            ></v-textarea>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="2">
            <v-card-subtitle class="pa-2 pl-0">Attributes :</v-card-subtitle>
          </v-col>
          <v-col cols="9">
            <template v-for="(attr,index) in bundle.attributes">
              <v-container row fluid :key="index">
                <v-col class="ma-0 pa-0" cols="3">
                  <v-text-field 
                    class="pa-0"
                    v-model="attr.key" 
                    hint="key" 
                    persistent-hint
                    :rules="[v => !!v || 'Required.']"
                    solo
                  ></v-text-field>
                </v-col>
                <v-col class="ma-0 pa-0 pl-2" cols="8">
                  <v-container row fluid>
                    <v-combobox
                      class="ma-0 pa-0"
                      v-model="attr.values"
                      :rules="[v => !!v || 'Required.']"
                      small-chips
                      solo
                      clearable
                      hint="values" 
                      persistent-hint
                      multiple
                    >
                      <template v-slot:selection="{ attrs, item, selected }">
                        <v-chip
                          v-bind="attrs"
                          :input-value="selected"
                          close
                          @click:close="removeAttributeValue(index,item)"
                        >
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <strong v-bind="attrs" v-on="on">{{ item.replace(/(?<=.{5})(.*)(=?)/, '...') }}</strong>
                            </template>
                            <span>{{ item }}</span>
                          </v-tooltip>
                        </v-chip>
                      </template>
                    </v-combobox>
                  </v-container>
                </v-col>
                <v-col class="pl-0 justify-center" cols="1">
                  <v-btn
                    icon
                    @click="removeAttribute(index)"
                  >
                    <v-icon>
                      mdi-tag-remove
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-container>
            </template>
            
            <v-row>
              <v-col>
                <v-btn
                  icon
                  @click="addAttribute"
                >
                  <v-icon>
                    mdi-tag-plus
                  </v-icon>
                </v-btn>
              </v-col>
            </v-row>
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
      bundle: {
        
      },
    }),
    created() {
      console.log('BundleEditView - created - bundle id', this.$route.params.bundle_id);
      this.$store.dispatch('FETCH_BUNDLE', this.$route.params.bundle_id)
        .then(res => {
          this.bundle = res;
        })
        .catch(error => { console.log(error) });
    },
    methods: {
      addAttribute() {
        this.bundle.attributes = [...this.bundle.attributes, { key: '', values: '' }]
      },
      removeAttribute(index) {
        this.bundle.attributes.splice(index,1);
      },
      cancel() {
        this.$router.back();
      },
      save() {
        const validateForm = this.$refs.form.validate();
    
        if(validateForm) {
          console.log('성공');
          // 저장 action 필요
          this.$store.dispatch('UPDATE_BUNDLE', this.bundle)
            .then(res => {
              console.log('UPDATE_BUNDLE - res', res);
              this.$router.push({name:'DatasetDetailView', params: {dataset_id: this.$route.params.dataset_id}})
            })
            .catch(error => { console.log(error) });
        } else {
          console.log('실패');
        }
      },
      removeAttributeValue(index,itemIndex) {
        const values = this.bundle.attributes[index].values;
        values.splice(values.indexOf(itemIndex), 1);
      },
    }
}
</script>