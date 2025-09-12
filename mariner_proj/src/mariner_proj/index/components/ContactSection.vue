<template>
    <section
        class="featurette7"
        aria-labelledby="contact-title"
    >
        <h2 id="contact-title">Contact Us</h2>
        <div class="jumbotron">
            <h3>The Marine Historic Environment Record Service</h3>
            <div class="row website-details">
                <div class="col-xs-12">
                    <p>
                        Email:
                        <a href="mailto:marineinfo@historicengland.org.uk"
                            >marineinfo@historicengland.org.uk</a
                        >
                    </p>
                </div>
            </div>
            <div class="row address-phone">
                <div class="col-sm-6">
                    <address>
                        Historic England
                        <br />The Engine House <br />Fire Fly Avenue
                        <br />Swindon SN2 2EH
                    </address>
                </div>
                <div class="col-sm-6">
                    <p>Phone: <a href="tel:+443707870700">0370 787 0700</a></p>
                </div>
            </div>
        </div>
        <div>
            <p>
                All photographs used on this page are &copy; Historic England
                Archive
            </p>
        </div>
    </section>
</template>

<script setup>
defineProps({
    contactInfo: {
        type: Object,
        default: () => ({}),
    },
});
</script>

<style scoped>
.featurette7 {
    margin-top: 2rem;
}
.jumbotron {
    background: #f5f5f5;
    padding: 2rem;
    border-radius: 8px;
}
</style>
