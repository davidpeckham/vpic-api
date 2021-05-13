from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Make:
    make_id: int
    make_name: str
    # manufacturer_id: Optional[int]
    # manufacturer_name: Optional[str]
    # vehicle_type_id: Optional[int]
    # vehicle_type: Optional[str]


@dataclass(eq=True, frozen=True)
class Model:
    # make_id: int
    # make_name: str
    model_id: int
    model_name: str


@dataclass(eq=True, frozen=True)
class Manufacturer:
    manufacturer_id: int
    manufacturer_name: str
    manufacturer_common_name: str


@dataclass(eq=True, frozen=True)
class WorldManufacturerIndex:
    created_on: str
    date_available_to_public: str
    manufacturer_name: str
    updated_on: str
    vehicle_type: str
    wmi: str
    common_name: str = ''
    country: str = ''
    make_name: str = ''
    manufacturer_id: int = None
    parent_company_name: str = '' 
    url: str = ''


@dataclass(eq=True, frozen=True)
class VehicleType:
    vehicle_type_id: int
    vehicle_type_name: str


@dataclass(eq=True, frozen=True)
class Variable:
    id: int
    name: str
    data_type: str
    description: str


@dataclass(eq=True, frozen=True)
class Value:
    element_name: str
    id: int
    name: str


@dataclass(frozen=True)
class Vehicle:
    abs: str
    active_safety_sys_note: str
    adaptive_cruise_control: str
    adaptive_driving_beam: str
    adaptive_headlights: str
    additional_error_text: str
    air_bag_loc_curtain: str
    air_bag_loc_front: str
    air_bag_loc_knee: str
    air_bag_loc_seat_cushion: str
    air_bag_loc_side: str
    auto_reverse_system: str
    automatic_pedestrian_alerting_sound: str
    axle_configuration: str
    axles: str
    base_price: str
    batterya: str
    batterya_to: str
    battery_cells: str
    battery_info: str
    batteryk_wh: str
    batteryk_wh_to: str
    battery_modules: str
    battery_packs: str
    battery_type: str
    batteryv: str
    batteryv_to: str
    bed_lengthin: str
    bed_type: str
    blind_spot_mon: str
    body_cab_type: str
    body_class: str
    brake_system_desc: str
    brake_system_type: str
    bus_floor_config_type: str
    bus_length: str
    bus_type: str
    can_aacn: str
    cib: str
    cash_for_clunkers: str
    charger_level: str
    charger_powerkw: str
    cooling_type: str
    curb_weightlb: str
    custom_motorcycle_type: str
    daytime_running_light: str
    destination_market: str
    displacementcc: str
    displacementci: str
    displacementl: str
    doors: str
    drive_type: str
    driver_assist: str
    dynamic_brake_support: str
    edr: str
    esc: str
    ev_drive_unit: str
    electrification_level: str
    engine_configuration: str
    engine_cycles: str
    engine_cylinders: str
    enginehp: str
    enginehp_to: str
    enginekw: str
    engine_manufacturer: str
    engine_model: str
    entertainment_system: str
    error_code: str
    error_text: str
    forward_collision_warning: str
    fuel_injection_type: str
    fuel_type_primary: str
    fuel_type_secondary: str
    gcwr: str
    gcwr_to: str
    gvwr: str
    gvwr_to: str
    keyless_ignition: str
    lane_departure_warning: str
    lane_keep_system: str
    lower_beam_headlamp_light_source: str
    make_name: str
    make_id: str
    manufacturer_name: str
    manufacturer_id: str
    model_name: str
    model_id: str
    model_year: str
    motorcycle_chassis_type: str
    motorcycle_suspension_type: str
    ncsa_body_type: str
    ncsa_make: str
    ncsa_map_exc_approved_by: str
    ncsa_map_exc_approved_on: str
    ncsa_mapping_exception: str
    ncsa_model: str
    ncsa_note: str
    note: str
    other_bus_info: str
    other_engine_info: str
    other_motorcycle_info: str
    other_restraint_system_info: str
    other_trailer_info: str
    park_assist: str
    pedestrian_automatic_emergency_braking: str
    plant_city: str
    plant_company_name: str
    plant_country: str
    plant_state: str
    possible_values: str
    pretensioner: str
    rear_cross_traffic_alert: str
    rear_visibility_system: str
    sae_automation_level: str
    sae_automation_level_to: str
    seat_belts_all: str
    seat_rows: str
    seats: str
    semiautomatic_headlamp_beam_switching: str
    series: str
    series2: str
    steering_location: str
    suggestedvin: str
    tpms: str
    top_speedmph: str
    track_width: str
    traction_control: str
    trailer_body_type: str
    trailer_length: str
    trailer_type: str
    transmission_speeds: str
    transmission_style: str
    trim: str
    trim2: str
    turbo: str
    vin: str
    valve_train_design: str
    vehicle_type: str
    wheel_base_long: str
    wheel_base_short: str
    wheel_base_type: str
    wheel_size_front: str
    wheel_size_rear: str
    wheels: str
    windows: str


@dataclass(eq=True, frozen=True)
class PlantCode:
    address: str
    city: str
    country: str
    dot_code: str
    name: str
    old_dot_code: str
    postal_code: str
    state_province: str
    status: str

@dataclass(eq=True, frozen=True)
class Document:
    cover_letter_url: str
    letter_date: str
    manufacturer_id: int
    manufacturer_name: str
    name: str
    url: str
    type: str = None
    model_year_from: str = None
    model_year_to: str = None
