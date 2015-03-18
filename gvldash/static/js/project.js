var homeModule = angular.module('gvldash.home', ['ngResource']);

homeModule.config(function($interpolateProvider, $httpProvider, $resourceProvider, PageConstants) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
    $resourceProvider.defaults.stripTrailingSlashes = false;
    $httpProvider.defaults.headers.common['X-CSRFToken'] = PageConstants.csrfToken;
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
        $http.get('/api/v1/services/', {
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
			gvlAppDataService.resumeDataService();

            $scope.isRefreshInProgress = function() {
                return gvlAppDataService.isRefreshInProgress();
            }

            $scope.getServiceList = function() {
                return gvlAppDataService.getServiceList();
            }

            $scope.getServiceURL = function(service_name) {
                if (service_name == "ssh")
                    return window.location.hostname;
                else
                	return window.location.origin + gvlAppDataService.getServicePath(service_name);
            }

        } ]);


homeModule.service('gvlAdminDataService', function($http, $timeout, $resource) {
    // Server Status Cache
    var _package_list = [];
    var _messages;

    // Local vars
    var _data_timeout_id;
    var _refresh_in_progress = false;

	var Package = $resource('/api/v1/packages/:packageName', null, {
        'update': { method:'PUT' },
    });

    var poll_data = function() {
        // Poll gvl status
        _refresh_in_progress = true;

        Package.query().$promise.then(function (result) {
        	_package_list = result;
            _refresh_in_progress = false;
        });

        resumeDataService();
    };

    var resumeDataService = function() {
        $timeout.cancel(_data_timeout_id); // cancel any
        // existing timers
        _data_timeout_id = $timeout(poll_data, 5000, true);
    };

    var getPackage = function(pkg) {
        for (var index in _package_list) {
            if (_package_list[index].package_name == package_name) {
                return _package_list[index];
            }
        }
        return null;
    };

    var installPackage = function(pkg) {
    	pkg.status = "installing";
    	Package.update({ packageName : pkg.package_name }, pkg);
    };

    // Public interface
    return {
        pauseDataService : function() {
            $timeout.cancel(_data_timeout_id);
        },
        resumeDataService : resumeDataService,
        getPackageList : function() {
            return _package_list;
        },
        installPackage : installPackage,
        isRefreshInProgress : function() {
            return _refresh_in_progress;
        }
    };
});


homeModule.controller("gvlAdminPageActionsController", [ "$scope", "gvlAdminDataService",
        function($scope, gvlAdminDataService) {
			gvlAdminDataService.resumeDataService();

            $scope.getPackageList = function() {
                return gvlAdminDataService.getPackageList();
            }

            $scope.install_package = function(pkg) {
                gvlAdminDataService.installPackage(pkg);
            }

            $scope.getPackageActions = function(service_name) {
                	return window.location.origin + gvlAdminDataService.getServicePath(service_name);
            }

        } ]);
