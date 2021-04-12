<template>
  <div>
    <div style="font-size: 20px;margin-left: 12px;margin: 14px;">模型</div>
    <bk-divider></bk-divider>
    <div class="wrapper flex">
      <bk-container flex :col="12">
        <bk-row>
          <bk-col :span="4">
            <bk-button @click="createModelSettings.visible = true" :theme="'primary'" :title="'新建模型'" class="mr10">
              新建模型
            </bk-button>
            <bk-dialog v-model="createModelSettings.visible" title="新建模型" :header-position="createModelSettings.headerPosition"
              :width="createModelSettings.width" @confirm="postCreateModel">
              <div class="select-icon-parent" @click="createModelIconSettings.visible = true">
                <i :class="[icon_index_name,{'select-icon':true}]"></i>
              </div>
              <div>所属分组</div>
              <bk-select :disabled="false" :search-with-pinyin="true" v-model="postModelData.group" style="width: 250px;"
                ext-cls="select-custom" ext-popover-cls="select-popover-custom" searchable>
                <bk-option v-for="item in this.groupList" :key="item.id" :id="item.id" :name="item.alias">
                </bk-option>
              </bk-select>
              <div>唯一标识</div>
              <bk-input :placeholder="'请输入唯一标识'" style="margin-bottom: 15px;" v-model="postModelData.name">
              </bk-input>
              <div>模型名称</div>
              <bk-input :placeholder="'请输入模型名称'" style="margin-bottom: 15px;" v-model="postModelData.alias">
              </bk-input>
            </bk-dialog>
            <bk-dialog v-model="createModelIconSettings.visible" title="新建模型" :header-position="createModelIconSettings.headerPosition"
              :width="createModelIconSettings.width" @confirm="selectIcon">
              <div class="icon-group">
                <div v-for="(icon,index) in icons" :class="{'active-icon':icon_index===index}" :key="'index'+index"
                  class="icon-cell" @click="clickIcon(index)">
                  <i :class="icon" class="icon-cell-2"></i>
                </div>
              </div>
            </bk-dialog>
            <bk-button @click="createGroupSettings.visible = true" :theme="'default'" :title="'新建分组'" class="mr10">
              新建分组
            </bk-button>
            <bk-dialog v-model="createGroupSettings.visible" title="新建分组" :header-position="createGroupSettings.headerPosition"
              :width="createGroupSettings.width" @confirm="postCreateGroup">
              <div>唯一标识</div>
              <bk-input :placeholder="'请输入唯一标识'" style="margin-bottom: 15px;" v-model="postGroupData.name">
              </bk-input>
              <div>分组名称</div>
              <bk-input :placeholder="'请输入分组名称'" style="margin-bottom: 15px;" v-model="postGroupData.alias">
              </bk-input>
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
    </div>
    <bk-collapse v-model="activeName">
      <div v-for="(group,index) in groupList" :key="'group'+index">
        <bk-collapse-item :name="group.id" class="ci-group">
          {{group.alias}}
          <div style="color: lightgray;float: right;"> ({{group.schema.length}})</div>
          <div slot="content" class="f13">
            <div style="display: flex;width: 100%;flex-wrap: wrap;">
              <div v-for="(ci,index) in group.schema" :key="'ci'+index" class="card-demo" @click="handleSchemaDetail(ci.id)">
                <bk-card title="卡片标题" :show-foot="false" :show-head="false" style="width: 100%;height: 100%;">
                  <div style="display: flex;" class="a-card">
                    <i :class="ci.icon_url" style="font-size: 36px;line-height: 72px;margin-left: 10px;color: #3A84FF;" />
                    <div style="margin-left: 26px;">
                      <p>{{ci.alias}}</p>
                      <p style="color: lightgray;">{{ci.name}}</p>
                    </div>
                    <bk-icon type="order" style="font-size: 24px;line-height: 64px;margin-left: 60px;" class="detail" />
                  </div>
                </bk-card>
              </div>
            </div>
          </div>
        </bk-collapse-item>
      </div>
    </bk-collapse>
  </div>
</template>

<script>
import {
  ciSChemaGroup,
  ciSChema,
  CreateSChemaGroup
} from '@/api/api'
export default {
  name: 'model-management',
  mounted () {
    this.getCiSchemaGroup()
  },
  data () {
    return {
      activeName: [],
      value: '',
      select_group: '',
      groupList: [],
      icons: ['cmdb-nginx', 'cmdb-tomcat', 'cmdb-apache', 'cmdb-windows', 'cmdb-Redis', 'cmdb-yingyong', 'cmdb-linux',
        'cmdb-nginx1', 'cmdb-jiqun', 'cmdb-Vue', 'cmdb-zhujizu', 'cmdb-yingyong1', 'cmdb-macos', 'cmdb-redis',
        'cmdb-mokuai', 'cmdb-MySQL', 'cmdb-db_mysql_database', 'cmdb-app_mw_weblogic_domain', 'cmdb-yunzhuji',
        'cmdb-vue', 'cmdb-zhuji', 'cmdb-cluster', 'cmdb-zuixing-86', 'cmdb-MySQL1', 'cmdb-bxl-django',
        'cmdb-ecs-disk', 'cmdb-xingzhuang', 'cmdb-xitongyunweibumen', 'cmdb-xitongyunweidakaiwenjianjia',
        'cmdb-xitongyunweitianjia', 'cmdb-xitongyunweiwenjian', 'cmdb-xitongyunweiwenjianjia01',
        'cmdb-xitongyunweiwenjianjia02', 'cmdb-xitongyunweiyonghu', 'cmdb-xitongyunweibaocunshouquan',
        'cmdb-yunweiguanli', 'cmdb-zhinengyunwei', 'cmdb-yunweiguanli1', 'cmdb-yunweiguanli2', 'cmdb-zhihuiyunwei',
        'cmdb-yunweiguanli3', 'cmdb-nav-oper-center', 'cmdb-oper-apply', 'cmdb-oper-equip', 'cmdb-special-oper',
        'cmdb-batch-oper', 'cmdb-nav-set-oper', 'cmdb-maintenance', 'cmdb-nav-oper-center-t', 'cmdb-cheliangyunwei',
        'cmdb-yunweiguanli4', 'cmdb-zhongduanyunwei', 'cmdb-erji-yunweibaobiao', 'cmdb-yunweiguanli5',
        'cmdb-yunweirenyuan', 'cmdb-lvzhou_yunwei', 'cmdb-navicon-ywpz', 'cmdb-yunweizhongxinzhihangjilu',
        'cmdb-yunweizhongxinzusaiduilie', 'cmdb-yunweizhongxinzichanzonglan', 'cmdb-yunwei', 'cmdb-oper-auto-1',
        'cmdb-oper-auto', 'cmdb-wulumuqishigongandashujuguanlipingtai-ico-', 'cmdb-icon-', 'cmdb-xitongyunwei',
        'cmdb-tab_yunwei', 'cmdb-yunwei1', 'cmdb-yunweiguanli6', 'cmdb-yunweiguanli7', 'cmdb-yunwei2',
        'cmdb-yunweizhongxin', 'cmdb-icon_xinyong_xianxing_jijin-', 'cmdb-yunweizhongxin1', 'cmdb-yunweiguanli8',
        'cmdb-yunweiguanli9', 'cmdb-yunwei3', 'cmdb-yunweigongju', 'cmdb-yunwei4', 'cmdb-shujuyunwei',
        'cmdb-yunweiguanli10', 'cmdb-yunweigongsi', 'cmdb-yunweiguanli11', 'cmdb-shebeiyunweiyujingshezhi',
        'cmdb-yunwei-xitongjiance', 'cmdb-yunwei-jiancebaogao', 'cmdb-yunwei-yunweirizhi', 'cmdb-54yunweibaobiao',
        'cmdb-quanwangyunweifuwuliucheng_xianxing_-01-01'
      ],
      icon_index: 0,
      icon_index_name: 'cmdb-tomcat',
      createModelSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      createModelIconSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      createGroupSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      postModelData: {
        icon_url: 'cmdb-tomcat',
        group: '',
        name: '',
        alias: ''
      },
      postGroupData: {
        name: '',
        alias: ''
      }
    }
  },
  methods: {
    handlerIconClick () {
      console.log('1')
    },
    getCiSchemaGroup () {
      ciSChemaGroup().then((response) => {
        this.groupList = response.data.data
        var activeName = []
        var index
        for (index in this.groupList) {
          activeName.push(this.groupList[index].id)
        }
        this.activeName = activeName
      }).catch((error) => {
        console.log(error)
      })
    },
    postCreateModel () {
      this.postModelData['icon_url'] = this.icon_index_name
      ciSChema(this.postModelData).then((response) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.getCiSchemaGroup()
      }).catch((error) => {
        this.$bkMessage({
          theme: 'error',
          message: error.message
        })
      })
    },
    selectIcon () {
      this.icon_index_name = this.icons[this.icon_index]
    },
    postCreateGroup () {
      CreateSChemaGroup(this.postGroupData).then((response) => {
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        })
        this.getCiSchemaGroup()
      }).catch((error) => {
        this.$bkMessage({
          theme: 'error',
          message: error.message
        })
      })
    },
    handleSchemaDetail (schemaID) {
      console.log('schemaID::', schemaID)
      this.$router.push({
        name: 'model_detail',
        params: {
          'schemaID': schemaID
        }
      })
    },
    clickIcon (index) {
      this.icon_index = index
    }
  }
}
</script>

<style>
  .detail {
    display: none;
    transition: all.7s;
  }

  .detail:hover {
    color: skyblue;
  }

  .a-card:hover .detail {
    display: block;
    background: skyblue;
    flex: 1;
  }

  .select-icon {
    margin: 0 auto;
    font-size: 36px;
    line-height: 72px;
    color: #87CEEB;
  }

  .select-icon-parent {
    text-align: center;
    border: 1px solid lightgray;
    width: 25%;
    margin: 0 auto;
    border-radius: 50px;
    cursor: pointer;
  }

  .select-icon-parent:hover {
    background-color: lavender;
  }

  .icon-cell {
    font-size: 30px;
    margin-right: 20px;
    margin-top: 10px;
    width: 40px;
    height: 40px;
    position: relative;
  }

  .icon-cell:hover {
    background: #ebf4ff;
    color: #3a84ff;
  }
  .icon-cell-2 {
    font-size: 30px;
    margin-left: 4px;
    margin-right: 20px;
    width: 40px;
    height: 40px;
  }
  .icon-group {
    display: flex;
    flex-flow: wrap;
    height: 320px;
    overflow: auto;
  }

  .active-icon {
    color: #3a84ff;
    box-shadow:0 2px 7px 0 rgba(85,110,97,0.35);
    border-radius:7px;
    border:1px solid #3a84ff;
  }

  .active-icon:before {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    border: 10px solid #4ABE84;
    border-top-color: transparent;
    border-left-color: transparent;
  }

  .active-icon:after {
    content: '';
    width: 5px;
    height: 8px;
    position: absolute;
    right: 2px;
    bottom: 4px;
    border: 2px solid #fff;
    border-top-color: transparent;
    border-left-color: transparent;
    transform: rotate(45deg);
  }
</style>
