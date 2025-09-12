<template>
    <footer>
        <div class="footer-top">
            <div class="container">
                <div class="row footer-top-first-row">
                    <div class="col-sm-4">
                        <a href="#"></a>
                    </div>
                    <div class="col-sm-5">
                        <a href="#"></a>
                    </div>
                    <div class="col-sm-3">
                        <a href="#"></a>
                    </div>
                </div>
                <div>
                    <div class="col-xs-8 col-sm-9 nmhr-text-container">
                        <p class="nmhr-title">
                            National Marine Historic Environment Record<br />
                        </p>
                    </div>
                    <div class="col-xs-4 col-sm-3 footer-top-contact-details">
                        <p><strong>Contact Us</strong></p>
                        <p>For enquiry, please contact<br /></p>
                    </div>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="container">
                <div class="footer-container">
                    <div class="col-xs-12 col-sm-8 footer-links">
                        <a
                            href="https://historicengland.org.uk/access/"
                            target="_blank"
                            rel="noopener"
                            >Accessibility</a
                        >
                        <a
                            href="#"
                            @click.prevent="openCookieControl"
                            >Manage Cookies</a
                        >
                    </div>
                    <div class="col-xs-12 col-sm-4 footer-copyright">
                        <span
                            >&copy; {{ copyright.year }}
                            {{ copyright.text }}</span
                        >
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
defineProps({
    copyright: {
        type: Object,
        default: () => ({ text: "", year: new Date().getFullYear() }),
    },
});
function openCookieControl() {
    // Implement cookie control logic or integration
}
</script>

<style scoped>
.footer-top,
.footer-bottom {
    background: #222;
    color: #fff;
    padding: 1rem 0;
}
.footer-links a {
    color: #fff;
    margin-right: 1rem;
    text-decoration: underline;
}
.footer-links a:focus {
    outline: 2px solid #ffd700;
    outline-offset: 2px;
}
</style>
