define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
    'common/bootstrap'
    'cs!globalModels/registration'
], ($, _, Backbone, flog, bootstrapData, Registration) ->
    class RegistrationList extends Backbone.Collection

        model: Registration

        initialize: () ->
            @on 'change:order', @reorder, @

        reorder: (model, newPos, options) ->
            oldPos = model.previous 'order'

            flog.info "Moving #{model.get('subject').get('ja_name')} from #{oldPos} to #{newPos}"

            if oldPos < newPos
                [x, toChange] = [-1, @filter (r) ->
                    oldPos < r.get('order') <= newPos && r != model]
            else
                [x, toChange] = [1, @filter (r) ->
                    newPos <= r.get('order') < oldPos && r != model]

            # When oldPos < newPos, decrement orders between else increment
            _.chain(toChange).each (r) -> r.set('order', r.get('order') + x, { silent: true })
            @sort()


        comparator: (model) ->
            model.get("order")


    new RegistrationList(bootstrapData.registrations)
