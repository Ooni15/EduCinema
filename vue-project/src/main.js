import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
export default pinia // vue Persist는 애플리케이션 상태를 특정 스토리지에 저장
// app.use(createPinia())
app.use(pinia)
app.use(router)

app.mount('#app')
