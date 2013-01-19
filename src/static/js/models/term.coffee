define [
    'jquery'
    'underscore'
    'backbone'
], ($, _, Backbone, Subject) ->
    class Term extends Backbone.RelationalModel

        initialize: () ->

        compare: (that) ->
            order = ["none", "spring", "summer", "autumn", "winter", "all_year"]
            (order.indexOf that.name) - (order.indexOf this.name)

    Term.setup()
    Term
