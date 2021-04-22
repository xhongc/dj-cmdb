<template>
  <div>
    <div class="login-card">
      <div class="login-header">
        <img src="../assets/logo_re.svg" style="width: 50px;height: 50px;" />
        <div class="title">配置平台</div>
      </div>
      <bk-divider></bk-divider>
      <div class="username">
        <bk-input :placeholder="'账号'" :left-icon="'bk-icon icon-user'" v-model="username" :font-size="'medium'" size="large">
        </bk-input>
      </div>
      <div class="password">
        <bk-input :type="'password'" :placeholder="'密码'" v-model="password" :left-icon="'bk-icon icon-unlock'"
          :font-size="'medium'" size="large"></bk-input>
      </div>
      <div class="login-button">
        <bk-button theme="primary" title="主要按钮" class="mr10" style="width: 300px;height: 38px;" @click='login'>登录</bk-button>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getToken
} from '@/api/api'
import cookie from '@/store/cookie'

export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login () {
      var that = this
      getToken({'username': this.username, 'password': this.password}).then((res) => {
        this.$bkMessage({
          theme: 'success',
          message: '登录成功'
        })
        // 本地存储用户信息
        cookie.delCookie('token')
        cookie.setCookie('token', res.data.token, 1)
        console.log(cookie.getCookie('token'))
        // 存储在store
        // 更新store数据
        console.log(that)
        that.$store.commit('setUserInfo', res.data.token)
        // 跳转到首页页面
        this.$router.push({name: 'home'})
      }).catch((err) => {
        console.log(err)
      })
    }
  }
}
</script>

<style>
  .login-card {
    width: 450px;
    height: 378px;
    border: 1px solid lightgrey;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
  }

  .login-header {
    display: flex;
    margin: 35px auto;
    width: 200px;
  }

  .title {
    margin: auto 20px;
    font-size: 25px;
    color: #283f8a;
  }

  .username {
    margin: 40px auto 20px;
    width: 300px;
  }

  .password {
    width: 300px;
    margin: 20px auto;
  }

  .password .control-icon {
    cursor: pointer;
  }

  .login-button {
    width: 300px;
    margin: 20px auto;
  }
</style>
