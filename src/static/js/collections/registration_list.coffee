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


    new RegistrationList(bootstrapData.registrations)
