<template>
    <section
        :id="id"
        class="featurette3"
        :aria-labelledby="id"
    >
        <h2
            :id="id"
            tabindex="0"
            role="heading"
            aria-level="2"
        >
            {{ heading }}
        </h2>
        <p>{{ text }}</p>
        <div
            v-if="images && images.length"
            class="row featurette3-row"
        >
            <div
                v-for="(img, idx) in images"
                :key="img.src"
                class="thumbnail featurette-image-block"
                :class="{ 'featurette3-first-block': idx === 0 }"
            >
                <img
                    :src="img.src"
                    :alt="img.alt"
                    :aria-labelledby="img.ariaLabelledby"
                />
                <div class="caption"></div>
            </div>
        </div>
        <p v-if="extra">
            <span class="tbc-highlight">{{ extra }}</span>
        </p>
        <slot></slot>
    </section>
</template>

<script setup>
defineProps({
    id: { type: String, default: "" },
    heading: { type: String, default: "" },
    text: { type: String, default: "" },
    images: { type: Array, default: () => [] },
    extra: { type: String, default: "" },
});
</script>

<style scoped>
.featurette3 {
    margin-bottom: 2rem;
}
</style>
