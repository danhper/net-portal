define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/classroom'
    'cs!globalModels/period'
], ($, _, Backbone, Classroom, Period) ->
    class Class extends Backbone.RelationalModel
        relations: [
            type: 'HasOne'
            key: 'classroom'
            relatedModel: Classroom
            reverseRelation:
                key: 'classes'
                type: 'HasMany'
        ,
            type: 'HasOne'
            key: 'start_period'
            relatedModel: Period
            reverseRelation:
                key: 'classes'
                type: 'HansMany'
        ,
            type: 'HasOne'
            key: 'end_period'
            relatedModel: Period
            reverseRelation:
                key: 'classes'
                type: 'HansMany'
        ]

        initialize: () ->

    Class.setup()
    Class
