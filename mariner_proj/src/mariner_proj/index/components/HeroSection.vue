<template>
    <section
        class="hero"
        aria-labelledby="main-title"
    >
        <div class="row featurette1">
            <div class="featurette1-left-container">
                <h1 id="main-title">{{ title }}</h1>
                <p class="lead">{{ lead }}</p>
            </div>
            <div class="featurette1-right-container pull-right">
                <img
                    :src="image"
                    alt="Photo of the London landscape"
                    class="img-rounded img-responsive"
                />
            </div>
        </div>
    </section>
</template>

<script setup>
defineProps({
    title: { type: String, default: "" },
    lead: { type: String, default: "" },
    image: { type: String, default: "" },
});
</script>

<style scoped>
.hero {
    margin-bottom: 2rem;
}
.img-responsive {
    max-width: 100%;
    height: auto;
}
</style>
