define [
    'jquery'
    'underscore'
    'backbone'
], ($, _, Backbone) ->
    class TermPeriod extends Backbone.RelationalModel

        initialize: () ->

        parse: (response) ->
            response.start_date = new Date(Date.parse(response.start_date))
            response.end_date = new Date(Date.parse(response.end_date))
            response

    TermPeriod.setup()
    TermPeriod
