define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'common/bootstrap'
    'cs!globalModels/period'
], ($, _, Backbone, flog, bootstrapData, Period) ->
    class PeriodList extends Backbone.Collection

        model: Period

        comparator: (model) ->
            model.get("id")

    flog.info "Loading data for periods"
    flog.info bootstrapData.periods
    new PeriodList(bootstrapData.periods)
