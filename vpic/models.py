from dataclasses import dataclass
from typing import List, Optional


@dataclass(eq=True, frozen=True)
class Document:
    cover_letter_url: str
    letter_date: str
    manufacturer_id: int
    manufacturer: str
    name: str
    url: str
    type: Optional[str] = None
    model_year_from: Optional[str] = None
    model_year_to: Optional[str] = None


@dataclass(eq=True, frozen=True)
class Make:
    make_id: int
    make: str
    manufacturer_id: Optional[int] = None
    manufacturer: Optional[str] = None
    vehicle_type_id: Optional[int] = None
    vehicle_type: Optional[str] = None


@dataclass(eq=True, frozen=True)
class Model:
    model_id: int
    model: str
    make_id: Optional[int] = None
    make: Optional[str] = None
    vehicle_type_id: Optional[int] = None
    vehicle_type: Optional[str] = None


@dataclass(eq=True, frozen=True)
class Manufacturer:
    manufacturer_id: int
    manufacturer: str
    manufacturer_common_name: str


@dataclass(eq=True, frozen=True)
class ManufacturerType:
    name: str


@dataclass(eq=True, frozen=False)
class VehicleType:
    name: Optional[str]
    vehicle_type: Optional[str]
    vehicle_type_id: Optional[int] = None
    make: Optional[str] = None
    make_id: Optional[int] = None
    gvwr_from: Optional[str] = None
    gvwr_to: Optional[str] = None
    is_primary: Optional[bool] = None

    def __post_init__(self):
        if self.name is not None:
            self.vehicle_type = self.name
        del self.name


@dataclass(eq=True, frozen=True)
class ManufacturerDetail:
    manufacturer_id: int
    manufacturer: str
    manufacturer_common_name: Optional[str]
    manufacturer_types: List[ManufacturerType]
    vehicle_types: List[VehicleType]
    address: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    contact_email: Optional[str] = None
    contact_fax: Optional[str] = None
    contact_phone: Optional[str] = None
    country: Optional[str] = None
    dbas: Optional[str] = None
    equipment_items: Optional[List[str]] = None
    last_updated: Optional[str] = None
    other_manufacturer_details: Optional[str] = None
    postal_code: Optional[str] = None
    primary_product: Optional[str] = None
    principal_first_name: Optional[str] = None
    principal_last_name: Optional[str] = None
    principal_position: Optional[str] = None
    state_province: Optional[str] = None
    submitted_name: Optional[str] = None
    submitted_on: Optional[str] = None
    submitted_position: Optional[str] = None


@dataclass(eq=True, frozen=True)
class PlantCode:
    dot_code: str
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    old_dot_code: Optional[str] = None
    postal_code: Optional[str] = None
    state_province: Optional[str] = None
    status: Optional[str] = None


@dataclass(eq=True, frozen=True)
class Value:
    element_name: str
    id: int
    name: str


@dataclass(eq=True, frozen=True)
class Variable:
    id: int
    name: str
    group_name: Optional[str]
    data_type: str
    description: str


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
    battery_a: str
    battery_a_to: str
    battery_cells: str
    battery_info: str
    battery_kwh: str
    battery_kwh_to: str
    battery_modules: str
    battery_packs: str
    battery_type: str
    battery_v: str
    battery_v_to: str
    bed_length_in: str
    bed_type: str
    blind_spot_intervention: str
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
    charger_power_kw: str
    cooling_type: str
    curb_weight_lb: str
    custom_motorcycle_type: str
    daytime_running_light: str
    destination_market: str
    displacement_cc: str
    displacement_ci: str
    displacement_l: str
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
    engine_hp: str
    engine_hp_to: str
    engine_kw: str
    engine_manufacturer: str
    engine_model: str
    entertainment_system: str
    error_code: str
    error_text: str
    forward_collision_warning: str
    fuel_injection_type: str
    fuel_type_primary: str
    fuel_type_secondary: str
    gcwr_from: str
    gcwr_to: str
    gvwr_from: str
    gvwr_to: str
    keyless_ignition: str
    lane_centering_assistance: str
    lane_departure_warning: str
    lane_keep_system: str
    lower_beam_headlamp_light_source: str
    make: str
    make_id: str
    manufacturer: str
    manufacturer_id: str
    model: str
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
    rear_automatic_emergency_braking: str
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
    suggested_vin: str
    tpms: str
    top_speed_mph: str
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


@dataclass(eq=True, frozen=False)
class WorldManufacturerIndex:
    created_on: str
    date_available_to_public: str
    manufacturer: Optional[str]
    name: Optional[str]
    id: Optional[int]
    updated_on: Optional[str]
    vehicle_type: str
    wmi: Optional[str] = None
    common_name: str = ""
    country: Optional[str] = None
    make: str = ""
    manufacturer_id: Optional[int] = None
    parent_company_name: str = ""
    url: str = ""

    def __post_init__(self):
        if self.id is not None:
            self.manufacturer_id = self.id
        del self.id
        if self.name is not None:
            self.manufacturer = self.name
        del self.name
