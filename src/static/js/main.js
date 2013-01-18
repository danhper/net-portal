requirejs.config({

    baseUrl: "/static/js"

  , paths: {
        cs: 'lib/requirejs/cs'
      , handlebars: 'lib/handlebars/handlebars'
      , hbs: 'lib/hbs/hbs'
      , i18nprecompile: 'lib/hbs/i18nprecompile'
      , json2: 'lib/hbs/json2'
      , jquery: 'lib/jquery/jquery-1.9.0.min'
      , underscore: 'lib/underscore/underscore-min'
      , backbone: 'lib/backbone/backbone-min'
      , backboneRel: 'lib/backbone/backbone-relational'
      , domReady: 'lib/requirejs/domReady'
      , templates: '../templates'
      , 'coffee-script': 'lib/coffeescript/coffee-script'
    }

  , hbs: {
        disableI18n: true
      , helperPathCallback: function(name) {
            return 'cs!helpers/' + name;
      }
  }
});

require([
    'cs!app'
  , 'domReady'
], function(App, domReady) {
    domReady(function() {
        App.initialize();
    });
});
