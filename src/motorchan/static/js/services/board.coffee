class BoardService
    constructor: ($resource) ->
        Board = $resource '/static/stub/boards.json', {},
            query:
                method: 'GET'
                isArray: false

        BoardService::get = ->
            Board.query().$promise

angular.module('motorchan').service 'BoardService', ['$resource', BoardService]
