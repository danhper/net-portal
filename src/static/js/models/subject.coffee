define [
    'jquery'
    'underscore'
    'backbone'
    'cs!globalModels/class'
    'cs!globalModels/school'
    'cs!globalModels/teacher'
], ($, _, Backbone, Class, School, Teacher) ->
    class Subject extends Backbone.RelationalModel

        relations: [
            type: 'HasMany'
            key: 'classes'
            relatedModel: Class
        ,
            type: 'HasOne'
            key: 'school'
            relatedModel: School
        ,
            type: 'HasMany'
            key: 'teachers'
            relatedModel: Teacher
        ]

        initialize: () ->

    Subject.setup()
    Subject
