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

app.controller('DoughnutCtrl', ['$scope', function ($scope) {
    $scope.labels = ['Advanced 6.7%', 'Proficient 35.6%', 'Basic 46.7%', 'Below Basic 11.1%'];
    $scope.data = [.067, .356, .467, .111];
    $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
    $scope.options = {
        legend: {
            display: true,
            position: 'bottom',
        }
    }
}]);


