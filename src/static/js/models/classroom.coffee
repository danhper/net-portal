define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/building'
], ($, _, Backbone, Building) ->
    class ClassRoom extends Backbone.RelationalModel

        relations: [
            type: 'HasOne'
            key: building
            relatedModel: 'Building'
            reverseRelation:
                key: 'classrooms'
                type: 'HasMany'
        ]

        initialize: () ->

    Classroom.setup()
    Classroom
