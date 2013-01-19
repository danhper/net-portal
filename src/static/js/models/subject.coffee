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
            reverseRelation:
                key: 'subject'
                type: 'HasOne'
        ,
            type: 'HasOne'
            key: 'school'
            relatedModel: School
            reverseRelation:
                key: 'subjects'
                type: 'HasMany'
        ,
            type: 'HasMany'
            key: 'teachers'
            relatedModel: Teacher
            reverseRelation:
                key: 'subjects'
                type: 'HasMany'
        ]

        initialize: () ->

    Subject.setup()
    Subject
