<template>
  <v-card>
    <v-card-title>
      <span class="text-h5">Label {{ !validLabel ? 'Create' : 'Update' }}</span>
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-card-subtitle class="pb-0 mb-0">Registered Labels</v-card-subtitle>
        <v-card class="rounded-lg mx-auto mb-5" outlined elevation="0">
          <v-container class="pa-1 ma-0" row>
            <v-chip-group 
              column
              v-model="selectedChipIndex"
              @change="changeLabel"
              class="pa-1"
            > 
              <template v-for="(chip, i) in labelChips">
                <v-chip
                  class="mx-1"
                  :key="i"
                  label
                  filter
                  :color="chip.color"
                  text-color="white"
                >
                  {{chip.name}}
                </v-chip>
              </template>
            </v-chip-group>
          </v-container>
        </v-card>
        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
        >
          <v-row>
            <v-col cols="3">
              <v-card-subtitle class="pa-2 pl-0">Label<v-icon x-small color="red">mdi-asterisk</v-icon> :</v-card-subtitle>
            </v-col>
            <v-col cols="9">
              <v-text-field
                label="Label Name"
                dense
                required
                v-model="label"
                :rules="[v => !!v || 'Required.']"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="4"
            >
              <v-btn
                v-for="t in types"
                :key="t"
                class="my-4"
                block
                @click="type = t"
              >
                {{ t }}
              </v-btn>
            </v-col>
            <v-col
              class="d-flex justify-center"
            >
              <v-color-picker v-model="color"></v-color-picker>
            </v-col>
            <v-col
              cols="12"
              md="4"
            >
              <v-sheet
                dark
                class="pa-4"
              >
              <pre>{{ showColor }}</pre>
              </v-sheet>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
      <small>*구분을 위해 레이블 색상을 지정 할 수 있습니다.</small>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        large
        @click="cancel"
      >
        Close
      </v-btn>
      <v-btn
        v-if="!validLabel"
        large
        color="primary"
        @click="createLabel"
      >
        Create
      </v-btn>
      <v-btn
        v-else
        large
        color="primary"
        @click="createLabel"
      >
        Update
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  export default {
    props: {
      labelChips: Array,
    },
    data: () => ({
      selectedChipIndex: null,
      selectedLabel: {},
      label: '',
      valid: false,
      types: ['hex', 'hexa'],
      //types: ['hex', 'hexa', 'rgba', 'hsla', 'hsva'],
      type: 'hex',
      hex: '#000000',
      hexa: '#FF00FFFF',
    //   rgba: { r: 255, g: 0, b: 255, a: 1 },
    //   hsla: { h: 300, s: 1, l: 0.5, a: 1 },
    //   hsva: { h: 300, s: 1, v: 1, a: 1 },
    }),   
    computed: {
      color: {
        get () {
          return this[this.type]
        },
        set (v) {
          this[this.type] = v
        },
      },
      showColor () {
        if (typeof this.color === 'string') return this.color

        return JSON.stringify(Object.keys(this.color).reduce((color, key) => {
          color[key] = Number(this.color[key].toFixed(2))
          return color
        }, {}), null, 2)
      },
      validLabel() {
        const findChips = {...this.labelChips.find((r) => r.name === this.label)};
        console.log(this.selectedLabel.label_id,typeof(this.selectedLabel.label_id),typeof(this.selectedLabel.label_id) === 'undefined');
        return (typeof(this.selectedLabel.label_id) === 'undefined') ? !findChips : !!findChips;
      }
    },
    methods: {
      labelInit() {
        this.selectedLabel = {};
        this.selectedChipIndex = null;
        this.label = '';
        this.color = '#000000';
      },
      changeLabel(index) {     
        this.selectedLabel = (typeof(index) !== 'undefined') ? {...this.labelChips[index]} : {};
        this.label = this.selectedLabel.name;

        if ((typeof(index) !== 'undefined') && (this.selectedLabel.color.length == 9)) {
          this.hexa = this.selectedLabel.color;
        } else if ((typeof(index) !== 'undefined') && (this.selectedLabel.color.length == 7)) {
          this.hex = this.selectedLabel.color;
        }

      },
      createLabel() {
        const validateForm = this.$refs.form.validate();

        if(validateForm) {
          this.dialog = false;
          const addChip = (typeof(this.selectedLabel.label_id) !== 'undefined') ? {label_id: this.selectedLabel.label_id, name: this.label, color: this.color} : {name: this.label, color: this.color};
          this.$emit('addLabelChip', addChip);  
          this.labelInit();
        }
      },
      cancel() {
        this.$emit('closeLabelDialog');
        this.labelInit();
      }
    }
  }
</script>