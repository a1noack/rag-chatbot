<template>
  <main class="p-6 max-w-3xl mx-auto space-y-4">
    <div v-for="(m,i) in messages" :key="i" :class="m.role">
      <p class="inline-block rounded-lg px-3 py-2"
         :class="m.role==='user'?'bg-blue-100':'bg-gray-100'">
        {{ m.text }}
      </p>
    </div>

    <form @submit.prevent="send">
      <input v-model="input"
             class="border w-full p-2 rounded"
             placeholder="Ask me anything…" />
    </form>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import axios      from 'axios'

const input    = ref('')
const messages = ref([])

async function send() {
  if (!input.value.trim()) return
  messages.value.push({ role:'user', text: input.value })
  const q = input.value; input.value = ''

  const { data } = await axios.post('http://localhost:8000/chat', {
    session_id: 'demo', message: q
  })
  messages.value.push({ role:'assistant', text: data.answer })
}
</script>

<style>
.user       { text-align: right; }
.assistant  { text-align: left;  }
</style>
