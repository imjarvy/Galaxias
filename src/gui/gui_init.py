import tkinter as tk
from .services import RouteService, VisualizationService, ConfigurationService, BurroJourneyService
from .components import (
    RoutePlanningPanel, BurroStatusPanel,
    ReportsPanel, VisualizationPanel
)
from .controllers import (
    RouteController, BurroController, VisualizationController
)
from ..core import SpaceMap, BurroAstronauta
from ..algorithms import HyperGiantJumpSystem

def initialize_services():
    config_service = ConfigurationService()
    config = config_service.load_configuration('data/spaceship_config.json')
    space_map = SpaceMap('data/constellations.json')
    route_service = RouteService(space_map, config)
    visualization_service = VisualizationService(space_map)
    journey_service = BurroJourneyService(space_map)
    return config_service, config, space_map, route_service, visualization_service, journey_service

def initialize_models(space_map):
    burro = space_map.create_burro_astronauta()
    hypergiant_system = HyperGiantJumpSystem(space_map)
    return burro, hypergiant_system

def initialize_components(space_map, burro):
    route_panel = RoutePlanningPanel(space_map)
    burro_panel = BurroStatusPanel(burro)
    reports_panel = ReportsPanel()
    visualization_panel = VisualizationPanel()
    return route_panel, burro_panel, reports_panel, visualization_panel

def initialize_controllers(route_service, space_map, route_panel, visualization_panel, visualization_service, burro, burro_panel):
    route_controller = RouteController(route_service, space_map, route_panel, visualization_panel, visualization_service)
    burro_controller = BurroController(burro, burro_panel)
    visualization_controller = VisualizationController(visualization_service, visualization_panel, burro)
    return route_controller, burro_controller, visualization_controller
