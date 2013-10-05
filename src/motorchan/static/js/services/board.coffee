class BoardService
    constructor: ($resource) ->
        Board = $resource '/static/stub/boards.json/:slug', {},
            query:
                method: 'GET'
                isArray: false

        BoardService::get = (params) ->
            Board.query(params).$promise

angular.module('motorchan').service 'BoardService', ['$resource', BoardService]
