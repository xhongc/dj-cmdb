<template>
  <div v-bkloading="{ isLoading: basicLoading, zIndex: 10 }">
    <div style="display: flex;">
      <bk-icon type="arrows-left" style="font-size: 40px;color: #3A84FF;cursor: pointer;" @click="backTo" />
      <div style="font-size: 18px;margin-top: auto;margin-bottom: auto;">模型详情</div>
    </div>
    <bk-divider style="margin: auto;"></bk-divider>
    <div style="height: 70px;background: #ebf4ff;">
      <div style="display: flex;height: 100%;">
        <bk-icon type="apps" style="margin-top: auto;margin-bottom: auto;margin-left: 10px;margin-right: 20px;" />
        <div style="margin-top: auto;margin-bottom: auto;margin-right: 20px;">唯一标识：{{schemaData.name}}</div>
        <div style="margin-top: auto;margin-bottom: auto;margin-right: 20px;">名称：{{schemaData.alias}}</div>
        <!-- <div style="margin-top: auto;margin-bottom: auto;">实例数量：</div> -->
      </div>
    </div>
    <bk-tab :active.sync="active" type="unborder-card">
      <bk-tab-panel v-for="(panel, index) in panels" v-bind="panel" :key="index">
        <div v-if="active=='field'">
          <div>
            <bk-button theme="primary" @click="createFieldSettings.visible = true">新建属性</bk-button>
            <bk-dialog v-model="createFieldSettings.visible" title="新建属性" :header-position="createFieldSettings.headerPosition"
              :width="createFieldSettings.width" @confirm="postCreateField">
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
            </bk-dialog>
            <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
          </div>
          <div class="wrapper flex">
            <div style="display: flex;width: 100%;flex-wrap: wrap;margin-top: 10px;margin-left: -5px;">
              <div v-for="(field,index) in schemaData.field" :key="'field'+index" class="card-demo" style="width: 200px;height: 60px;"
                @click="customSettings.isShow = true">
                <bk-card title="卡片标题" :show-foot="false" :show-head="false" style="width: 100%;height: 100%;">
                  <div style="display: flex;width: 100%;height: 100%;" class="b-card">
                    <div style="margin-left: 26px;margin-top: auto;margin-bottom: auto;">
                      <div style="color: darkgray;">{{field.alias}}</div>
                      <div style="display: flex;margin-top: 3px;">
                        <div style="color: lightgray;font-size: 14px;margin-right: 10px;margin-top: auto;margin-bottom: auto;">{{field.value_type}}</div>
                        <div style="color: lightgray;font-size: 14px;margin-top: auto;margin-bottom: auto;">{{field.name}}</div>
                      </div>
                    </div>
                    <bk-icon type="edit" style="position: relative;left: 30px;bottom: -23px;color: #87CEEB;" class="b-detail" />
                  </div>
                </bk-card>
              </div>
            </div>
            <bk-sideslider :is-show.sync="customSettings.isShow" :quick-close="true">
              <div slot="header">{{ customSettings.title }}</div>
              <div class="p20" slot="content">
                自定义内容
              </div>
            </bk-sideslider>
          </div>
        </div>
        <div v-else-if="active=='relation'">
          <div>
            <bk-button theme="primary">新建关系</bk-button>
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
        </div>
        <div v-else>
          <bk-table style="margin-top: 15px;" :data="relationData" :size="setting.size">
            <bk-table-column v-for="field in setting.selectedFields" :key="field.id" :label="field.label" :prop="field.id">
            </bk-table-column>
            <bk-table-column type="setting">
              <bk-table-setting-content :fields="setting.fields" :selected="setting.selectedFields" :max="setting.max"
                :size="setting.size" @setting-change="handleSettingChange">
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
  readCISchema
} from '@/api/api'
export default {
  name: 'modelDetail',
  mounted () {
    this.readSchema()
  },
  computed: {
  },
  created () {
  },
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
      valueTypeMap: [{
        'type_id': 0,
        'name': '整型'
      },
      {
        'type_id': 1,
        'name': '浮点型'
      },
      {
        'type_id': 2,
        'name': '文本型'
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
        'type_id': 6,
        'name': 'JSON'
      },
      {
        'type_id': 7,
        'name': '字符串'
      },
      {
        'type_id': 8,
        'name': '枚举'
      }
      ],
      createFieldSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      pk: this.$route.params.schemaID,
      postFieldData: {
        name: '',
        alias: '',
        value_type: '',
        schema: this.$route.params.schemaID
      },
      fieldList: [],
      schemaData: {},
      relationData: [],
      setting: {
        max: 3,
        fields: fields,
        selectedFields: fields.slice(0, 3),
        size: 'small'
      },
      basicLoading: false
    }
  },
  methods: {
    backTo () {
      this.$router.push({
        name: 'model'
      })
    },
    getCiField () {
      ciField().then((response) => {
        this.fieldList = response.data.data
      })
    },
    readSchema () {
      this.basicLoading = true
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
      console.log(this.postFieldData)
      createCiField(this.postFieldData).then((response) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.readSchema()
      }).catch((error) => {
        this.$bkMessage({
          theme: 'error',
          message: error.message
        })
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
  }

  .b-card:hover .b-detail {
    display: block;
  }

  .bk-tab-section {
    padding: 10px;
  }
</style>
