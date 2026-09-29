define([
    'knockout',
    'views/components/search/base-filter',
    'templates/views/components/search/latlong-filter.htm',
], function(ko, BaseFilter, latlongFilterTemplate) {
    const componentName = 'latlong-filter';

    // null means the field has not been edited yet, so no error is shown
    const rangeError = function(value, label, min, max) {
        if (value === null || value === undefined) { return ''; }
        const entry = String(value).trim();
        if (entry === '') { return label + ' is required'; }
        const number = Number(entry);
        if (!isFinite(number)) { return label + ' must be a number'; }
        if (number < min || number > max) {
            return label + ' must be between ' + min + ' and ' + max;
        }
        return '';
    };

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

            this.longitudeError = ko.pureComputed(function() {
                return rangeError(this.filter.longitude(), 'Longitude (X)', -180, 180);
            }, this);

            this.latitudeError = ko.pureComputed(function() {
                return rangeError(this.filter.latitude(), 'Latitude (Y)', -90, 90);
            }, this);

            this.bufferError = ko.pureComputed(function() {
                const value = this.filter.buffer();
                if (value === null || value === undefined) { return ''; }
                const entry = String(value).trim();
                if (entry === '') { return ''; }
                const number = Number(entry);
                if (!isFinite(number)) { return 'Buffer radius must be a number'; }
                if (number < 0) { return 'Buffer radius must be 0 or greater'; }
                return '';
            }, this);

            this.hasErrors = ko.pureComputed(function() {
                return !!(this.longitudeError() || this.latitudeError() || this.bufferError());
            }, this);

            this.restoreState();
            this.searchFilterVms[componentName](this);
        },

        updateQuery: function() {
            const queryObj = this.query();
            const hasCoordinates = this.filter.longitude() !== null && this.filter.latitude() !== null;
            if (hasCoordinates && !this.hasErrors()) {
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
