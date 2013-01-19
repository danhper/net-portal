define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/classroom'
], ($, _, Backbone, Classroom) ->
    class Building extends Backbone.RelationalModel

        relations: [
            type: 'HasMany'
            key: 'classrooms'
            relatedModel: Classroom
            reverseRelation:
                key: 'building'
                type: 'HasOne'
        ]

        initialize: () ->

    Building.setup()
    Building
