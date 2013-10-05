class Routes
    constructor: ($routeProvider) ->
        $routeProvider
        .when '/',
            controller: 'BoardListController'
            templateUrl: '/static/templates/boards.html'
        .when '/:board/',
            controller: 'BoardController',
            templateUrl: '/static/templates/board.html'
        .otherwise
            redirectTo: '/'

angular.module('motorchan').config ['$routeProvider', Routes]
