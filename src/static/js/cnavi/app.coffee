define [
    'cs!app_router'
    'flog'
    'i18next'
    'text'
    'cs!views/header_view'
], (Router, flog, i18next, text, headerView) ->
    i18nOptions =
        ns:
            namespaces: [
                'cnavi'
            ]
            defaultNs: 'cnavi'
        debug: true
        resStore:
            ja: {}
        fallbackLng: 'ja'

    initialize: (lng='ja') ->
        flog.setLevel 'debug'
        flog.info 'Initializing app'

        moduleName = "text!locales/#{lng}/cnavi.json"

        require [moduleName], (t) ->
            translations = JSON.parse t

            i18nOptions.lng = lng
            i18nOptions.resStore[lng].cnavi = translations
            i18next.init i18nOptions

            headerView.render()
            Router.initialize()
