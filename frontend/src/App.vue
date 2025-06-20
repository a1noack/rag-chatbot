<template>
  <main class="container mx-auto flex flex-col h-screen px-4 py-4">
    <!-- Title -->
    <header class="mb-6 text-center">
      <h1 class="text-4xl font-bold">Wikipedia RAG Chatbot</h1>
      <p class="text-gray-400 mt-2">Ask anything about Wikipedia using our AI-powered RAG backend</p>
    </header>

    <!-- Chat history -->
    <section class="flex-1 overflow-y-auto space-y-4 mb-6">
      <div v-for="(m, i) in messages" :key="i" :class="m.role">
        <p class="inline-block rounded-lg px-4 py-2"
           :class="m.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'">
          {{ m.text }}
        </p>
      </div>
    </section>

    <!-- Input area -->
    <form @submit.prevent="send" class="mt-auto">
      <div class="flex space-x-2">
        <input v-model="input"
               class="flex-1 border border-gray-300 p-4 h-12 text-lg rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
               placeholder="Ask me anything…" />
        <button type="submit"
                class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
          Send
        </button>
      </div>
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
