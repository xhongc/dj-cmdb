<template>
  <div>
    <div class="sub-title">{{this.$route.params.name}}</div>
    <bk-divider></bk-divider>
    <div style="margin-left: 10px;margin-right: 10px;">
      <bk-button theme="primary" @click="customSettings.isShow=true">新建</bk-button>
      <bk-button>导入</bk-button>
      <bk-button :disabled="!isSelectColumn">导出</bk-button>
      <bk-button :disabled="!isSelectColumn">删除</bk-button>
      <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
    </div>
    <!-- 新建ci的侧边栏 -->
    <bk-sideslider :is-show.sync="customSettings.isShow" :quick-close="true" :width="customSettings.width"
      :before-close="clearFormData">
      <div slot="header">{{ customSettings.title }}</div>
      <div class="p20" slot="content">
        <bk-form :label-width="200" form-type="vertical" class="form">
          <bk-exception v-if="fieldList.length===0" class="exception-wrap-item exception-part" type="empty" scene="part">
            <router-link :to="{ name: 'model_detail', params: { schemaID: this.pk }}">请先创建模型字段</router-link>
          </bk-exception>
          <bk-form-item v-for="(field,index) in fieldList" :key="'field'+index" :label="field.label" :required="true"
            class="field-form">
            <bk-input v-model="formData[field.id]"></bk-input>
          </bk-form-item>

          <div style="flex-basis: 100%;position:fixed; right:0px; bottom:5px; z-index:999;width: 500px;background-color: white;">
            <bk-divider style="margin: 0 0 8px;"></bk-divider>
            <bk-button v-if="fieldList.length!==0" ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="submitData">提交</bk-button>
            <bk-button v-if="fieldList.length!==0" ext-cls="mr5" theme="default" title="取消" @click.stop.prevent="clearFormData">取消</bk-button>
          </div>
        </bk-form>
      </div>
    </bk-sideslider>
    <bk-table style="margin-top: 15px;" :data="ciData" :size="setting.size" @cell-click="cellDetail" @selection-change="selectColumn">
      <bk-table-column type="selection" width="50px" v-if="this.fieldList.length !== 0"></bk-table-column>
      <bk-table-column label="ID" prop="ci_id" class-name="id-index" v-if="this.fieldList.length !== 0"></bk-table-column>
      <bk-table-column v-for="field in setting.selectedFields" :key="field.id" :label="field.label" :prop="field.id">
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
  </div>
</template>

<script>
import {
  getCI,
  createCi
} from '@/api/api'
export default {
  name: 'resources',
  data () {
    const fields = [{
      id: 'ci_id',
      label: '暂无数据'
    }]
    return {
      pk: this.$route.params.schemaID,
      ciData: [],
      setting: {
        max: 3,
        fields: fields,
        selectedFields: fields.slice(0, 3),
        size: 'small'
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
      customSettings: {
        isShow: false,
        title: '创建' + this.$route.params.name,
        width: 500
      },
      formData: {},
      isSelectColumn: false
    }
  },
  methods: {
    getCIData () {
      getCI(this.pk, {
        page: this.pagingConfigTwo.current,
        page_size: this.pagingConfigTwo.limit
      }).then((res) => {
        this.ciData = res.data.data.item
        this.pagingConfigTwo.count = res.data.data.count
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
      this.getCIData()
    },
    changeLimit (limit) {
      this.pagingConfigTwo.limit = limit
      this.getCIData()
    },
    submitData () {
      createCi({
        schema_id: this.pk,
        field_value: this.formData
      }).then((res) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.customSettings.isShow = false
        this.getCIData()
        this.formData = {}
      }).catch((err) => {
        this.$bkMessage({
          theme: 'error',
          message: err.message
        })
      })
    },
    cellDetail (raw, column, cell, event, rowIndex, columnIndex) {
      if (columnIndex !== 1) {
        return false
      }
      var paramsData = this.$route.params
      paramsData['raw'] = raw
      this.$router.push({name: 'inst_detail', params: paramsData})
    },
    clearFormData () {
      this.customSettings.isShow = false
      this.formData = {}
    },
    selectColumn (row) {
      if (row.length >= 1) {
        this.isSelectColumn = true
      } else {
        this.isSelectColumn = false
      }
    }

  },
  mounted () {
    if (this.fieldList.length !== 0) {
      this.setting.fields = this.fieldList
      this.setting.selectedFields = this.fieldList.slice(0, 4)
    }
    this.getCIData()
  },
  computed: {
    fieldList () {
      var index
      var fields = []
      for (index in this.$route.params.fields) {
        fields.push({
          id: this.$route.params.fields[index].name,
          label: this.$route.params.fields[index].alias
        })
      }
      return fields
    }
  }
}
</script>

<style>
  .sub-title {
    font-size: 20px;
    margin-left: 12px;
    margin: 14px;
    height: 23px;
  }

  .form {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
  }

  .field-form {
    width: 42%;
    margin-right: 30px;
    margin-top: 8px;
  }
  .id-index {
    color: #3A84FF;
    cursor: pointer;
  }
</style>
