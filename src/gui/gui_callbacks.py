def setup_additional_callbacks(route_panel, reports_panel, life_panel, route_controller, life_controller, _start_journey, _generate_report):
    route_panel.on_travel = _start_journey
    reports_panel.on_generate_report = _generate_report
    life_panel.on_analyze_travel = lambda: life_controller.analyze_next_travel(route_controller.get_current_path())
