<template>
  <div>
    <div>
      <div style="font-size: 20px;margin-left: 12px;margin: 14px;">资源目录</div>
      <bk-divider></bk-divider>
      <div>
        <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:left;margin-left: 20px;"></bk-input>
      </div>
    </div>
    <div>
      <div class="container">
        <div v-for="(schemaGroup,index) in schemaGroupList" :key="'schemaGroup'+index" class="item">
          <div class="item-title">{{schemaGroup.alias}}</div>
          <bk-divider></bk-divider>
          <div v-for="(schema,index) in schemaGroup.schema" :key="'schema'+index" class="field">
            <i :class="schema.icon_url" class="item-icon" />
            <div class="item-content" @click="redirctResource(schema)">{{schema.alias}}</div>
            <bk-icon :type="schema.is_show?'heart-shape':'heart'" :class="schema.is_show?'item-fav-display':'item-fav'"
              @click="handleFav(schema.id,schema.is_show)" />
          </div>
        </div>

        <span class="item break"></span>
        <span class="item break"></span>
        <span class="item break"></span>
      </div>
    </div>
  </div>
</template>

<script>
import {
  ciSChemaGroup,
  patchCiSChema
} from '@/api/api'
export default {
  name: 'resource',
  inject: ['getCISchemaFuc'],
  mounted () {
    this.getCiSChemaGroup()
  },
  data () {
    return {
      schemaGroupList: []
    }
  },
  methods: {
    getCiSChemaGroup () {
      ciSChemaGroup().then((response) => {
        this.schemaGroupList = response.data.data
      }).catch((error) => {
        console.log('2', error)
      })
    },
    handleFav (id, isShow) {
      console.log('item', id, isShow)
      patchCiSChema(id, {
        is_show: !isShow
      }).then((response) => {
        this.$bkMessage({
          theme: 'success',
          message: isShow ? '取消导航成功' : '添加导航成功'
        })
        this.getCiSChemaGroup()
        this.getCISchemaFuc()
      }).catch((error) => {
        this.$bkMessage({
          theme: 'error',
          message: error.message
        })
      })
    },
    redirctResource (schema) {
      this.$router.push({
        'name': 'resources',
        'params': {
          'schemaID': schema.id,
          'name': schema.alias,
          'fields': schema.field
        }
      })
    }
  }
}
</script>

<style scoped>
  .item-icon {
    margin-right: 12px;
    color: #3A84FF;
  }

  .item-fav {
    margin: auto auto;
    display: none;
    font-size: 14px !important;
    line-height: 14px;
  }

  .item-fav-display {
    margin: auto auto;
    display: block;
    font-size: 14px !important;
    line-height: 14px;
    color: #FFB400;
  }

  .field:hover {
    color: lightblue;
    cursor: pointer;
  }

  .field:hover .item-fav {
    display: block;
  }

  .field {
    display: flex;
    margin-bottom: 12px;
  }

  .container {
    display: flex;
    flex-flow: column wrap;
    align-content: space-between;
    /* 容器必须有固定高度
     * 且高度大于最高的列高 */
    height: 960px;

    /* 非必须 */
    /* background-color: #f7f7f7; */
    border-radius: 3px;
    padding: 20px;
    width: 100%;
    margin: 20px auto;
    counter-reset: items;
  }

  .item {
    width: 24%;
    /* 非必须 */
    position: relative;
    margin-bottom: 2%;
    border-radius: 3px;
    background-color: white;
    border: 1px solid #ebf0f5;
    box-shadow: 0 2px 2px rgba(0, 90, 250, 0.05),
      0 4px 4px rgba(0, 90, 250, 0.05),
      0 8px 8px rgba(0, 90, 250, 0.05),
      0 16px 16px rgba(0, 90, 250, 0.05);
    color: #63656E;
    padding: 15px;
    box-sizing: border-box;
  }

  /* 将内容块重排为4列 */
  .item:nth-of-type(4n+1) {
    order: 1;
  }

  .item:nth-of-type(4n+2) {
    order: 2;
  }

  .item:nth-of-type(4n+3) {
    order: 3;
  }

  .item:nth-of-type(4n) {
    order: 4;
  }

  /* 强制换列 */
  .break {
    flex-basis: 100%;
    width: 0;
    border: 0px solid transparent;
    margin: 10px;
    content: "";
    padding: 0;
  }

  .item-title {
    font-weight: bolder;
    font-size: 14px;
  }

  .item-content {
    font-size: 14px;
  }
</style>
