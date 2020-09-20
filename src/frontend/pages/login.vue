<template>
  <el-card class="center">
    <el-form ref="form" :rules="rules" :model="form" @submit.prevent.native="login">
        <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="nom d'utilisateur" @keypress.enter.native="login"></el-input>
        </el-form-item>
        <el-form-item prop="password">
            <el-input v-model="form.password" show-password placeholder="mot de passe" @keypress.enter.native="login"></el-input>
        </el-form-item>
    </el-card>
</template>

<script>
    export default {

        data() {
            return {
                form: {
                    username: "",
                    password: "",
                },
                rules: {
                    username: {
                        required: true, message: "Nom d'utilisateur manquant", trigger: "blur"
                    },
                    password: {
                        required: true, message: "Mot de passe manquant", trigger: "blur"
                    },
                },
            }
        },

        methods: {
            async login() {
                try {
                    await this.$refs["form"].validate()
                    try {
                        r = await this.$axios.post("api/login", {
                            username: this.username,
                            password: this.password,
                        })
                        console.log(r)
                    }
                    catch (err) {
                        console.log(err)
                    }
                }
                catch(err) {} // invalid form
            },
        }
    }
</script>

<style scoped>
    .center {
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        position: absolute;
        min-width: fit-content;
    }

</style>
