var homeModule = angular.module('gvldash.home', ['ngResource', 'ui.bootstrap', 'ui.bootstrap.tpls' , 'ui.bootstrap', 'dialog']);

homeModule.config(function($interpolateProvider, $httpProvider, $resourceProvider, PageConstants) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
    $resourceProvider.defaults.stripTrailingSlashes = false;
    $httpProvider.defaults.headers.common['X-CSRFToken'] = PageConstants.csrfToken;
});

homeModule.service('gvlHomePageDataService', function($http, $timeout) {
    // Server Status Cache
    var _system_data = [];
    var _messages;

    // Local vars
    var _data_timeout_id;

    var get_data = function() {
        // Poll gvl status
        $http.get('/api/v1/system/status', {
            params : {}
        }).success(function(data) {
        	_system_data = data;
        }).error(function(data) {
        });
    };

    // Execute first time fetch
    get_data();

    // Public interface
    return {
    	getGVLVersion : function() {
            return _system_data['version'];
        },
    	getGVLFlavour : function() {
            return _system_data['flavour'];
        },
        getGVLBuildDate : function() {
            return _system_data['build_date'];
        }
    };
});

homeModule.service('gvlAppDataService', function($http, $timeout) {
    // Server Status Cache
    var _service_list = [];

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

homeModule.controller("gvlHomePageActionsController", [ "$scope", "gvlHomePageDataService", "gvlAppDataService",
        function($scope, gvlHomePageDataService, gvlAppDataService) {

			$scope.getGVLVersion = function() {
		        return gvlHomePageDataService.getGVLVersion();
		    }

			$scope.getGVLFlavour = function() {
		        return gvlHomePageDataService.getGVLFlavour();
		    }

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

    // Local vars
    var _data_timeout_id;
    var _refresh_in_progress = false;

	var Package = $resource('/api/v1/packages/:packageName', null, {
        'update': { method:'PUT' },
    });

	var System = $resource('/api/v1/system/status/', null, {
        'save': { method:'POST' },
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

    // Execute first time fetch
    poll_data();

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

    var rebootCluster = function() {
    	system = new System({ state : "reboot" });
    	system.update();
    };

    var terminateCluster = function() {
    	system = new System({ state : "shutdown" });
    	system.$save();
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
        terminateCluster : terminateCluster,
        rebootCluster : rebootCluster,
        isRefreshInProgress : function() {
            return _refresh_in_progress;
        }
    };
});


homeModule.controller("gvlAdminPageActionsController", [ "$scope", "$dialog", "gvlAdminDataService",
        function($scope, $dialog, gvlAdminDataService) {

            $scope.getPackageList = function() {
                return gvlAdminDataService.getPackageList();
            }

            $scope.install_package = function(pkg) {
                gvlAdminDataService.installPackage(pkg);
            }

            $scope.terminate_cluster = function() {
            	var title = "Confirm terminate...";
				var msg = "Are you sure you want to terminate this cluster?";
				var btns = [{result:'CANCEL', label: 'Cancel'},
				            {result:'OK', label: 'Ok', cssClass: 'btn-danger'}];

				$dialog.messageBox(title, msg, btns, function(result) {
					if (result === 'OK') {
						gvlAdminDataService.terminateCluster();
					}
				});
            }

            $scope.reboot_cluster = function() {
            	var title = "Confirm reboot...";
				var msg = "Are you sure you want to reboot the cluster?";
				var btns = [{result:'CANCEL', label: 'Cancel'},
				            {result:'OK', label: 'Ok', cssClass: 'btn-warning'}];

				$dialog.messageBox(title, msg, btns, function(result) {
					if (result === 'OK') {
		            	gvlAdminDataService.rebootCluster();
					}
				});

            }


        } ]);


homeModule.controller("gvlAboutPageActionsController", [ "$scope", "gvlHomePageDataService",
        function($scope, gvlHomePageDataService) {

			$scope.getGVLVersion = function() {
		        return gvlHomePageDataService.getGVLVersion();
		    }

			$scope.getGVLFlavour = function() {
		        return gvlHomePageDataService.getGVLFlavour();
		    }

			$scope.getGVLBuildDate = function() {
		        return gvlHomePageDataService.getGVLBuildDate();
		    }

        } ]);


var dialogModule = angular.module("dialog", [ 'ngSanitize', 'ui.bootstrap' ]);


dialogModule.factory('$dialog', ['$rootScope', '$modal', function($rootScope, $modal) {

  function dialog(modalOptions, resultFn) {
    var dialog = $modal.open(modalOptions);
    if (resultFn) dialog.result.then(resultFn);
    dialog.values = modalOptions;
    return dialog;
  }

  function modalOptions(templateUrl, controller, scope) {
    return { templateUrl:  templateUrl, controller: controller, scope: scope }; }

  return {
    /**
     * Creates and opens dialog.
     */
    dialog: dialog,

    /**
     * Returns 0-parameter function that opens dialog on evaluation.
     */
    simpleDialog: function(templateUrl, controller, resultFn) {
      return function () { return dialog(modalOptions(templateUrl, controller), resultFn); }; },

    /**
     * Opens simple generic dialog presenting title, message (any html) and provided buttons.
     */
    messageBox: function(title, message, buttons, resultFn) {
      var scope = angular.extend($rootScope.$new(false), { title: title, message: message, buttons: buttons });
      return dialog(modalOptions("template/messageBox/message.html", 'MessageBoxController', scope), function (result) {
        var value = resultFn ? resultFn(result) : undefined;
        scope.$destroy();
        return value;
      }); }
  };
}]);


dialogModule.run(["$templateCache", function($templateCache) {
  $templateCache.put("template/messageBox/message.html",
      '<div class="modal-header"><h3>{$ title $}</h3></div>\n' +
      '<div class="modal-body"><p ng-bind-html="message"></p></div>\n' +
      '<div class="modal-footer"><button ng-repeat="btn in buttons" ng-click="close(btn.result)" class="btn" ng-class="btn.cssClass">{$ btn.label $}</button></div>\n');
}]);


dialogModule.controller('MessageBoxController', ['$scope', '$modalInstance', function ($scope, $modalInstance) {
  $scope.close = function (result) { $modalInstance.close(result); }
}]);