<template>
  <div>
    <div style="font-size: 20px;margin-left: 12px;margin: 14px;">属性库</div>
    <bk-divider></bk-divider>
    <div class="wrapper flex">
      <bk-container flex :col="12">
        <bk-row>
          <bk-col :span="4">
            <bk-button @click="createFieldSettings.visible = true" :theme="'primary'" :title="'新建属性'" class="mr10">
              新建属性
            </bk-button>
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
                <bk-option v-for="item in this.valueTypeMap" :key="item.type_id" :id="item.type_id" :name="item.name">
                </bk-option>
              </bk-select>
            </bk-dialog>
          </bk-col>
          <bk-col :span="4"></bk-col>
          <bk-col :span="4">
            <bk-row>
              <bk-input clearable :placeholder="'请输入关键字'" :right-icon="'bk-icon icon-search'" v-model="value"
                @right-icon-click="handlerIconClick">
              </bk-input>
            </bk-row>
          </bk-col>
        </bk-row>
      </bk-container>
      <div style="display: flex;width: 100%;flex-wrap: wrap;margin-top: 20px;margin-left: 20px;">
        <div v-for="(field,index) in this.fieldList" :key="'field'+index" class="card-demo" style="width: 200px;height: 60px;" @click="customSettings.isShow = true">
          <bk-card title="卡片标题" :show-foot="false" :show-head="false" style="width: 100%;height: 100%;">
            <div style="display: flex;width: 100%;height: 100%;" class="b-card">
              <div style="margin-left: 26px;margin-top: auto;margin-bottom: auto;">
                <div style="color: darkgray;">{{field.alias}}</div>
                <div style="display: flex;margin-top: 3px;">
                  <div style="color: lightgray;font-size: 14px;margin-right: 10px;">{{field.value_type}}</div>
                  <div style="color: lightgray;font-size: 14px;">{{field.name}}</div>
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
</template>

<script>
import {
  ciField,
  createCiField
} from '@/api/api'
export default {
  name: 'field',
  mounted () {
    this.getCiField()
  },
  data () {
    return {
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
      }
      ],
      createFieldSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      postFieldData: {
        name: '',
        alias: '',
        value_type: ''
      },
      fieldList: []
    }
  },
  methods: {
    getCiField () {
      ciField().then((response) => {
        this.fieldList = response.data.data
      })
    },
    postCreateField () {
      createCiField(this.postFieldData).then((response) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.getCiField()
      }).catch((error) => {
        this.$bkMessage({
          theme: 'error',
          message: error.message
        })
      })
    },
    handlerIconClick () {
      console.log('123')
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
</style>
