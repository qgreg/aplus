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
var app = angular.module("aplusApp", ['chart.js', 'ngRoute', 'ui.bootstrap']);

app.config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('{a');
      $interpolateProvider.endSymbol('a}');
    }]);

app.config(["$routeProvider","$locationProvider", function ($routeProvider,$locationProvider) {
      $routeProvider
                .when('/browse', {
                    templateUrl: '../static/partials/select.html',
                    controller: 'BrowserCtrl'
                })
                .when('/compare', {
                    templateUrl: '../static/partials/donut.html',
                    controller: 'DoughnutCtrl'
                })
                .when('/', {
                    templateUrl: '../static/partials/home.html'
                })
                .otherwise({
                    redirectTo: '/'
                });
      $locationProvider.hashPrefix('');
        }]);

app.controller('MainCtrl', ['$route',
  function MainCtrl($route) {
    this.$route = $route;
}]);

app.controller('BrowserCtrl', ['$scope', '$http', 'dataFactory',
    function ($scope, $http, dataFactory) {

    $scope.pssa = {
    "year": "",
    "subject": "",
    "school": "",
    "grade": "",
    "subset": ""
    };

    $http.get('/api/pssa/select')
        .then(function (result) {
            $scope.select = result.data;
        });

    $scope.fullid = $scope.pssa.year + $scope.pssa.subject + $scope.pssa.school + $scope.pssa.grade + $scope.pssa.subset;
    $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
    $scope.options = {
        legend: {
            display: true,
            position: 'bottom'
    }};

    $scope.status;
    $scope.scores;
    $scope.labels;
    $scope.data;

    $scope.getScores = function () {
        dataFactory.getScores($scope.pssa.year, $scope.pssa.school, $scope.pssa.grade, $scope.pssa.subject, $scope.pssa.subset)
            .then(
                function (response) {
                    $scope.status = 'Retrieved score!';
                    $scope.scores = response.data;
                    $scope.labels = ['Advanced ' + $scope.scores.advanced + ' ' + ($scope.scores.advanced / $scope.scores.total_tested * 100).toFixed(1) + '%', 'Proficient ' + $scope.scores.proficient + ' ' + ($scope.scores.proficient / $scope.scores.total_tested * 100).toFixed(1) + '%', 'Basic ' + $scope.scores.basic + ' ' + ($scope.scores.basic / $scope.scores.total_tested * 100).toFixed(1) + '%', 'Below Basic ' + $scope.scores.below_basic + ' ' + ($scope.scores.below_basic / $scope.scores.total_tested * 100).toFixed(1) + '%'];
                    $scope.data = [$scope.scores.advanced, $scope.scores.proficient, $scope.scores.basic, $scope.scores.below_basic];
                    $scope.donutload = true;
                    // var myPie = new Chart(document.getElementById($scope.fullid).getContext("2d")).Doughnut($scope.data, $scope.labels, $scope.options);
                    var canvas = document.getElementById($scope.fullid);
                    var ctx = canvas.getContext("2d");
                    ctx.font = "10px Arial";
                    var topScore = (($scope.scores.advanced + $scope.scores.proficient) * 100).toFixed(1);
                    ctx.fillText("Hello",0,0);
                    ctx.fillText(topScore + "%",10,50);
                }, 
                function (error) {
                    $scope.status = 'Error retrieving score! ' + error.message;
                })
    };
}]);


app.controller('DoughnutCtrl', ['$scope', 'dataFactory',
    function ($scope, dataFactory) {

    $scope.year = '2016';
    $scope.subject = 'ELA';
    $scope.school = 'PPS Phillips';
    $scope.grade = '3';
    $scope.subset = 'All';
    $scope.donutload = false;
    $scope.fullid = $scope.year + $scope.subject + $scope.school + $scope.grade + $scope.subset
    $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
    $scope.options = {
        legend: {
            display: true,
            position: 'bottom'
    }};

    $scope.status;
    $scope.scores;
    $scope.labels;
    $scope.data;

    $scope.getScores = function () {
        dataFactory.getScores($scope.year, $scope.school, $scope.grade, $scope.subject, $scope.subset)
            .then(
                function (response) {
                    $scope.status = 'Retrieved score!';
                    $scope.scores = response.data;
                    $scope.labels = ['Advanced ' + ($scope.scores.advanced * 100).toFixed(1) + '%', 'Proficient '  + ($scope.scores.proficient * 100).toFixed(1) + '%', 'Basic ' + ($scope.scores.basic * 100).toFixed(1) + '%', 'Below Basic ' + ($scope.scores.below_basic * 100).toFixed(1) + '%'];
                    $scope.data = [$scope.scores.advanced, $scope.scores.proficient, $scope.scores.basic, $scope.scores.below_basic];
                    $scope.donutload = true;
                    // var myPie = new Chart(document.getElementById($scope.fullid).getContext("2d")).Doughnut($scope.data, $scope.labels, $scope.options);
                    var canvas = document.getElementById($scope.fullid);
                    var ctx = canvas.getContext("2d");
                    ctx.font = "10px Arial";
                    var topScore = (($scope.scores.advanced + $scope.scores.proficient) * 100).toFixed(1);
                    ctx.fillText("Hello",0,0);
                    ctx.fillText(topScore + "%",10,50);
                }, 
                function (error) {
                    $scope.status = 'Error retrieving score! ' + error.message;
                })
    };
}]);

app.controller('DonutChildCtrl', ['$scope', 'dataFactory',
    function ($scope, dataFactory) {

    var vm = this;
    BrowserCtrl.apply(vm, arguments);
    $scope.donutload = false;
    $scope.fullid = pssa.year + pssa.subject + pssa.school + pssa.grade + pssa.subset
    $scope.colors = ['#60B064', '#9DDBB5', '#D2A6D2', '#BA66B0'];
    $scope.options = {
        legend: {
            display: true,
            position: 'bottom'
    }};

    $scope.status;
    $scope.scores;
    $scope.labels;
    $scope.data;

    $scope.getScores = function () {
        dataFactory.getScores(pssa.year, pssa.school, pssa.grade, pssa.subject, pssa.subset)
            .then(
                function (response) {
                    $scope.status = 'Retrieved score!';
                    $scope.scores = response.data;
                    $scope.labels = ['Advanced ' + ($scope.scores.advanced * 100).toFixed(1) + '%', 'Proficient '  + ($scope.scores.proficient * 100).toFixed(1) + '%', 'Basic ' + ($scope.scores.basic * 100).toFixed(1) + '%', 'Below Basic ' + ($scope.scores.below_basic * 100).toFixed(1) + '%'];
                    $scope.data = [$scope.scores.advanced, $scope.scores.proficient, $scope.scores.basic, $scope.scores.below_basic];
                    $scope.donutload = true;
                    // var myPie = new Chart(document.getElementById($scope.fullid).getContext("2d")).Doughnut($scope.data, $scope.labels, $scope.options);
                    var canvas = document.getElementById($scope.fullid);
                    var ctx = canvas.getContext("2d");
                    ctx.font = "10px Arial";
                    var topScore = (($scope.scores.advanced + $scope.scores.proficient) * 100).toFixed(1);
                    ctx.fillText("Hello",0,0);
                    ctx.fillText(topScore + "%",10,50);
                }, 
                function (error) {
                    $scope.status = 'Error retrieving score! ' + error.message;
                })
    };
}]);

