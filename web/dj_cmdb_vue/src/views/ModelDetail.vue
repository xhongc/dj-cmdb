<template>
  <div v-bkloading="{ isLoading: basicLoading, zIndex: 10 }">
    <div style="display: flex;">
      <bk-icon type="arrows-left" style="font-size: 40px;color: #3A84FF;cursor: pointer;" @click="backTo" />
      <div style="font-size: 18px;margin-top: auto;margin-bottom: auto;">模型详情</div>
    </div>
    <bk-divider style="margin: auto;"></bk-divider>
    <div style="height: 70px;background: #ebf4ff;">
      <div style="display: flex;height: 100%;">
        <i :class="schemaData.icon_url" style="margin-top: auto;margin-bottom: auto;margin-left: 10px;margin-right: 20px;" />
        <div style="margin-top: auto;margin-bottom: auto;margin-right: 20px;">唯一标识：{{schemaData.name}}</div>
        <div style="margin-top: auto;margin-bottom: auto;margin-right: 20px;">名称：{{schemaData.alias}}</div>
        <!-- <div style="margin-top: auto;margin-bottom: auto;">实例数量：</div> -->
      </div>
    </div>
    <bk-tab :active.sync="active" type="unborder-card" @tab-change="handleTab">
      <bk-tab-panel v-for="(panel, index) in panels" v-bind="panel" :key="index">
        <div v-if="active=='field'">
          <div>
            <bk-button theme="primary" @click="createFieldSettings.visible = true">新建属性</bk-button>
            <bk-sideslider :is-show.sync="createFieldSettings.visible" :quick-close="true" :width="createFieldSettings.width"
              :before-close="clearForm">
              <div slot="header">{{createFieldSettings.title}}</div>
              <div class="p20" slot="content">
                <bk-form :label-width="200" form-type="vertical" class="form">
                  <div>唯一标识</div>
                  <bk-input :placeholder="'请输入唯一标识'" style="margin-bottom: 15px;" v-model="postFieldData.name">
                  </bk-input>
                  <div>属性名称</div>
                  <bk-input :placeholder="'请输入属性名称'" style="margin-bottom: 15px;" v-model="postFieldData.alias">
                  </bk-input>
                  <div>字段类型</div>
                  <bk-select :disabled="false" :search-with-pinyin="true" v-model="postFieldData.value_type" style="width: 250px;"
                    ext-cls="select-custom" ext-popover-cls="select-popover-custom" searchable>
                    <bk-option v-for="item in valueTypeMap" :key="item.type_id" :id="item.type_id" :name="item.name">
                    </bk-option>
                  </bk-select>

                  <div v-if="postFieldData.value_type===8||postFieldData.value_type==='8'" style="margin-top: 10px ;">
                    <div>枚举值</div>
                    <div v-for="(item, index) in postFieldData.meta.enum" :key="'index'+index">
                      <bk-input v-model="item.key" placeholder="请输入枚举键" class='enum-key'></bk-input>
                      <bk-input v-model="item.value" placeholder="请输入枚举值" class='enum-value'></bk-input>
                      <bk-icon type="minus-circle-shape" @click="rmEnum(index)" class='icon-rm'/>
                      <bk-icon type="plus-circle-shape" v-if="postFieldData.meta.enum.length===index+1" @click="addEnum" class='icon-add'/>
                    </div>
                  </div>
                  <div>是否必填
                    <bk-switcher v-model="postFieldData.meta.is_required" theme="primary"></bk-switcher>
                  </div>
                  <div>是否唯一
                    <bk-switcher v-model="postFieldData.meta.is_unique" theme="primary"></bk-switcher>
                  </div>
                  <div style="flex-basis: 100%;position:fixed; right:0px; bottom:5px; z-index:999;width: 500px;background-color: white;">
                    <bk-divider style="margin: 0 0 8px;"></bk-divider>
                    <bk-button ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="postCreateField">提交</bk-button>
                    <bk-button ext-cls="mr5" theme="default" title="取消" @click.stop.prevent="createFieldSettings.visible=false">取消</bk-button>
                  </div>
                </bk-form>
              </div>
            </bk-sideslider>

            <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
          </div>
          <div class="wrapper flex">
            <draggable class="card-parent" v-model="schemaData.field" :options="{animation:380}" @change="change">
              <bk-exception v-if="schemaData.field.length===0" class="exception-wrap-item exception-part" type="empty"
                scene="part"> </bk-exception>
              <div v-for="(field,index) in schemaData.field" :key="'field'+index" class="card-demo" style="width: 200px;height: 60px;position: relative;"
                @click="fieldDetail(field)">
                <bk-card title="卡片标题" :show-foot="false" :show-head="false" style="width: 100%;height: 100%;">
                  <div style="display: flex;width: 100%;height: 100%;" class="b-card">
                    <div style="margin-left: 26px;margin-top: auto;margin-bottom: auto;">
                      <div style="color: darkgray;">{{field.alias}}</div>
                      <div style="display: flex;margin-top: 3px;">
                        <div style="color: lightgray;font-size: 14px;margin-right: 10px;margin-top: auto;margin-bottom: auto;">{{valueMap[field.value_type]}}</div>
                        <div style="color: lightgray;font-size: 14px;margin-top: auto;margin-bottom: auto;">{{field.name}}</div>
                      </div>
                    </div>
                    <bk-icon type="edit" style="position: relative;left: 30px;bottom: -23px;color: #87CEEB;" class="b-detail" />
                  </div>
                </bk-card>
              </div>
            </draggable>
          </div>
        </div>
        <div v-else-if="active=='relation'">
          <div>
            <bk-button theme="primary" @click="createRelationSettings.visible = true">新建关系</bk-button>
            <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
          </div>
          <bk-table style="margin-top: 15px;" :data="relationData" :size="setting.size">
            <bk-table-column v-for="field in setting.selectedFields" :key="field.id" :label="field.label" :prop="field.id">
            </bk-table-column>
            <bk-table-column type="setting">
              <bk-table-setting-content :fields="setting.fields" :selected="setting.selectedFields" :max="setting.max"
                :size="setting.size" @setting-change="handleSettingChange">
              </bk-table-setting-content>
            </bk-table-column>
          </bk-table>
          <bk-sideslider :is-show.sync="createRelationSettings.visible" :quick-close="true" :width="createRelationSettings.width"
            :before-close="clearRelationForm">
            <div slot="header">新建关系</div>
            <div class="p20" slot="content">
              <bk-form :label-width="200" form-type="vertical" class="form">
                <div>源模型</div>
                <bk-select :disabled="false" :search-with-pinyin="true" v-model="postRelationData.source_id" style="width: 250px;"
                  ext-cls="select-custom" ext-popover-cls="select-popover-custom" searchable>
                  <bk-option v-for="item in schemaRelationSelect.schema" :key="item.id" :id="item.id" :name="item.alias">
                  </bk-option>
                </bk-select>
                <div>目标模型</div>
                <bk-select :disabled="false" :search-with-pinyin="true" v-model="postRelationData.target_id" style="width: 250px;"
                  ext-cls="select-custom" ext-popover-cls="select-popover-custom" searchable>
                  <bk-option v-for="item in schemaRelationSelect.schema" :key="item.id" :id="item.id" :name="item.alias">
                  </bk-option>
                </bk-select>
                <div>关联关系</div>
                <bk-select :disabled="false" :search-with-pinyin="true" v-model="postRelationData.relation_id" style="width: 250px;"
                  ext-cls="select-custom" ext-popover-cls="select-popover-custom" searchable>
                  <bk-option v-for="item in schemaRelationSelect.relation" :key="item.id" :id="item.id" :name="item.alias">
                  </bk-option>
                </bk-select>
                <bk-form-item class="mt20" style="flex-basis: 100%;">
                  <bk-button ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="postCreateRelation">提交</bk-button>
                  <bk-button ext-cls="mr5" theme="default" title="取消" @click.stop.prevent="createRelationSettings.visible=false">取消</bk-button>
                </bk-form-item>
              </bk-form>
            </div>
          </bk-sideslider>
        </div>
        <div v-else>
          <bk-table style="margin-top: 15px;" :data="fieldList" :size="metaSetting.size">
            <bk-table-column v-for="field in metaSetting.selectedFields" :key="field.id" :label="field.label" :prop="field.id">
            </bk-table-column>
            <bk-table-column type="setting">
              <bk-table-setting-content :fields="metaSetting.fields" :selected="metaSetting.selectedFields" :max="metaSetting.max"
                :size="metaSetting.size" @setting-change="handleMetaSettingChange">
              </bk-table-setting-content>
            </bk-table-column>
          </bk-table>
        </div>
      </bk-tab-panel>
    </bk-tab>
  </div>
</template>

<script>
import {
  ciField,
  createCiField,
  readCISchema,
  updateCiField,
  getSchemaRelationSelect,
  createRelation
} from '@/api/api'
import draggable from 'vuedraggable'
export default {
  name: 'modelDetail',
  mounted () {
    this.readSchema()
  },
  computed: {},
  components: {
    draggable
  },
  created () {},
  data () {
    const fields = [{
      id: 'source',
      label: '源模型',
      disabled: true
    }, {
      id: 'relation',
      label: '关联关系'
    }, {
      id: 'target',
      label: '目标模型'
    }]
    const metaFields = [{
      id: 'alias',
      label: '字段名称'
    }, {
      id: 'is_unique',
      label: '是否唯一'
    },
    {
      id: 'is_required',
      label: '是否必填'
    },
    {
      id: 'value_type',
      label: '字段类型'
    }, {
      id: 'name',
      label: '字段标识'
    }
    ]
    return {
      panels: [{
        name: 'field',
        label: '模型字段'
      },
      {
        name: 'relation',
        label: '模型关联'
      },
      {
        name: 'unique',
        label: '唯一校验'
      }
      ],
      active: 'field',
      value: '',
      customSettings: {
        isShow: false,
        title: '字段详情'
      },
      valueMap: {
        '0': '整型',
        '1': '浮点型',
        '2': '文本型',
        '3': '日期时间',
        '4': '日期',
        '5': '时间',
        '6': 'JSON',
        '7': '字符串',
        '8': '枚举'
      },
      valueTypeMap: [{
        'type_id': 0,
        'name': '整型'
      },
      {
        'type_id': 1,
        'name': '浮点型'
      },
      {
        'type_id': 7,
        'name': '字符串'
      },
      {
        'type_id': 3,
        'name': '日期时间'
      },
      {
        'type_id': 4,
        'name': '日期'
      },
      {
        'type_id': 5,
        'name': '时间'
      },
      {
        'type_id': 2,
        'name': '文本型'
      },
      {
        'type_id': 6,
        'name': 'JSON'
      },

      {
        'type_id': 8,
        'name': '枚举'
      }
      ],
      createFieldSettings: {
        title: '新建属性',
        visible: false,
        width: 500,
        headerPosition: 'left'
      },
      createRelationSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      pk: this.$route.params.schemaID,
      postFieldData: {
        name: '',
        alias: '',
        value_type: '',
        schema: this.$route.params.schemaID,
        meta: {
          is_required: false,
          is_unique: false,
          'enum': [{'key': '', 'value': ''}]
        }
      },
      postRelationData: {
        source_id: this.$route.params.schemaID,
        target_id: '',
        relation_id: ''
      },
      fieldList: [],
      schemaData: {
        field: []
      },
      relationData: [],
      setting: {
        max: 3,
        fields: fields,
        selectedFields: fields.slice(0, 3),
        size: 'small'
      },
      basicLoading: false,
      metaSetting: {
        max: 3,
        fields: metaFields,
        selectedFields: metaFields.slice(0, 3),
        size: 'small'
      },
      schemaRelationSelect: {},
      positionX: '',
      positionY: ''
    }
  },
  methods: {
    backTo () {
      this.$router.push({
        name: 'model'
      })
    },
    getCiField (params) {
      ciField(params).then((response) => {
        this.fieldList = response.data.data
        console.log(this.fieldList)
      })
    },
    readSchema () {
      this.basicLoading = true
      if (!this.pk) {
        this.$router.push({
          name: 'model'
        })
      }
      readCISchema(this.pk).then((response) => {
        this.basicLoading = false
        this.schemaData = response.data.data

        for (var i in this.schemaData.relation_schema) {
          this.schemaData.relation.push(this.schemaData.relation_schema[i])
        }
        this.relationData = this.schemaData.relation
      })
    },
    postCreateField () {
      if (this.postFieldData['field_id']) {
        updateCiField(this.postFieldData['field_id'], this.postFieldData).then((response) => {
          this.$bkMessage({
            theme: 'success',
            message: '创建成功'
          })
          this.createFieldSettings.visible = false
          this.readSchema()
        }).catch((error) => {
          this.$bkMessage({
            theme: 'error',
            message: error.message
          })
        })
      } else {
        createCiField(this.postFieldData).then((response) => {
          this.$bkMessage({
            theme: 'success',
            message: '创建成功'
          })
          this.createFieldSettings.visible = false
          this.readSchema()
        }).catch((error) => {
          this.$bkMessage({
            theme: 'error',
            message: error.message
          })
        })
      }
    },
    postCreateRelation () {
      console.log(this.postRelationData)
      createRelation(this.postRelationData).then((res) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.createRelationSettings.visible = false
        this.readSchema()
      }).catch((err) => {
        this.$bkMessage({
          theme: 'error',
          message: err.message
        })
      })
    },
    getSchemaRelation () {
      getSchemaRelationSelect().then((res) => {
        console.log(1)
        this.schemaRelationSelect = res.data.data
      }).catch((err) => {
        console.log(err)
      })
    },
    handlerIconClick () {
      console.log('123')
    },
    handleSettingChange ({
      fields,
      size
    }) {
      this.setting.size = size
      this.setting.selectedFields = fields
    },
    handleMetaSettingChange ({
      fields,
      size
    }) {
      this.metaSetting.size = size
      this.metaSetting.selectedFields = fields
    },
    handleTab (name) {
      if (name === 'unique') {
        this.getCiField({
          meta: '1',
          schema_id: this.pk
        })
      } else if (name === 'relation') {
        this.getSchemaRelation()
      }
    },
    fieldDetail (raw) {
      this.postFieldData.field_id = raw.id
      this.postFieldData.name = raw.name
      this.postFieldData.alias = raw.alias
      this.postFieldData.value_type = raw.value_type
      this.postFieldData.meta = raw.meta
      this.createFieldSettings.title = '修改属性'
      this.createFieldSettings.visible = true
    },
    clearForm () {
      this.postFieldData.name = ''
      this.postFieldData.alias = ''
      this.postFieldData.value_type = ''
      this.postFieldData.meta = {
        is_required: false,
        is_unique: false,
        'enum': [{'key': '', 'value': ''}]
      }
      this.createFieldSettings.title = '新建属性'
      this.createFieldSettings.visible = false
    },
    clearRelationForm () {
      this.createRelationSettings.visible = false
    },
    addEnum () {
      this.postFieldData.meta.enum.push({'key': '', 'value': ''})
    },
    rmEnum (index) {
      if (this.postFieldData.meta.enum.length === 1) {
        return false
      }
      this.postFieldData.meta.enum.splice(index, 1)
    },
    change (evt) {
      console.log('change', evt, this.schemaData.field)
    }
  }

}
</script>

<style>
  .bk-card-body {
    width: 100%;
    height: 100%;
  }

  .b-detail {
    display: none;
    cursor: pointer;
  }
  .b-card {
    cursor: move;
  }
  .b-card:hover .b-detail {
    display: block;
  }

  .bk-tab-section {
    padding: 10px;
  }
  .enum-key {
    width: 100px;
    margin-right: 10px;
    margin-top: 5px;
  }
  .enum-value{
    width: 200px;
    margin-right: 5px;
    margin-top: 5px;
  }
  .icon-add {
    color: lightgray;
    cursor: pointer;
  }
  .icon-rm {
    color: lightgray;
    cursor: pointer;
  }
  .card-parent {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
    margin-top: 10px;
    margin-left: -5px;
    cursor: move;
  }
</style>
