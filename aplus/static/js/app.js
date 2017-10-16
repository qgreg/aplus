'use strict';

/**
 * @ngdoc object
 * @name aplusApp
 * @requires ui.bootstrap
 *
 * @description
 * Root app, which routes and specifies the partial html and controller depending on the url requested.
 *
 */
var app = angular.module("aplusApp", ['chart.js', 'ui.bootstrap']);

  app.controller('DoughnutCtrl', ['$scope', '$timeout', function ($scope, $timeout) {
    $scope.labels = ['Download Sales', 'In-Store Sales', 'Mail-Order Sales'];
    $scope.data = [350, 450, 100];

}]);


