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

        toJSON: () ->
            ar = super
            unless _.isObject(ar)
                return ar

            ar.classes[0].termNeedPrint = true
            if ar.classes.length > 1
                term = ar.classes[0].term.name
                allNeedPrint = false
                for v in ar.classes
                    if v.term.name != term
                        allNeedPrint = true
                for v in ar.classes[1..]
                    v.termNeedPrint = allNeedPrint
            ar


    Subject.setup()
    Subject
