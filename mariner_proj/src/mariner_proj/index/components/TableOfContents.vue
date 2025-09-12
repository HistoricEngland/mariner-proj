<template>
    <nav
        aria-label="On this page"
        class="featurette2-sub-container"
    >
        <h2>On this page</h2>
        <ol>
            <li
                v-for="section in sections"
                :key="section.id"
            >
                <a :href="`#${section.id}`">{{ section.label }}</a>
            </li>
        </ol>
    </nav>
</template>

<script setup>
defineProps({
    sections: {
        type: Array,
        default: () => [],
    },
});
</script>

<style scoped>
.featurette2-sub-container {
    margin-bottom: 2rem;
}
</style>
