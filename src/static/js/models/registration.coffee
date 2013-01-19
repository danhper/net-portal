define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/subject'
], ($, _, Backbone, Subject) ->
    class SubjectRegistration extends Backbone.RelationalModel

        relations: [
            type: 'HasOne'
            key: 'subject'
            relatedModel: Subject
            reverseRelation:
                key: 'registrations'
                type: 'HasMany'
        ]

        initialize: () ->

    SubjectRegistration.setup()
    SubjectRegistration
