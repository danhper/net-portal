define [
    'handlebars'
    'cs!helpers/trObj'
    'flog'
], (Handlebars, trObj, flog) ->
    formatClassroom = (classroom) ->
        content = ""
        content += "#{trObj(classroom.building, 'name')}-" if classroom.building?
        try
            content += trObj(classroom, 'name').toString()
        catch e
            flog.warning "No classroom name found for"
            flog.warning classroom

        if not content and classroom.info
            content = classroom.info

        new Handlebars.SafeString(content)

