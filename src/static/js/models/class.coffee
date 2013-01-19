define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/classroom'
    'cs!globalModels/period'
    'cs!globalModels/subject'
], ($, _, Backbone, Classroom, Period, Subject) ->
    class Class extends Backbone.RelationalModel

        relations: [
            type: 'HasOne'
            key: 'classroom'
            relatedModel: Classroom
        ,
            type: 'HasOne'
            key: 'start_period'
            relatedModel: Period
        ,
            type: 'HasOne'
            key: 'end_period'
            relatedModel: Period
        ]

        initialize: () ->


    Class.setup()
    Class
