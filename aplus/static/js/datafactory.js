angular.module("aplusApp").service('dataFactory', ['$http', function ($http) {

        var urlBase = '/api';

        this.getScores = function (year, school, grade, subject, subset) {
            return $http.get(urlBase + '/' + year + '/' + school + '/' + grade + '/' +subject + '/' + subset);
        };

    }]);