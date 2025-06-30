odoo.define('parc_automobile.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var QWeb = core.qweb;
    var _t = core._t;

    var ParcDashboard = AbstractAction.extend({
        template: 'ParcAutomobileDashboard',
        jsLibs: [
            '/web/static/lib/Chart/Chart.js'
        ],
        events: {
            'click .o_dashboard_action': '_onDashboardActionClick',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboard_data = {};
        },

        willStart: function() {
            var self = this;
            return $.when(
                this._loadData(),
                ajax.loadLibs(this),
                this._super()
            );
        },

        _loadData: function() {
            var self = this;
            return this._rpc({
                model: 'parc.automobile.dashboard',
                method: 'get_dashboard_data',
            }).then(function(result) {
                self.dashboard_data = result;
            });
        },

        start: function() {
            var self = this;
            this._renderDashboard();
            return this._super();
        },

        _renderDashboard: function() {
            var self = this;
            this.$('.dashboard-content').html(QWeb.render('ParcDashboardContent', {
                data: this.dashboard_data
            }));
            
            // Initialiser les graphiques
            this._initCharts();
        },

        _initCharts: function() {
            // Graphique de consommation de carburant
            if (this.dashboard_data.fuel_consumption) {
                var ctx = this.$('#fuelConsumptionChart')[0].getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: this.dashboard_data.fuel_consumption.labels,
                        datasets: [{
                            label: 'Consommation (L/100km)',
                            data: this.dashboard_data.fuel_consumption.values,
                            backgroundColor: 'rgba(52, 152, 219, 0.2)',
                            borderColor: 'rgba(52, 152, 219, 1)',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }

            // Graphique d'état des véhicules
            if (this.dashboard_data.vehicle_states) {
                var ctx2 = this.$('#vehicleStateChart')[0].getContext('2d');
                new Chart(ctx2, {
                    type: 'pie',
                    data: {
                        labels: this.dashboard_data.vehicle_states.labels,
                        datasets: [{
                            data: this.dashboard_data.vehicle_states.values,
                            backgroundColor: [
                                'rgba(46, 204, 113, 0.7)',
                                'rgba(52, 152, 219, 0.7)',
                                'rgba(155, 89, 182, 0.7)',
                                'rgba(231, 76, 60, 0.7)'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            }
        },

        _onDashboardActionClick: function(ev) {
            ev.preventDefault();
            var actionId = $(ev.currentTarget).data('action');
            this.do_action(actionId);
        },
    });

    core.action_registry.add('parc_automobile_dashboard', ParcDashboard);

    return ParcDashboard;
});