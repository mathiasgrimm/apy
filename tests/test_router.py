import pytest
from apy import router
from typing import List


class RouteTests:

    def test_it_initializes_correctly(self):
        uri = '/api/v1/tests/<int:test>'
        methods = ['GET', 'POST']
        name = 'test.get'

        route = router.Route(uri=uri, methods=methods, name=name)
        assert route.uri == '/api/v1/tests/<int:test>'
        assert methods == route.methods
        assert name == route.name

    def test_it_validates_uri_without_leading_slash(self):
        with pytest.raises(router.RouterException):
            router.Route(uri='tests', methods='GET')

    def test_it_validates_uri_with_trailing_slash(self):
        with pytest.raises(router.RouterException):
            router.Route(uri='/tests/', methods='GET')

    def test_it_validates_methods(self):
        with pytest.raises(router.RouterException):
            router.Route(uri='/tests', methods=(123,123))

    def test_it_validates_name(self):
        with pytest.raises(router.RouterException):
            router.Route(uri='/tests', methods='GET', name=[])

    def test_methods_can_be_simple_str(self):
        route = router.Route(uri='/tests', methods='GET')
        assert isinstance(route.methods, List)
        assert route.methods[0] == 'GET'

    def test_methods_str_is_always_upper(self):
        route = router.Route(uri='/tests', methods='get')
        assert route.methods[0] == 'GET'
        route = router.Route(uri='/tests', methods=['get'])
        assert route.methods[0] == 'GET'

    def test_str_methods_splits_str(self):
        route = router.Route(uri='/tests', methods='GET,POST')
        assert route.methods[0] == 'GET'
        assert route.methods[1] == 'POST'

    def test_it_accepts_only_valid_http_methods(self):
        router.Route(uri='/tests', methods='GET,POST,PUT,PATCH,DELETE,OPTIONS,HEAD')
        with pytest.raises(router.RouterException):
            router.Route(uri='/tests', methods='SOME')

    def test_it_initialize_with_valid_resource_when_str(self):
        resource = 'myapp.controller.LoginController@login'
        route = router.Route(uri='/tests', methods='GET', resource=resource)
        assert route.resource == resource

    def test_it_initialize_with_valid_resource_when_callable(self):
        resource = lambda: 'hello world'
        route = router.Route(uri='/tests', methods='GET', resource=resource)
        assert route.resource == resource

        def some_callable():
            return 'Hello World'

        resource = some_callable
        route = router.Route(uri='/tests', methods='GET', resource=resource)
        assert id(route.resource) == id(resource)

        class SomeCallable:
            def __call__(self, *args, **kwargs):
                pass

        resource = SomeCallable()
        route = router.Route(uri='/tests', methods='GET', resource=resource)
        assert id(route.resource) == id(resource)

    def test_it_validates_resource(self):
        # invalid type
        with pytest.raises(router.RouterException):
            router.Route(uri='/tests', methods='GET', resource=123)

        # invalid format
        with pytest.raises(router.RouterException):
            router.Route(uri='/tests', methods='GET', resource='hey')


class RouteCollectionTests:
    def test_it_initializes_correctly_when_no_route_is_passed(self):
        router.RouteCollection()

    def test_it_adds_correctly_when_instatiating(self):
        route = router.Route(uri='/tests', methods='GET', name='some.route')
        route_collection = router.RouteCollection([route])

        assert len(route_collection.routes_by_uri) == 1
        assert len(route_collection.routes_by_name) == 1

        assert id(route_collection.routes_by_name['some.route']) == id(route)
        assert id(route_collection.routes_by_uri['/tests']['GET']) == id(route)

    def test_it_allows_only_routes_to_be_added(self):
        with pytest.raises(router.RouterException):
            router.RouteCollection([1, 2, 3])

    def test_it_can_add_route_without_name(self):
        route = router.Route(uri='/tests', methods='GET')
        route_collection = router.RouteCollection([route])

        assert len(route_collection.routes_by_uri) == 1
        assert len(route_collection.routes_by_name) == 0

    def test_it_overrides_when_adding(self):
        route_collection = router.RouteCollection()
        route1 = router.Route(uri='/tests', methods='GET', name='some.route')
        route_collection.add(route1)

        route2 = router.Route(uri='/tests', methods='GET', name='some.route')
        route_collection.add(route2)

        assert id(route_collection.routes_by_name['some.route']) == id(route2)
        assert id(route_collection.routes_by_uri['/tests']['GET']) == id(route2)

    def test_it_adds_routes_with_multiple_methods(self):
        route_collection = router.RouteCollection()
        route = router.Route(uri='/tests', methods='GET,POST', name='some.route')
        route_collection.add(route)

        assert len(route_collection.routes_by_uri) == 1
        assert len(route_collection.routes_by_name) == 1
        assert id(route_collection.routes_by_uri['/tests']['GET']) == id(route)
        assert id(route_collection.routes_by_uri['/tests']['POST']) == id(route)

    def test_it_gets_by_name(self):
        route_collection = router.RouteCollection()
        route1 = router.Route(uri='/tests-a', methods='GET,POST', name='some.route.a')
        route2 = router.Route(uri='/tests-b', methods='GET,POST', name='some.route.b')
        route_collection.add(route1)
        route_collection.add(route2)

        assert route_collection.get_by_name('some.route.c') is None
        assert id(route_collection.get_by_name('some.route.a')) == id(route1)
        assert id(route_collection.get_by_name('some.route.b')) == id(route2)

    def test_it_get_by_uri_and_method(self):
        route1 = router.Route(uri='/tests-a', methods='GET,POST', name='some.route.a')
        route2 = router.Route(uri='/tests-b', methods='GET,POST', name='some.route.b')
        route_collection = router.RouteCollection([route1, route2])

        assert route_collection.get_by_uri_and_method('/tests-a', 'PUT') is None
        assert route_collection.get_by_uri_and_method('/tests', 'GET') is None
        assert id(route1) == id(route_collection.get_by_uri_and_method('/tests-a', 'GET'))
        assert id(route1) == id(route_collection.get_by_uri_and_method('/tests-a', 'POST'))
        assert id(route2) == id(route_collection.get_by_uri_and_method('/tests-b', 'GET'))
        assert id(route2) == id(route_collection.get_by_uri_and_method('/tests-b', 'POST'))


class MatcherTests:

    def test_i_matches_uri(self):
        pass
