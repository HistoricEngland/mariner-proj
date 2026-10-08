# Discovery: AEA Template Override Strategy (ph_112381)

Azure DevOps paste-friendly version of this discovery note (tables/nested lists in the main markdown file don't always render cleanly when pasted into ADO work item discussions). Formatting here is intentionally flat: no nested bullets, no markdown tables, code blocks kept standalone.

Status: Proven locally against mariner_proj (branch ph_112381_common_ui_discovery). This is a discovery note, not an implementation - all code used to prove this was reverted from mariner_proj afterwards. A disconnected reference example remains in a sibling repo (arches_he_common_ui), not wired into any project, for whoever picks up the real implementation.

## Terminology

AEA = Arches Extension Application (per Arches docs, developing/extension-applications): a pip-installable Django app, wired into a project via INSTALLED_APPS, reusable as a modular component across multiple Arches projects.

This is distinct from a plain Arches Extension (widget, datatype, function, plugin, card component). A plain Extension is a registered component tied to a specific extension point, and is not a Django app in INSTALLED_APPS.

## Chosen pattern: Arches Extension Application, not a plain Extension

Reasoning: Django's template resolution (APP_DIRS=True) only searches templates/ directories belonging to apps listed in INSTALLED_APPS. Plain Extensions have no presence in INSTALLED_APPS, so they cannot supply a generic, overridable page template (e.g. index.htm) via this mechanism.

A template-only shared UI package must be built as an Arches Extension Application: a Django app with is_arches_application = True, installed the same way as mariner_app or arches_he_data_transformation.

## Template loader ordering (confirmed)

Arches projects build TEMPLATES via build_templates_config() (arches/arches/settings_utils.py). Resolution order for a given template name (e.g. index.htm) is:

1. Host project's own templates/ directory - TEMPLATES[0]["DIRS"]. Checked by Django's filesystem loader before any app, and always wins regardless of INSTALLED_APPS order.
2. APP_DIRS fallback - each app's templates/ directory, searched in INSTALLED_APPS order, first match wins.
3. Core arches.app templates are the fallback of last resort.

Required INSTALLED_APPS position:

```
INSTALLED_APPS = (
    ...
    "mariner_proj",          # host project - always first
    "arches_he_common_ui",   # AEA(s) - after host, before arches.app
    "mariner_app",
    ...
)
INSTALLED_APPS += ("arches.app",)   # core Arches - always last
```

The AEA must sit after the host project and before arches.app for its templates to override core but still be overridable by the host. This ordering is not enforced automatically - if an AEA is listed after arches.app, core wins again (verified). It must be documented and checked in review (e.g. a comment in settings.py, as already exists for arches.app's position), not left to chance.

## Proof (local Mariner environment)

Using a throwaway test AEA with its own index.htm, verified via direct curl against the running dev server and via manage.py shell (django.template.utils.get_app_template_dirs('templates') and django.template.loader.get_template('index.htm').origin.name - useful for debugging ordering issues directly instead of inferring from rendered HTML).

Results:

- AEA vs core: with INSTALLED_APPS order mariner_proj then AEA then ... then arches.app, and the host's index.htm temporarily removed, the AEA's index.htm was served.
- Host vs AEA: same order, with the host's index.htm restored, the host's index.htm was served, even though the AEA was still installed.
- Order sensitivity: moving the AEA to after arches.app caused core's index.htm to be served again (AEA ignored).

Also proved the AEA working as a genuinely separate, standalone repo (not just a folder inside the host project), installed the same way arches_he_data_transformation is: COPY the repo into the image then pip install -e '.[dev]' at image build time (the AEA's pyproject.toml needs a dev extra defined, even if empty), with a docker-compose volume mount overlaying the same path at runtime for live editing. Confirmed via pip show showing the editable location pointing at the mounted repo, and the template origin resolving there.

## Settings-driven customization (confirmed)

A host project can override individual values (not just whole templates) via a context processor, following the same convention core Arches already uses for things like map_info/livereload.

Example pattern (AEA's context_processors.py):

```
def common_ui_settings(request):
    return {
        "common_ui_headline": getattr(settings, "COMMON_UI_HEADLINE", "<placeholder>"),
    }
```

The AEA ships sensible placeholder defaults; a host registers the processor in its own TEMPLATES config and sets plain settings values to override them - no template fork required.

The AEA's template can also wrap customizable regions in {% block %} tags (harmless even when unextended), so a host needing a deeper structural change can instead {% extends %} the AEA's template and override a specific block. Two levels of override: settings (values) and template inheritance (structure).

## Styling: must live in the AEA, not the project

Requirement: styling for the shared UI must ship with the AEA so a new host project gets a consistent look out of the box, not something each project re-implements.

Confirmed the same SCSS convention other Arches apps already use: an AEA provides media/css/_app-name.scss (hyphenated name), and the host's own project.scss does an @import of that name. Sass resolves this via includePaths built from each ARCHES_APPLICATIONS entry's media/css dir (see webpack.common.js), so the host just needs the one @import line - no other wiring.

Gotcha 1: the webpack dev-server container has its own volume mount list, separate from the main app container. A locally-mounted AEA needs its volume added to both (or neither picks up live edits or @import targets).

Gotcha 2: don't reuse the host project's existing custom CSS class names in the AEA's markup. Both end up in the same compiled bundle, so if the AEA's markup reuses the host's class names (for example a host-specific rule written for a different layout, such as position: absolute on a left-hand text container), the AEA page silently inherits and conflicts with rules it didn't expect. The AEA should use its own prefixed/unique class names - confirmed this resolves the conflict cleanly.

CDN links or inline style blocks are fine for a quick spike but wrong for production (no version pinning, external network dependency, CSP concerns, and risk of visually diverging from the host's actual compiled CSS). Production styling should go through the same SCSS/webpack pipeline as everything else.

## Plan for implementation (not yet done)

This was a discovery spike - the actual Common UI AEA still needs to be built. Decisions and groundwork to carry forward:

1. Pattern: build it as a real Arches Extension Application (own repo, pyproject.toml, is_arches_application = True), per the proof above.
2. INSTALLED_APPS ordering: document (and consider a startup check for) the required position - host first, AEA(s) next, arches.app last.
3. Template strategy: decide which pages/partials are fully AEA-owned templates vs settings-driven values vs block-overridable regions. Define and document the full list of overridable settings names (e.g. a COMMON_UI_ prefix convention) as the AEA grows - don't leave host teams to read context_processors.py to discover what's configurable.
4. Styling: ship a hyphenated SCSS partial per the confirmed convention; keep all custom class names uniquely prefixed to avoid collision with host CSS in the shared compiled bundle.
5. Local dev wiring: when adding a locally-mounted AEA to a host's act/docker-compose setup, remember both the Dockerfile COPY plus pip install -e '.[dev]' step, and the volume mounts on every service that needs it (main app and webpack).
6. Visual/pixel-level fidelity to any specific existing page (e.g. the current Mariner landing page) is implementation work, not discovery - out of scope here.
