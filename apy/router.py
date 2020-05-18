import re
from typing import List
from collections import OrderedDict


class RouterException(Exception):
    pass


class Route:

    def __init__(self, uri, methods, name=None, resource=None):
        self.uri = self._initialize_uri(uri)
        self.methods = self._initialize_methods(methods)
        self.name = self._initialize_name(name)
        self.resource = self._initialize_resource(resource)

    def _initialize_resource(self, resource):
        if resource is None:
            return resource

        if isinstance(resource, str):
            if resource.find('@') == -1 or resource.find('.') == -1:
                raise RouterException(
                    'when resource is a string is should be in the format'
                    + ' package.module.ClassName@method'
                )
        elif not callable(resource):
            raise RouterException(
                'resource has to be either a callable or a string in the format'
                + ' package.module.ClassName@method'
            )

        return resource

    def _initialize_name(self, name):
        if name is not None and not isinstance(name, str):
            raise RouterException('name should be a string')

        return name

    def _initialize_uri(self, uri):
        if uri[0] != '/':
            raise RouterException('uri should start with a /')

        if uri[-1] == '/':
            raise RouterException('uri should not end with a /')

        return uri

    def _initialize_methods(self, methods):
        if isinstance(methods, str):
            methods = self._convert_str_methods_to_list(methods)
        elif not isinstance(methods, List):
            raise RouterException('methods needs to be either a string or a list')

        # converting all methods to uppercase
        methods = [method.upper() for method in methods]
        valid_methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']
        for method in methods:
            if method not in valid_methods:
                raise RouterException(
                    f'{method} is an invalid HTTP method. Valid methods are '
                    + ', '.join(valid_methods)
                )

        return methods

    def _convert_str_methods_to_list(self, methods):
        if methods.find(',') == -1:
            methods = [methods]
        else:
            methods = methods.split(',')

        return methods

    def __repr__(self): # pragma: no cover
        return f'uri: {self.uri} methods: {self.methods} name: {self.name}'


class RouteCollection:

    def __init__(self, routes=[]):
        self.routes_by_uri = {}
        self.routes_by_name = {}

        for route in routes:
            self.add(route)

    def add(self, route):
        if not isinstance(route, Route):
            raise RouterException("RouteCollection only accepts Route")

        if route.uri not in self.routes_by_uri:
            self.routes_by_uri[route.uri] = {}

        for method in route.methods:
            self.routes_by_uri[route.uri][method] = route

        if route.name:
            self.routes_by_name[route.name] = route

    def get_by_name(self, name):
        return self.routes_by_name.get(name)

    def get_by_uri_and_method(self, uri, method):
        if uri in self.routes_by_uri and method in self.routes_by_uri[uri]:
            return self.routes_by_uri[uri][method]

        return None


class Matcher:
    def __init(self, route_collection):
        self.route_collection = route_collection

    def match(self, uri, method):
        pass


