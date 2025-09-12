<template>
    <header>
        <nav
            class="navbar"
            aria-label="Main navigation"
        >
            <div class="container">
                <div class="navbar-header">
                    <a
                        href="/"
                        class="navbar-brand"
                        aria-label="Link to homepage"
                    >
                        <img
                            src="/static/img/HE_Logo_RGB.svg"
                            alt="Historic England logo"
                            height="48"
                        />
                    </a>
                </div>
                <!-- Navigation items can be added here -->
            </div>
        </nav>
    </header>
</template>

<script setup>
defineProps({
    appTitle: {
        type: String,
        default: "",
    },
});
</script>

<style scoped>
.navbar {
    background: #fff;
    border-bottom: 1px solid #ccc;
}
.navbar-brand img {
    max-height: 48px;
}
</style>
