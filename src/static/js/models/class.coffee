define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/classroom'
    'cs!globalModels/period'
    'cs!globalModels/subject'
    'cs!globalModels/term'
], ($, _, Backbone, Classroom, Period, Subject, Term) ->
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
        ,
            type: 'HasOne'
            key: 'term'
            relatedModel: Term
        ]

        initialize: () ->


    Class.setup()
    Class
