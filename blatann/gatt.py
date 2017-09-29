import enum
import logging
from blatann.nrf.nrf_types.gatt import BLE_GATT_HANDLE_INVALID


logger = logging.getLogger(__name__)


class SecurityLevel(enum.Enum):
    NO_ACCESS = 0
    OPEN = 1
    JUST_WORKS = 2
    MITM = 3


class ServiceType(enum.Enum):
    PRIMARY = 1
    SECONDARY = 2


class SubscriptionState(enum.Enum):
    NOT_SUBSCRIBED = 0
    NOTIFY = 1
    INDICATION = 2


class CharacteristicProperties(object):
    def __init__(self, read=True, write=False, notify=False, indicate=False, broadcast=False,
                 write_no_response=False, signed_write=False):
        self.read = read
        self.write = write
        self.notify = notify
        self.indicate = indicate
        self.broadcast = broadcast
        self.write_no_response = write_no_response
        self.signed_write = signed_write

    @classmethod
    def from_nrf_properties(cls, nrf_props):
        """
        :type nrf_props: blatann.nrf.nrf_types.BLEGattCharacteristicProperties
        """
        return CharacteristicProperties(nrf_props.read, nrf_props.write, nrf_props.notify, nrf_props.indicate,
                                        nrf_props.broadcast, nrf_props.write_wo_resp, nrf_props.auth_signed_wr)

    def __repr__(self):
        props = [
            [self.read, "r"],
            [self.write, "w"],
            [self.notify, "n"],
            [self.indicate, "i"],
            [self.broadcast, "b"],
            [self.write_no_response, "wn"],
            [self.signed_write, "sw"],
        ]
        props = [c for is_set, c in props if is_set]
        return "CharProps({})".format(",".join(props))

class CharacteristicDescriptor(object):
    class Type(enum.Enum):
        EXTENDED_PROPERTY = 0x2900
        USER_DESCRIPTION = 0x2901
        CLIENT_CHAR_CONFIG = 0x2902
        SERVER_CHAR_CONFIG = 0x2903
        PRESENTATION_FORMAT = 0x2904
        AGGREGATE_FORMAT = 0x2905

    def __init__(self, uuid, handle):
        self.uuid = uuid
        self.handle = handle


class Characteristic(object):
    def __init__(self, ble_device, peer, uuid, properties):
        """
        :type ble_device: blatann.device.BleDevice
        :type peer: blatann.peer.Peer
        :type uuid: blatann.uuid.Uuid
        :type properties: CharacteristicProperties
        """
        self.ble_device = ble_device
        self.peer = peer
        self.uuid = uuid
        self.declaration_handle = BLE_GATT_HANDLE_INVALID
        self.value_handle = BLE_GATT_HANDLE_INVALID
        self.cccd_handle = BLE_GATT_HANDLE_INVALID
        self.cccd_state = SubscriptionState.NOT_SUBSCRIBED
        self._properties = properties

    def __repr__(self):

        return "Characteristic({}, {}".format(self.uuid, self._properties)


class Service(object):
    def __init__(self, ble_device, peer, uuid, service_type,
                 start_handle=BLE_GATT_HANDLE_INVALID, end_handle=BLE_GATT_HANDLE_INVALID):
        """
        :type ble_device: blatann.device.BleDevice
        :type peer: blatann.peer.Peer
        """
        self.ble_device = ble_device
        self.peer = peer
        self.uuid = uuid
        self.service_type = service_type
        self.characteristics = []
        self.start_handle = start_handle
        # If a valid starting handle is given and not a valid ending handle, then the ending handle
        # is the starting handle
        if start_handle != BLE_GATT_HANDLE_INVALID and end_handle == BLE_GATT_HANDLE_INVALID:
            end_handle = start_handle
        self.end_handle = end_handle

    def __repr__(self):
        return "Service({}, characteristics: [{}])".format(self.uuid, "\n    ".join(str(c) for c in self.characteristics))


class GattDatabase(object):
    def __init__(self, ble_device, peer):
        """
        :type ble_device: blatann.device.BleDevice
        :type peer: blatann.peer.Peer
        """
        self.ble_device = ble_device
        self.peer = peer
        self.services = []

    def __repr__(self):
        return "Database(peer {}, services: [{}])".format(self.peer.conn_handle, "\n  ".join(str(s) for s in self.services))