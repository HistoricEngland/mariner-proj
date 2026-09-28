define([
    'knockout',
    'views/components/search/base-filter',
    'templates/views/components/search/latlong-filter.htm',
], function(ko, BaseFilter, latlongFilterTemplate) {
    const componentName = 'latlong-filter';
    const viewModel = BaseFilter.extend({
        initialize: function(options) {
            options.name = 'LatLong Filter';
            BaseFilter.prototype.initialize.call(this, options);

            this.filter = {
                longitude: ko.observable(null),
                latitude: ko.observable(null),
                buffer: ko.observable(0),
                inverted: ko.observable(false)
            };

            this.restoreState();
            this.searchFilterVms[componentName](this);
        },

        updateQuery: function() {
            const queryObj = this.query();
            if (this.filter.longitude() !== null && this.filter.latitude() !== null) {
                queryObj[componentName] = ko.toJSON(this.filter);
            } else {
                delete queryObj[componentName];
            }
            this.query(queryObj);
        },

        restoreState: function() {
            const query = this.query();
            if (componentName in query) {
                const value = JSON.parse(query[componentName]);
                this.filter.inverted(!!value.inverted);
                this.getFilterByType('term-filter-type').addTag(this.name, this.name, this.filter.inverted);
                this.filter.longitude(value.longitude);
                this.filter.latitude(value.latitude);
                this.filter.buffer(value.buffer);
            }
        },

        clear: function() {
            this.filter.longitude(null);
            this.filter.latitude(null);
            this.filter.buffer(0);
            this.filter.inverted(false);
            this.getFilterByType('term-filter-type').removeTag(this.name);
            this.updateQuery();
        }
    });

    return ko.components.register(componentName, {
        viewModel: viewModel,
        template: latlongFilterTemplate,
    });
});
