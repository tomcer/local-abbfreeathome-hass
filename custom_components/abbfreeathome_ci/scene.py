"""Create ABB-free@home scene entities."""

from typing import Any

from abbfreeathome import FreeAtHome
from abbfreeathome.channels.scene import Scene as FahScene

from homeassistant.components.scene import Scene as SceneEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_SERIAL, DOMAIN, MANUFACTURER


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up free@home scenes."""
    free_at_home: FreeAtHome = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        FreeAtHomeSceneEntity(
            channel,
            sysap_serial_number=entry.data[CONF_SERIAL],
        )
        for channel in free_at_home.get_channels_by_class(channel_class=FahScene)
    )


class FreeAtHomeSceneEntity(SceneEntity):
    """Defines a free@home scene entity."""

    _attr_should_poll: bool = False

    def __init__(
        self,
        channel: FahScene,
        sysap_serial_number: str,
    ) -> None:
        """Initialize the scene."""
        super().__init__()
        self._channel = channel
        self._sysap_serial_number = sysap_serial_number
        self._attr_name = channel.channel_name
        self._attr_unique_id = (
            f"{channel.device_serial}_{channel.channel_id}_scene"
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._channel.device_serial)},
            name=self._channel.device_name,
            manufacturer=MANUFACTURER,
            serial_number=self._channel.device_serial,
            suggested_area=self._channel.room_name,
        )

    async def async_activate(self, **kwargs: Any) -> None:
        """Activate (recall) the scene."""
        await self._channel.activate()
