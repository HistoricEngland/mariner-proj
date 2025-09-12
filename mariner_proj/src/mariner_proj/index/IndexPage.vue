<template>
    <div>
        <a
            href="#main-content"
            class="skip-link"
            >Skip to main content</a
        >
        <HeaderNav :app-title="appTitle" />
        <main
            id="main-content"
            tabindex="-1"
        >
            <HeroSection
                :title="heroTitle"
                :lead="heroLead"
                :image="heroImage"
            />
            <TableOfContents :sections="tocSections" />
            <section
                v-for="featurette in featurettes"
                :key="featurette.id"
            >
                <FeaturetteSection v-bind="featurette" />
            </section>
            <ContactSection :contact-info="contactInfo" />
        </main>
        <FooterSection :copyright="copyright" />
    </div>
</template>

<script setup>
import HeaderNav from "@/mariner_proj/index/components/HeaderNav.vue";
import HeroSection from "@/mariner_proj/index/components/HeroSection.vue";
import TableOfContents from "@/mariner_proj/index/components/TableOfContents.vue";
import FeaturetteSection from "@/mariner_proj/index/components/FeaturetteSection.vue";
import ContactSection from "@/mariner_proj/index/components/ContactSection.vue";
import FooterSection from "@/mariner_proj/index/components/FooterSection.vue";

// Example props/data, to be replaced with Django context or API
const appTitle = "National Marine Historic Environment Record (NMHR)";
const heroTitle = appTitle;
const heroLead =
    "The online heritage information and management system for the marine historic environment.";
const heroImage = "/static/img/landing/featurette1.png";
const tocSections = [
    {
        id: "bm-what-service",
        label: "What is the Marine Historic Environment Service?",
    },
    {
        id: "bm-what-record",
        label: "What is the National Marine Heritage Record?",
    },
    { id: "bm-records-held", label: "What type of records do we hold?" },
    { id: "bm-records-provide", label: "What type of records do we provide?" },
    { id: "bm-how-to-use", label: "How to use the Marine HER Service" },
];
const featurettes = [
    {
        id: "bm-what-service",
        heading: "What is the Marine Historic Environment Service?",
        text: `The Marine HER Service is the first port of call for anyone seeking information about heritage that is located in England's seas and tidal waters, from the mean high water mark out to the edge of the offshore marine planning area [KM to source map]. We provide access to, and maintenance and enhancement of the National Marine Heritage Record.`,
    },
    {
        id: "bm-what-record",
        heading: "What is the National Marine Heritage Record?",
        text: `The National Marine Heritage Record (NMHR) documents England's coastal, intertidal and underwater heritage, from the prehistoric submerged landscapes of Doggerland in the North Sea, to WWII sea defences, to newly discovered wrecks. It is constantly updated with the latest available research, by Historic England marine and coastal specialists.`,
    },
    {
        id: "bm-records-held",
        heading: "What type of records do we hold?",
        text: `We hold records detailing archaeological investigations of coastal structures, and intertidal and underwater sites including over 6,000 shipwrecks and aircraft wrecks, obstructions, submerged prehistoric landscapes, marine buildings and structures (such as seaforts, fish traps, docks, harbours, jetties, sea defences), and find spots. These records are based on archaeological reports, radio carbon dates, reports from Marine aggregate extractions, UKHO data, historic seascape characterisation, local and project data sets (Citizan and the Ships Project), recreational diver information, and Receiver of Wreck droit finds. We also hold records that document 31,000 recorded vessel losses, where no physical site has been found, based on historical documentary evidence such as historic news articles and Lloyds listings.`,
    },
    {
        id: "bm-records-provide",
        heading: "What type of records do we provide?",
        text: `Dependant on the type of the query, we can provide genealogical information, archaeological information, spatial data in a range of formats, etc [KM to expand on this]. [Say something about HE open data commitments].`,
        images: [
            {
                src: "/static/img/landing/about-left.png",
                alt: "About left",
                ariaLabelledby: "img-left",
            },
            {
                src: "/static/img/landing/about-right.png",
                alt: "About right",
                ariaLabelledby: "img-right",
            },
        ],
        extra: "[May link externally to Citizan and other partner organisations who are providing data - to be discussed]",
    },
    {
        id: "bm-how-to-use",
        heading: "How to use the Marine HER Service",
        text: `Anyone can use this service. Details to be provided (e.g. public and academic users vs commercial guidelines - likely to follow GLHER, but tbc).`,
    },
];
const contactInfo = {
    // Contact details here
};
const copyright = {
    text: "Historic England",
    year: new Date().getFullYear(),
};
</script>

<style scoped>
.skip-link {
    position: absolute;
    left: -999px;
    top: auto;
    width: 1px;
    height: 1px;
    overflow: hidden;
    z-index: 1000;
    background: #ffd700;
    color: #222;
    padding: 0.5rem 1rem;
    border-radius: 4px;
}
.skip-link:focus {
    left: 1rem;
    top: 1rem;
    width: auto;
    height: auto;
    outline: 2px solid #222;
}
</style>
