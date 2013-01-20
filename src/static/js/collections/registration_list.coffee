define [
    'jquery'
    'underscore'
    'backbone'
    'common/bootstrap'
    'cs!globalModels/registration'
], ($, _, Backbone, bootstrapData, Registration) ->
    class RegistrationList extends Backbone.Collection

        model: Registration

        initialize: () ->

        comparator: (model) ->
            model.get("order")


    new RegistrationList(bootstrapData.registrations)
