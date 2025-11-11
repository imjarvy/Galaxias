def setup_additional_callbacks(route_panel, reports_panel, route_controller, _start_journey, _generate_report):
    route_panel.on_travel = _start_journey
    reports_panel.on_generate_report = _generate_report
