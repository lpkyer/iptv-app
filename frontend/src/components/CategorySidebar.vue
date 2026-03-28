<template>
  <div class="flex flex-col h-full border-r border-dark-600 bg-dark-800">
    <div class="px-4 py-3 border-b border-dark-600">
      <h2 class="text-xs font-semibold text-gray-500 uppercase tracking-widest">Catégories</h2>
    </div>
    <div class="flex-1 overflow-y-auto py-2">
      <!-- Toutes les chaînes -->
      <button
        class="w-full text-left px-4 py-2.5 text-sm transition-colors hover:bg-dark-600"
        :class="selected === null ? 'text-white font-medium bg-dark-600' : 'text-gray-400'"
        @click="$emit('select', null)"
      >
        Toutes les chaînes
      </button>

      <!-- Par catégorie -->
      <button
        v-for="cat in categories"
        :key="cat.category_id"
        class="w-full text-left px-4 py-2.5 text-sm transition-colors hover:bg-dark-600 truncate"
        :class="selected === cat.category_id ? 'text-white font-medium bg-dark-600' : 'text-gray-400'"
        @click="$emit('select', cat.category_id)"
      >
        {{ cat.category_name }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  categories: { type: Array, default: () => [] },
  selected: { type: String, default: null }
})
defineEmits(['select'])
</script>
