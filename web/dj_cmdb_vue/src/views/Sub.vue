<template>
  <div>
    <div class="sub-title">事件订阅</div>
    <bk-divider></bk-divider>
    <div style="margin-left: 10px;margin-right: 10px;">
      <bk-button theme="primary" @click="customSettings.isShow=true">新建</bk-button>
      <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
    </div>
    <bk-table style="margin-top: 15px;" :data="subData" :size="setting.size">
      <bk-table-column v-for="field in setting.selectedFields" :key="field.id" :label="field.label" :prop="field.id">
      </bk-table-column>
      <bk-table-column label="编辑" width="150">
        <template slot-scope="props">
          <bk-button class="mr10" theme="primary" text :disabled="props.row.status === '创建中'" @click="resetSub(props.row)">编辑</bk-button>
          <bk-button class="mr10" theme="primary" text @click="removeSub(props.row)">移除</bk-button>
        </template>
      </bk-table-column>
      <bk-table-column type="setting">
        <bk-table-setting-content :fields="setting.fields" :selected="setting.selectedFields" :max="setting.max" :size="setting.size"
          @setting-change="handleSettingChange">
        </bk-table-setting-content>
      </bk-table-column>
    </bk-table>
    <bk-pagination size="small" :current.sync="pagingConfigTwo.current" :limit="pagingConfigTwo.limit" :count="pagingConfigTwo.count"
      :location="pagingConfigTwo.location" :align="pagingConfigTwo.align" :show-limit="pagingConfigTwo.showLimit"
      :limit-list="pagingConfigTwo.limitList" :show-total-count="pagingConfigTwo.totalCount" @change="changePage"
      @limit-change="changeLimit">
    </bk-pagination>
    <bk-sideslider :is-show.sync="customSettings.isShow" :quick-close="true" :width="customSettings.width"
      :before-close="clearFormData">
      <div slot="header">{{ customSettings.title }}</div>
      <div class="p20" slot="content">
        <bk-form :label-width="120" :model="formData">
          <bk-form-item label="订阅名称" :required="true" :property="'name'">
            <bk-input v-model="formData.name"></bk-input>
          </bk-form-item>
          <bk-form-item label="订阅人" :required="true" :property="'subscriber'">
            <bk-input v-model="formData.subscriber"></bk-input>
          </bk-form-item>
          <bk-form-item label="通知地址" :required="true" :property="'notify_url'">
            <bk-input v-model="formData.notify_url"></bk-input>
          </bk-form-item>
          <bk-form-item label="成功状态码" :required="true" :property="'success_code'">
            <bk-input v-model="formData.success_code"></bk-input>
          </bk-form-item>
          <bk-form-item label="超时时间" :required="true" :property="'timeout'">
            <bk-input v-model="formData.timeout"></bk-input>
          </bk-form-item>
          <bk-collapse v-model="activeName">
            <div v-for="(group,index) in groupSchemaData" :key="'group'+index">
              <bk-collapse-item :name="group.id" class="ci-group">
                {{group.alias}}
                <div slot="content" class="f13">
                  <div style="display: flex;width: 100%;flex-wrap: wrap;">
                    <div v-for="(ci,index) in group.schema" :key="'ci'+index">
                      <bk-form-item :label="ci.alias">
                        <bk-checkbox-group v-model="formData.meta[ci.name]">
                          <bk-checkbox :label="'add'" class="mr20">
                            <i class="bk-icon mr5"></i>新增
                          </bk-checkbox>
                          <bk-checkbox :label="'modify'" class="mr20">
                            <i class="bk-icon mr5"></i>修改
                          </bk-checkbox>
                          <bk-checkbox :label="'delete'">
                            <i class="bk-icon mr5"></i>删除
                          </bk-checkbox>
                        </bk-checkbox-group>
                      </bk-form-item>
                    </div>
                  </div>
                </div>
              </bk-collapse-item>
            </div>
          </bk-collapse>
          <div style="flex-basis: 100%;position:fixed; right:0px; bottom:5px; z-index:999;width: 500px;background-color: white;">
            <bk-divider style="margin: 0 0 8px;"></bk-divider>
            <bk-button ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="submitData">提交</bk-button>
            <bk-button ext-cls="mr5" theme="default" title="取消" @click.stop.prevent="clearFormData">取消</bk-button>
          </div>
        </bk-form>
      </div>
    </bk-sideslider>
  </div>
</template>

<script>
import {
  getSub,
  ciSChemaGroup,
  createSub,
  deleteSub,
  updateSub
} from '@/api/api'
export default {
  mounted () {
    this.getSubData()
    this.getCiSchemaGroupData()
  },
  data () {
    const fields = [{
      id: 'name',
      label: '订阅名称'
    },
    {
      id: 'subscriber',
      label: '订阅人'
    },
    {
      id: 'update_time',
      label: '更新时间'
    },
    {
      id: 'notify_url',
      label: '通知地址'
    },
    {
      id: 'success_code',
      label: '成功状态'
    },
    {
      id: 'timeout',
      label: '超时时间'
    }
    ]
    return {
      customSettings: {
        isShow: false,
        title: '创建事件订阅',
        width: 500
      },
      pagingConfigTwo: {
        current: 1,
        limit: 10,
        count: 0,
        location: 'left',
        align: 'right',
        showLimit: true,
        limitList: [10, 20, 50],
        totalCount: true
      },
      setting: {
        max: 3,
        fields: fields,
        selectedFields: fields.slice(0, 3),
        size: 'small'
      },
      subData: [],
      groupSchemaData: [],
      activeName: [],
      formData: {
        'name': '',
        'subscriber': '',
        'notify_url': '',
        'success_code': '',
        'timeout': '',
        'meta': {}
      }
    }
  },
  methods: {
    getSubData () {
      getSub({
        page: this.pagingConfigTwo.current,
        page_size: this.pagingConfigTwo.limit
      }).then((res) => {
        console.log(res)
        this.subData = res.data.data.items
      }).catch((err) => {
        console.log(err)
      })
    },
    getCiSchemaGroupData () {
      ciSChemaGroup().then((res) => {
        this.groupSchemaData = res.data.data
        var activeName = []
        var index
        for (index in this.groupSchemaData) {
          activeName.push(this.groupSchemaData[index].id)
        }
        this.activeName = activeName
        console.log(activeName)
      }).catch((err) => {
        console.log(err)
      })
    },
    handleSettingChange ({
      fields,
      size
    }) {
      this.setting.size = size
      this.setting.selectedFields = fields
    },
    changePage (page) {
      this.pagingConfigTwo.current = page
      this.getSub()
    },
    changeLimit (limit) {
      this.pagingConfigTwo.limit = limit
      this.getSub()
    },
    resetSub (props, rows) {
      console.log(props, rows)
      this.customSettings.isShow = true
      this.customSettings.title = '编辑事件订阅'
      this.formData = props
    },
    removeSub (props, rows) {
      console.log(props, rows)
      deleteSub(props.id).then((res) => {
        this.$bkMessage({
          theme: 'success',
          message: '移除成功'
        })
        this.getSubData()
      }).catch((err) => {
        console.log(err)
      })
    },
    clearFormData () {
      this.customSettings.isShow = false
      this.customSettings.title = '创建事件订阅'
      this.formData = {
        'name': '',
        'subscriber': '',
        'notify_url': '',
        'success_code': '',
        'timeout': '',
        'meta': {}
      }
    },
    submitData () {
      if (this.formData['id']) {
        updateSub(this.formData['id'], this.formData).then((res) => {
          this.$bkMessage({
            theme: 'success',
            message: '修改成功'
          })
          this.customSettings.isShow = false
          this.getSubData()
          this.formData = {
            'name': '',
            'subscriber': '',
            'notify_url': '',
            'success_code': '',
            'timeout': '',
            'meta': {}
          }
        }).catch((err) => {
          console.log(err)
        })
      } else {
        createSub(this.formData).then((res) => {
          this.$bkMessage({
            theme: 'success',
            message: '创建成功'
          })
          this.customSettings.isShow = false
          this.getSubData()
        }).catch((err) => {
          console.log(err)
        })
      }
    }
  }
}
</script>

<style>
</style>
