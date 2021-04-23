<template>
  <div>
    <div style="display: flex;">
      <bk-icon type="arrows-left" style="font-size: 40px;color: #3A84FF;cursor: pointer;" @click="backTo" />
      <div style="font-size: 18px;margin-top: auto;margin-bottom: auto;">实例详情</div>
    </div>
    <bk-divider style="margin: auto;"></bk-divider>
    <div style="height: 70px;background: #ebf4ff;">
      <div style="display: flex;height: 100%;">
        <i class="cmdb-mokuai inst-icon" />
        <div class="inst-title">
          <div>{{this.$route.params.name}}</div>
          <div>【{{this.$route.params.raw[Object.keys(this.$route.params.raw)[0]]}}】</div>
        </div>
      </div>
    </div>
    <bk-tab :active.sync="active" type="unborder-card" @tab-change="handleTab">
      <bk-tab-panel v-for="(panel, index) in panels" v-bind="panel" :key="index">
        <div v-if="active==='attr'">
          <bk-button theme="primary" @click="modifyMode">{{modifyButtonTitle}}</bk-button>
          <bk-button theme="primary" @click="submitData" v-if="isModify">提交</bk-button>
          <bk-form :label-width="80" form-type="horizontal" class="form form-cls">
            <div v-for="(field,index) in fieldList" :key="'field'+index" class="cell-form">
              <label>{{field.label}}</label>
              <input v-model="formData[field.id]" :readonly="!isModify" :class="isModify?'input-cls-modify':'input-cls'">
            </div>
          </bk-form>
        </div>
        <div v-else>
          <bk-button theme="primary" @click="createCIRelation">新建关联</bk-button>
          <div class="bk-button-group btn-group">
            <bk-button @click="groupSetting1.selected = 'list'" :class="groupSetting1.selected === 'list' ? 'is-selected' : ''">列表</bk-button>
            <bk-button @click="groupSetting1.selected = 'topo'" :class="groupSetting1.selected === 'topo' ? 'is-selected' : ''">拓扑</bk-button>
          </div>
          <bk-collapse v-model="activeName" v-for="(relation,index) in ciRelationData" :key="'index'+index" @item-click="handlerClick">
            <bk-collapse-item :name="index">
              {{relation.relation_name}}-({{relation.child_ids.length}})
              <div slot="content" class="f13">{{relation.child_ids}}</div>
            </bk-collapse-item>
          </bk-collapse>
        </div>
      </bk-tab-panel>
    </bk-tab>
  </div>
</template>

<script>
import {
  createCi,
  getCIRelation
} from '@/api/api'
export default {
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
  },
  data () {
    return {
      panels: [{
        name: 'attr',
        label: '属性'
      },
      {
        name: 'relation',
        label: '关联'
      }
      ],
      active: 'attr',
      formData: this.$route.params.raw,
      isModify: false,
      modifyButtonTitle: '编辑',
      groupSetting1: {
        selected: 'list'
      },
      activeName: [],
      ciRelationData: []
    }
  },
  methods: {
    backTo () {
      this.$router.push({
        'name': 'resources',
        'params': {
          'schemaID': this.$route.params.schemaID,
          'name': this.$route.params.name,
          'fields': this.$route.params.fields
        }
      })
    },
    handleTab () {
      console.log(this.$route.params.raw)
      if (this.active === 'relation') {
        this.getCIRelationData()
      }
    },
    modifyMode () {
      this.isModify = !this.isModify
      this.modifyButtonTitle = this.isModify ? '取消编辑' : '编辑'
    },

    submitData () {
      createCi({
        schema_id: this.$route.params.schemaID,
        field_value: this.formData
      }).then((res) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.isModify = false
        this.modifyButtonTitle = '编辑'
      }).catch((err) => {
        this.$bkMessage({
          theme: 'error',
          message: err.message
        })
      })
    },
    createCIRelation () {
      console.log(123)
    },
    getCIRelationData () {
      getCIRelation({
        'parent_id': this.$route.params.raw['ci_id']
      }).then((res) => {
        this.ciRelationData = res.data.data
        // this.activeName.push()
      }).catch((err) => {
        console.log(err)
      })
    },
    handlerClick (val) {
      console.log(val)
    }
  }
}
</script>

<style>
  .inst-icon {
    margin: auto 20px;
    font-size: 30px;
    color: gray;
  }

  .inst-title {
    display: flex;
    margin: auto 0;
    color: gray;
  }

  .form-cls {
    margin: 20px 40px;
    display: flex;
    flex-flow: wrap;
  }

  .input-cls {
    -webkit-box-sizing: border-box;
    height: 32px;
    line-height: normal;
    color: #63656e;
    background-color: #fafbfd;
    border-radius: 2px;
    width: 100%;
    font-size: 14px;
    box-sizing: border-box;
    border: 0px;
    padding: 0 10px;
    text-align: left;
    vertical-align: middle;
    outline: none;
    resize: none;
    -webkit-transition: border .2s linear;
    transition: border .2s linear;
  }

  .input-cls-modify {
    -webkit-box-sizing: border-box;
    height: 32px;
    line-height: normal;
    color: #63656e;
    background-color: #fff;
    border-radius: 2px;
    width: 50%;
    font-size: 14px;
    box-sizing: border-box;
    border: 1px solid #c4c6cc;
    padding: 0 10px;
    text-align: left;
    vertical-align: middle;
    outline: none;
    resize: none;
    -webkit-transition: border .2s linear;
    transition: border .2s linear;
  }

  .bk-form .bk-label {
    text-align: left;
  }

  .cell-form {
    width: 34%;
    display: flex;
    margin: 10px 0;
  }

  .cell-form label {
    margin: auto 0;
    width: 100px;
  }

  .cell-form input {
    margin: auto 0;
  }

  .cell-form label::after {
    content: "：";
  }

  .btn-group {
    float: right;
  }
  .bk-collapse-item-header {
    background-color: #dcdee5;
  }
</style>
