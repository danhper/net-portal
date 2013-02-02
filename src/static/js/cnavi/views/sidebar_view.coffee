define [
    'jquery'
    'underscore'
    'backbone'
    'flog'
], ($, _, Backbone, flog) ->
    class SidebarView extends Backbone.View
        el: "div#sidebar"

        events:
            'click a': 'changeActiveEvent'

        changeActive: (id) ->
            @$('ul li').removeClass 'active'
            @$('ul li').eq(id).addClass 'active'

        changeActiveEvent: (e) ->
            $target = @$(e.target)
            unless $target.is 'a'
                $target = $target.parents 'a'
            @changeActive @$('li').index($target.find('li'))


    new SidebarView()
