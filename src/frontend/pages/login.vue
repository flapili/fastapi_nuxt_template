<template>
    <div class="background">
        <el-card class="center">
            <el-form ref="form" :rules="rules" :model="form" @submit.prevent.native="login">
                <el-form-item prop="username">
                    <el-input v-model="form.username" placeholder="nom d'utilisateur" @keypress.enter.native="login"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="form.password" show-password placeholder="mot de passe" @keypress.enter.native="login"></el-input>
                </el-form-item>
            </el-card>
    </div>
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
                        const r = await this.$axios.post(`${this.$config.api_url}/user/login`, {
                            username: this.form.username,
                            password: this.form.password,
                        })
                        alert("login")
                    }
                    catch (err) {
                        console.log(err)
                        if (!err.response || err.response.status >= 500) {
                            this.$message.error('Serveurs injoignables. Réessayer plus tard');
                        }
                        else if (err.response.status === 400) {
                            this.$message.error('Mauvais identifiants');
                        }

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
    .background {
        background-color: #808080;
        height: 100vh;
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
    }
</style>