var homeModule = angular.module('gvldash.home', []);

homeModule.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

homeModule.service('gvlAppDataService', function($http, $timeout) {
    // Server Status Cache
    var _service_list = [];
    var _messages;

    // Local vars
    var _data_timeout_id;
    var _refresh_in_progress = false;

    var poll_data = function() {
        // Poll gvl status
        _refresh_in_progress = true;
        $http.get('api/v1/services/', {
            params : {}
        }).success(function(data) {
            _service_list = data;
            _refresh_in_progress = false;
        }).error(function(data) {
            _refresh_in_progress = false;
        });
        resumeDataService();
    };

    var resumeDataService = function() {
        $timeout.cancel(_data_timeout_id); // cancel any
        // existing timers
        _data_timeout_id = $timeout(poll_data, 5000, true);
    };

    // Execute first time fetch
    poll_data();

    // Public interface
    return {
        pauseDataService : function() {
            $timeout.cancel(_data_timeout_id);
        },
        resumeDataService : resumeDataService,
        getServiceList : function() {
            return _service_list;
        },
        getServicePath : function(service_name) {
            for (var index in _service_list) {
                if (_service_list[index].service_name == service_name) {
                    return _service_list[index].service_path;
                }
            }
            return null;
        },
        isRefreshInProgress : function() {
            return _refresh_in_progress;
        }
    };
});

homeModule.controller("gvlHomePageActionsController", [ "$scope", "gvlAppDataService",
        function($scope, gvlAppDataService) {

            $scope.isRefreshInProgress = function() {
                return gvlAppDataService.isRefreshInProgress();
            }

            $scope.getServiceList = function(service_name) {
                return gvlAppDataService.getServiceList();
            }

            $scope.getServiceURL = function(service_name) {
                if (service_name == "ssh")
                    return window.location.hostname;
                return window.location.origin + gvlAppDataService.getServicePath(service_name);
            }

        } ]);
