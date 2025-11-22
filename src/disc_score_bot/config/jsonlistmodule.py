from pathlib import Path

from .config import Config
from abc import abstractmethod
from dataclasses import dataclass, asdict, is_dataclass
from typing import List, Type, TypeVar, Optional

T = TypeVar("T")

class JsonListModule(Config):
    """Base class for configs stored as list[dataclass] in JSON."""

    module_name: str = None
    key_field: Optional[str] = "discord_id"  # default, can be None
    item_cls: Type[T] = None  # must be set in child classes

    def create_module(self):
        return self.write([], self.module_name)

    def _from_dict(self, data: dict) -> T:
        return self.item_cls(**data) # pylint: disable=not-callable

    def _to_dict(self, obj: T) -> dict:
        if is_dataclass(obj):
            return asdict(obj)
        return obj.__dict__

    def get_all(self, **filters) -> List[T]:
        """Return all items, optionally filtered by key=value pairs"""
        if not self.module_exists():
            return []

        items = [self._from_dict(item) for item in self.read(self.module_name)]
        if filters:
            def match(obj):
                return all(getattr(obj, k) == v for k, v in filters.items())
            items = [obj for obj in items if match(obj)]
        return items

    def get_item(self, key_value) -> Optional[T]:
        """Get item by key_field (if key_field is defined)"""
        if self.key_field is None:
            raise ValueError(f"{self.module_name} has no key_field; use get_all(filters) instead.")

        if not self.module_exists():
            return None

        json_object = self.read(self.module_name)
        for item in json_object:
            if item[self.key_field] == key_value:
                return self._from_dict(item)
        return None

    def add_item(self, obj: T):
        """Add or update an item"""
        json_object = self.read(self.module_name) or []

        if self.key_field:
            key_value = getattr(obj, self.key_field, None)
            if key_value is None:
                raise ValueError(f"{self.module_name} requires {self.key_field} for add/update.")

            modified = False
            for item in json_object:
                if item[self.key_field] == key_value:
                    item.update(self._to_dict(obj))
                    modified = True
                    break
            if not modified:
                json_object.append(self._to_dict(obj))
            return self.write(json_object, self.module_name), modified

        # List-only mode → use "name" as soft-key if present
        modified = False
        if hasattr(obj, "name") and obj.name:
            for item in json_object:
                if item.get("name") == obj.name:
                    item.update(self._to_dict(obj))
                    modified = True
                    break

        if not modified:
            json_object.append(self._to_dict(obj))

        return self.write(json_object, self.module_name), modified

    def remove_item(self, key_value):
        """Remove an item by key_field (if key_field is defined)"""
        if self.key_field is None:
            raise ValueError(f"{self.module_name} has no key_field; use get_all() and filter manually.")

        if not self.module_exists():
            return False

        cfg = self.read(self.module_name)
        for i, item in enumerate(cfg):
            if item[self.key_field] == key_value:
                del cfg[i]
                return self.write(cfg, self.module_name)
        return False